# C41 — Identity / actor model & attribution  (Spec, canonical track)

> Source: README Part 4 **P9 — Attribution** (lines 220–231: "Every commit, task, event carries actor identity. Foundation for debug, compliance, trust"; the 4-row component table — Identity model = "Gas City `actor` schema (cities, rigs, agents)"; Action attribution = "Gas City beads, events native `created_by`" / "strongest principle match"; Audit trail = "Gas City event bus + bead history"; Identity verification = "Custom: signature on bead provenance" / "**optional, deferred**"); README:90 ("attribution is automatic"); README:371 ("P9 (attribution): native; every bead and event carries `created_by`"); AI-CONTEXT §3.1 row 9 ("**Strongest match in entire corpus** — automatic everywhere"); AI-CONTEXT §3.2 ("nine concepts" #1 Session → P9, #2 Bead Store → P9, #3 Event Bus → P9, #6 Messaging → P9); AI-CONTEXT §3.3 vocabulary table (city = workspace, rig = agent worker role); AI-CONTEXT §13.3 rig-partition skeleton (`[[rig]]` blocks); F-MODE-COVERAGE §2 (F14 "Attribution collapse" → "every bead, event, action carries actor"; F32 "Mail-injection / unsigned coordination" → "P9 attribution + optional HMAC signing layer"), §6 (F43 "RSI Board-Visibility Gap" → "P9 attribution + audit trail + bead history"), §7 (F32 revisit → "HMAC signing on mail bus"); component-inventory C41 row (maps `A43, A44, A44b, A44c, A19d, B50, B51, A22i`; depends on C01, C19, C23; gap G36; foundational: yes; critical-path note: "cross-cutting load-bearer that touches nearly everything … every action"); ambiguities-and-gaps **G36** (minor — "Attribution integrity is optional/deferred … without signed provenance, attribution is *self-asserted* … an optional guard does not address a security failure").
> Inventory ID: C41   Kind: component   Status: sweep-2
> Track: A (canonical)
> Binding decisions obeyed: **D-5** (C41 owns the provenance hash-chain, computed over C23-provided ordered gap-free `event_id`s; C23 provides ordered ids only, never the chain), **D-14** (G37 ≠ FE-3; signing stays deferred; specs deferring signing cite G37, not FE-3).

> [D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25] Two substrate facts from the Gas
> City prototype harvest apply to C41: **(F8)** all inter-agent coordination passes *through the bead
> store* — agents write beads and recipients poll — so the `created_by` field on each bead is the
> *primary* attribution record for every inter-agent action (confirms the universal-attribution
> invariant is not theoretical; the bead-write path IS the coordination path). **(F9)** the Dolt bead
> store backend requires `dolt push --ref refs/heads/<branch>` in proxy-mediated environments; this is
> an ops-portability caveat for C19, not a C41 schema concern. The key C41 implication of F8: because
> agents *only* interact via beads (and events), the `created_by` on every bead/event is the exhaustive
> attribution record — no side-channel action exists to be unattributed. This strengthens the F14
> invariant claim while leaving the substrate-enforcement question (OQ-C41-3) open.

## 1. Purpose & responsibility

C41 is the **identity / actor model and attribution layer** of the factory. It answers two questions
for every action in the system: **"who or what acted?"** (the actor model — cities, rigs, agents) and
**"is that recorded on the action?"** (attribution — `created_by` on every bead and event). It is P9 in
the principle taxonomy, which README and AI-CONTEXT both name **the single strongest native match in the
entire corpus** — attribution flows automatically through Gas City beads and events without
configuration (README:231; AI-CONTEXT §3.1 row 9).

C41 exists as a *named component* (not just "a field") because three things must be defined for
attribution to be load-bearing rather than incidental: (1) the **actor vocabulary** — the closed set of
actor kinds (city, rig, agent, tool) that may legitimately appear in a `created_by` (`tool` added per
INT-4 to cover C17 tool-node actors); (2) the **universality invariant** — that *every* state-changing
action carries a `created_by`, with no unattributed path; and (3) the **audit trail** — that the union
of bead history (C19) and the event bus (C23) is a queryable, append-only record of who did what. The optional fourth piece — **identity *verification*** (signed
provenance proving the claimed actor is the actual actor) — v4 marks "optional, deferred" (README:229),
so C41 *defines the seam* for it but does not require it (gap G36; see §6). **D-5** adds a fifth,
non-optional piece unique to C41: the **provenance hash-chain** — a tamper-evident chain computed over
C23-provided ordered gap-free `event_id`s. This is the one genuine small custom piece beyond the
substrate-native `created_by`; it provides tamper evidence that the `created_by` stream has not been
reordered or truncated, without requiring signatures (which would need G37-resolved key storage).

**Responsibilities**
- Define the **actor model**: the actor kinds — **city** (workspace), **rig** (agent worker role),
  **agent** (the acting worker/judge/scenario role), **tool** (automated tool-node actors, e.g.
  C17 `inspect_eval`; added per INT-4) — and how an actor is identified (README:226 "Gas City
  `actor` schema (cities, rigs, agents)"; AI-CONTEXT §3.3 city/rig vocabulary; `tool` is the
  INT-4 addition required so `resolve_actor("tool:inspect_eval")` succeeds).
- Own the **`created_by` attribution semantics**: what a `created_by` value *is* (a reference to an actor
  in the actor model), so that C19 (beads) and C23 (events) — which merely *carry* the field — resolve to
  a defined actor (README:227 "native `created_by`"; component-inventory: beads/events carry `created_by`,
  verification deferred to C41).
- Assert the **universal-attribution invariant**: every action that writes a bead (C19/C20) or emits an
  event (C23) carries a `created_by`; there is no unattributed write path (README:222 "Every commit,
  task, event carries actor identity"; F14 "Addressed").
- Define the **audit trail** as the queryable union of **bead history** (C19) and the **append-only event
  bus** (C23) keyed by actor (README:228 "Audit trail — Gas City event bus + bead history").
- Own the **provenance hash-chain** (D-5): the tamper-evident chain computed over C23-provided ordered
  gap-free `event_id`s. C23 provides the ordered `event_id` stream; C41 computes, stores, and exposes
  the verification interface. This is a P-principle capability (tamper evidence for audit trail integrity)
  and is the only non-trivial custom piece C41 builds.
- Define the **provenance-verification seam** (the *optional* signed-provenance pack): the place a
  signature over a bead/event's provenance would attach, what it would cover, and how a verifier would
  check it — **named and described, not required** (README:229 "Custom: signature on bead provenance …
  optional, deferred"; G36; signing deferred to FE-3 per D-14). The HMAC-mail-signing variant
  referenced for F32 attaches at this seam (F-MODE-COVERAGE §2/§7), though the mail bus itself is C06.

**Explicitly NOT**
- NOT the bead store (C19) or the bead schema (C20). C19 owns persistence and the `gc bd` graph; C20
  declares `created_by` as a required *envelope field*. C41 owns the **meaning** of that field — the
  actor it points at and the verification (or non-verification) of the claim. (C20 §1 states the same
  boundary in reverse: "C41 owns *who can act* and the `created_by` provenance semantics; C20 merely
  declares `created_by`".)
- NOT the event bus (C23). C23 is the append-only JSONL transport that *records* every action; C41
  defines that each such record carries a resolvable actor and that the bus + bead history *form* the
  audit trail. C41 ≠ C23 (inventory lists both as distinct foundational rows; C41 depends on C23).
- NOT **authorization / partitioning** (C42) or the **isolation boundary** (C43). C41 says *who acted*;
  it does **not** decide *what an actor is allowed to do*. Read/write partitions across worker/scenario/
  judge rigs are C42; the lethal-trifecta boundary is C43. C41 supplies the identity those policies are
  written against; it does not enforce them. (Inventory: C42 = "Worker/scenario/judge roles with read/
  write partitions"; C43 = "isolation & lethal-trifecta boundary".)
- NOT secrets / credential management (G37). OAuth tokens, mTLS certs, judge-provider credentials live in
  config (C03) / env; C41 does not store or rotate them. G37 is assigned to C03/C43, not C41.
- NOT a **mandatory cryptographic provenance** system. v4 marks identity verification "optional,
  deferred" (README:229). **D-14** confirms: "Signing stays deferred (Bet 2 → FE-3); resolves the old
  'signing mandatory vs optional' → optional/deferred (README:229), revisit at FE-3's trigger." C41
  defines the seam and flags the residual risk (G36).
- NOT the messaging bus (C06). C06 owns Mail/Nudge and the *optional HMAC signing* of mail; C41 owns the
  identity that signing would bind to. (Inventory: C06 carries gap G36 too — the HMAC seam — but the
  signing layer attaches at C41's provenance seam.)

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | The `actor` schema, `created_by`, beads, and the event bus are all Gas City native (README:226–228; AI-CONTEXT §3.2). C41 elaborates Gas City's actor model; it does not build a new one. Inventory: C41 `depends on C01`. |
| Upstream (depends on) | **C19** Bead store / work-graph | Beads carry `created_by`; bead *history* is half the audit trail. C41 defines what that field resolves to. Inventory: C41 `depends on C19`. |
| Upstream (depends on) | **C23** Event bus | Append-only JSONL records every action with `created_by`; the bus is the other half of the audit trail (README:228). **D-5**: C23 provides gap-free ordered `event_id`s; C41 consumes them to compute the provenance hash-chain. Inventory: C41 `depends on C23`. |
| Sibling (field declarer) | **C20** Bead schema registry | C20 declares `created_by` as a required envelope field on every bead; C41 supplies its meaning + verification seam. (C20 §1 / §6 cross-reference.) |
| Downstream (consumes identity) | **C42** Rig / agent-role partitioning | Writes read/write authorization policy *against* C41's actor identities (worker vs scenario vs judge rig). C41 supplies the subject; C42 supplies the policy. |
| Downstream (consumes identity) | **C43** Isolation & lethal-trifecta boundary | Boundary typing is written against actor identity; C41 supplies the "who". |
| Downstream (consumes the seam) | **C06** Messaging (Mail + Nudge) | Optional HMAC mail signing (F32) binds a message to a C41 actor via the provenance seam. Inventory: C06 gap G36. |
| Downstream (consumes audit trail) | **C35** Override→pattern→rule loop; **C46** meta-metrics; RSI visibility (F43) | Override beads, meta-metrics, and RSI-status declarations all read the actor-keyed audit trail (F43: "P9 attribution + audit trail + bead history"). |

C41 is **foundational** (inventory: yes) and in **Batch 1** (authored in parallel with C01/C19/C20/C23).
The inventory's critical-path note names C41 a **cross-cutting load-bearer that "touches nearly
everything but is not on a single linear path … every action."** It is load-bearing because the
universal-attribution invariant is a precondition for F14 (attribution collapse), F32 (unsigned
coordination), and F43 (RSI board-visibility) all being marked Addressed.

## 3. Interfaces / contracts

### 3.1 Actor-model contract

The closed vocabulary of actor *kinds* (`city`, `rig`, `agent`, `tool`) and the shape of an *actor
reference* that a `created_by` resolves to. Any component reading a `created_by` can resolve it to
`(kind, identifier)` against this contract. (`tool` added per INT-4 — see §3.1 fix note above.)

**Interface signature (C41-I1):**
```
resolve_actor(created_by: string) → ActorRef | ActorResolutionError
  ActorRef = { kind: "city" | "rig" | "agent" | "tool", id: string }
  ActorResolutionError: E-C41-03 (unknown kind), E-C41-04 (malformed ref)
```

> **INT-4 FIX (Sweep-2):** `tool` is added to the `kind` enum. C17 tool-nodes (e.g. `inspect_eval`)
> emit `created_by = "tool:inspect_eval"` (D-29 wire type). C41 is the vocabulary authority; if
> `tool` is not in the enum then `resolve_actor("tool:inspect_eval")` raises E-C41-03 (unknown kind),
> breaking the universality invariant (every action attributable). The `{city, rig, agent, tool}`
> closed set is now the canonical actor-kind vocabulary. All invariant text and error descriptions
> that name `{city, rig, agent}` are updated to include `tool`.

> `created_by` wire type = colon-delimited `"kind:id"` string per **D-29** (parsed to C41 `ActorRef`); resolves OQ-C41-4. `ActorRef` is the in-memory/parsed form; the wire value across C19/C20/C21/C23 is the `"kind:id"` string (e.g. `"rig:worker-1"`).

### 3.2 `created_by` attribution contract

The guarantee that every bead (via C20 envelope) and every event (via C23 record) carries a
`created_by` whose value is a valid actor reference. This is the contract C19/C20/C23 rely on and
that downstream auditors trust.

**Precondition.** The writing component has a valid ActorRef for the acting actor.  
**Postcondition.** The written bead/event record carries `created_by` equal to a string that
`resolve_actor` returns without error.  
**Invariant.** An unattributed write (missing or empty `created_by`) is invalid — rejected or flagged
(enforcement strength is OQ-C41-3 / G11-gated; see §6).

### 3.3 Audit-trail query contract (C41-I2)

The named ability to ask "what did actor X do?" / "who created bead/event Y?" by reading the union
of bead history (C19) + event bus (C23), keyed by actor. The concrete query surface (`gc bd` filters
+ event-bus scan) is C19/C23's; C41 defines that it is *answerable by actor*.

```
audit_trail(actor: ActorRef) → stream<AuditRecord>
  AuditRecord = { source: "bead" | "event", id: string, created_by: ActorRef, timestamp: timestamp, payload_digest: sha256 }
audit_trail_by_id(id: string) → AuditRecord | NotFound
```

### 3.4 Provenance hash-chain contract (D-5) (C41-I3)

**D-5 (ADOPTED, verbatim):** "**C41 owns the provenance hash-chain**, computed over C23-provided
ordered `event_id`s. C23 provides gap-free ordered `event_id`s only; it does NOT provide the chain."

C41 exposes two operations over the chain:

```
chain_append(event_ids: gap_free_ordered_list<EventId>) → ChainEntry
  # Appends one entry; event_ids is the C23-ordered gap-free batch since the last entry.
  # C41 computes payload_digest over the C23 record bytes at chain-append time (D-27).
  # Returns the new ChainEntry (prev_hash, event_ids, payload_digest, entry_hash).

chain_verify(from_seq: uint64, to_seq: uint64) → VerifyResult
  VerifyResult = { ok: bool, first_mismatch_seq: uint64 | null, error: ChainError | null }
  ChainError: E-C41-05 (hash mismatch), E-C41-06 (chain gap), E-C41-07 (entry missing)
```

**Invariant.** The chain is append-only; entries are never rewritten. A `chain_verify` that returns
`ok=false` signals tamper evidence: either a hash recomputed differently (E-C41-05) or a gap in the
event_id sequence (E-C41-06).

**Signing deferred boundary.** The chain provides *tamper evidence* without signatures. **Attestation
and signing are DEFERRED to FE-3** per D-14: "G37 = open secrets/credential-storage gap (owned by
C03; plaintext `city.toml`/env today). FE-3 = graduated-mandatory signing, BLOCKED ON G37 but a
distinct deferred enhancement. Specs deferring secrets cite **G37**, not FE-3. Signing stays deferred
(Bet 2 → FE-3)." C41 names the seam where a signature over chain entries would attach (the optional
verification pack, §4.3), but does **not** specify a signing mechanism. The seam is defined so adding
signing later is additive (no chain rework).

### 3.5 Provenance-verification seam (optional, deferred) (C41-I4)

The *named, optional* interface where a signature over a bead/event's provenance attaches and is
checked: what bytes the signature covers (the actor reference + the action's identifying content),
where the signature is stored, and the verify operation (`actor-claimed == actor-signed`). Marked
optional/deferred per README:229; algorithm/keys are the optional pack's later sweeps — see the G36
AMBIGUITY block in §6 and D-14 above. The HMAC-mail-signing layer (F32) is one instantiation of this
seam; the bead-provenance-signature variant (README:229) is another.

### 3.6 C23 event_id stream seam (the interface to freeze first, D-5)

The C23→C41 seam is the load-bearing input to the hash-chain. C23 MUST provide:

```
event_id_stream(from_seq: uint64 | null) → gap_free_ordered_list<EventRecord>
  EventRecord = { event_id: EventId, created_by: string, timestamp: timestamp }
  EventId = { stream: string, seq: uint64 }
  # gap-free: no skipped seq numbers between from_seq and last returned event_id.seq
  # ordered: returned in strictly ascending event_id.seq order
```

> Wire type per **D-26**: `event_id` is C23's `EventId = {stream, seq}` struct, not a bare integer.

> Per **D-27**: `payload_digest` is computed by C41 over the C23 record bytes at chain-append time; C23 does not provide it.

**Freeze requirement:** This seam (the gap-free ordered `event_id` stream, with `event_id` as a
monotonic sequence number) must be frozen jointly with C23 before C41's chain implementation can
proceed. OQ-C41-5 gates this.

**Invariants**
- **Universal attribution**: no state-changing action (bead write, event emit) exists without a
  `created_by` resolving to a valid actor. An unattributed write is invalid (this *is* F14 "Addressed";
  README:222).
- **Actor-kind closure**: every `created_by` resolves to one of the named kinds (city / rig / agent / tool);
  an actor of unknown kind is invalid. (> [FAITHFUL-FILL + INT-4] — see §4.1.)
- **Append-only audit**: the audit trail (event bus + bead history) is append-only; attribution records
  are never rewritten (C23 is "append-only JSONL with monotonic seq" — AI-CONTEXT §3.2 #3).
- **Chain append-only**: chain entries are never rewritten or deleted; a recomputed hash that differs
  from the stored hash is tamper evidence (E-C41-05).
- **Self-asserted by default**: absent the optional verification pack, `created_by` is the actor's *own
  claim*, not a proven identity (README:229; G36). C41 records this as a stated invariant so downstream
  components do not over-trust attribution (see §6/§7).

## 4. Data model / state

C41 owns the **actor model and the attribution semantics** and **the provenance hash-chain**. Bead
instances live in C19; event records live in C23. C41 defines what the `created_by` *on* those records
means, and maintains the chain.

### 4.1 Actor reference (the value of `created_by`)

**Field table — ActorRef (the structured value `created_by` resolves to):**

| Field | Type | Req? | Semantics | Read-by | Write-by |
|---|---|---|---|---|---|
| `kind` | `enum{"city","rig","agent","tool"}` | R | the actor kind — closed set (README:226 "cities, rigs, agents" + `tool` added per INT-4 to cover C17 tool-node actors, e.g. `"tool:inspect_eval"`) | C41 resolve_actor; C42 partition; C43 boundary | writer stamps on bead/event creation |
| `id` | `string` | R | the specific actor identifier — rig name from a `[[rig]]` block (AI-CONTEXT §13.3), agent name from `[[agent]]` (AI-CONTEXT §3.4) | C41 audit_trail; C42; C43 | writer; sourced from Gas City config |
| `signature` | `bytes` | O | signed provenance binding ref to action — **present only with the optional verification pack** (README:229; G36; signing deferred to FE-3 per D-14) | C41-I4 verifier | optional pack writes |

> [FAITHFUL-FILL] **Actor-kind set = {city, rig, agent, tool}.** v4 names "cities, rigs, agents"
> verbatim as the Gas City `actor` schema (README:226); the `agent` kind is sourced from README:226 +
> §3.4 `[[agent]]` blocks (RC41A-01 — *not* from §3.3, which glosses only city/rig and ambiguously maps
> rig = "agent worker role"). **INT-4 (Sweep-2) adds `tool`:** C17 tool-nodes (e.g. `inspect_eval`)
> emit `created_by = "tool:inspect_eval"` (D-29 wire type). C41 owns the vocabulary; without `tool`
> in the enum, `resolve_actor("tool:inspect_eval")` raises E-C41-03 and breaks the universality
> invariant. `tool` is the fourth kind — a distinct actor class for automated tool-node actors that
> are neither a city workspace, a rig worker role, nor an agent persona. Whether
> the *human operator* is modeled as an `agent`, a distinct kind, or sits outside the actor model entirely
> is a real open question (overrides are operator actions — README P8) — flagged as OQ-C41-2; the smallest
> faithful reading is that the operator acts *through* an agent/rig and is attributed as such, since v4
> gives no fifth kind. Concrete identifier grammar: `"<kind>:<id>"` e.g. `"rig:worker-1"`,
> `"agent:judge"`, `"tool:inspect_eval"` — the colon-delimited prefix is the minimal structured encoding
> (OQ-C41-4).

> [FAITHFUL-FILL] **Actor reference is (minimal faithful reading) a (kind, identifier) pair, not a flat
> string — pending C19/C23 ratification (OQ-C41-4).** v4 stores `created_by` as a field but never gives
> its internal shape. The smallest consistent elaboration that lets a reader "resolve to a valid actor"
> (§3 contract) is a structured (kind, identifier) reference rather than an opaque string, because the
> actor *kinds* are explicitly enumerated and partitioning (C42) is written against kind
> (worker/scenario/judge rigs). This does not add a store — it only structures an existing field.
> *Honesty caveat (RC41A-04):* C19/C23 faithful specs currently treat `created_by` as an **opaque carried
> value** and have not ratified this structure; if they ship a flat string, this fill is over-reach. The
> flat-string-vs-structured choice is the joint freeze OQ-C41-4 (plan M1). Wire encoding deferred to sweep 2.

### 4.2 Provenance hash-chain entry (D-5)

**Field table — ChainEntry (one entry in the C41-owned provenance hash-chain):**

| Field | Type | Req? | Semantics | Read-by | Write-by |
|---|---|---|---|---|---|
| `seq` | `uint64` | R | monotonic sequence number of this chain entry; starts at 0 | C41 verify; auditors | C41 chain_append (auto-increments) |
| `prev_hash` | `sha256 \| null` | R | SHA-256 of the previous ChainEntry (serialised canonical form); `null` only for seq=0 (genesis) | C41 verify | C41 chain_append |
| `event_ids` | `gap_free_ordered_list<EventId>` | R | the C23 event_ids this entry covers — gap-free, strictly ascending, from C23's monotonic sequence (D-5: C23 provides these; C41 consumes). Wire type per **D-26**: `EventId = {stream: string, seq: uint64}`, not a bare integer. | C41 verify; auditors | C41 chain_append from C23 stream |
| `payload_digest` | `sha256` | R | SHA-256 computed by C41 over the C23 record bytes for the events in `event_ids` at chain-append time (tamper-evidence over attribution stream). Per **D-27**: this is a C41 chain-internal field; C23 does not provide it. | C41 verify | C41 chain_append |
| `entry_hash` | `sha256` | R | SHA-256 of the canonical serialisation of `{seq, prev_hash, event_ids, payload_digest}` — the linkage value that becomes the next entry's `prev_hash` | C41 verify | C41 chain_append |
| `appended_at` | `timestamp` | R | wall-clock time the entry was appended (local to the C41 process; not a cryptographic timestamp) | auditors; ops | C41 chain_append |

> [FAITHFUL-FILL] **Hash function = SHA-256; canonical serialisation = JSON-canonical (RFC 8785).**
> v4 never names a hash function. SHA-256 is the minimal faithful choice: it is a widely-available,
> collision-resistant standard hash; the provenance hash-chain is a tamper-evidence structure (not a
> cryptographic commitment scheme requiring specialized properties). JSON-canonical (RFC 8785) is the
> minimal deterministic serialisation that avoids key-ordering ambiguity. Both are conventional and
> reversible without architectural impact if a future review chooses differently.

> [FAITHFUL-FILL] **Entry granularity: one chain entry per C23 flush (not one per event).** D-5 says
> the chain is computed over C23-provided ordered `event_id`s but does not specify entry granularity.
> Batching per-C23-flush (one entry covering the event_ids since the last flush) is the minimal
> consistent choice: it bounds chain entry count, matches C23's natural append cadence, and avoids
> one-entry-per-event overhead. Concrete flush interval is OQ-C41-5.

### 4.3 Audit trail (derived, not owned)

The audit trail is **not new state** — it is the *actor-keyed view* over two stores C41 depends on:

```
audit-trail(actor X) ≡ { beads in C19 where created_by == X (+ bead history) }
                      ∪ { events in C23 where created_by == X }
```

C41 owns the *definition* (it is keyed by actor and append-only); C19 and C23 own the bytes. This is
README:228's "Audit trail — Gas City event bus + bead history". No separate audit store is introduced
(faithful: v4 names none).

### 4.4 Chain store

The chain store holds ChainEntry records. It is a **C41-owned, append-only log** — the only new state
C41 introduces beyond defining semantics. Persistence mechanism: a simple append-only JSONL file or a
Dolt table alongside the bead store (C19) — implementation choice deferred to the build phase, not
architecture. What is frozen: append-only, single-writer (the C41 chain_append caller), queryable by
`seq` range.

### 4.5 Provenance signature (optional, deferred)

When the optional verification pack is installed, a signature attaches to a bead/event's provenance. v4
specifies only "signature on bead provenance" (README:229) and "HMAC signing on mail bus" (F-MODE §7).
C41 (sweep 2) defines *where it attaches and what it covers* (the actor reference + the action's
identifying content) but **not** the algorithm, key model, or rotation — those are sweep-2/sweep-3 of
the *optional pack*, and v4 marks the whole thing deferred. **D-14 (verbatim):** "G37 = open
secrets/credential-storage gap (owned by C03; plaintext `city.toml`/env today). FE-3 = graduated-
mandatory signing, BLOCKED ON G37 but a distinct deferred enhancement. Specs deferring secrets cite
**G37**, not FE-3." The seam this pack installs into is §3.5 / C41-I4.

### 4.6 Persistence & consistency

C41 holds **one piece of instance state**: the chain store (§4.4). The actor model is a *definition*
(like C20's registry); the attribution values live on C19 beads and C23 events. C41's consistency
requirements: **(a) resolvability** — every `created_by` written by C19/C23 must resolve to a valid
actor under the C41 actor model (otherwise F14 attribution-collapse re-opens); **(b) chain
monotonicity** — `seq` values are strictly increasing; **(c) chain completeness** — every C23 event_id
appears in exactly one chain entry (no gaps, no double-counting). The actor *registry* (which concrete
rigs/agents exist) is sourced from Gas City config — `[[rig]]` / `[[agent]]` blocks in `city.toml`
(AI-CONTEXT §3.4, §13.3) — so C41 does not own a separate actor database.

## 5. Behavior

C41 has no control loop; its behavior is **definitional**, **stamp-time**, **chain-append-time**, and
(optionally) **verify-time**:

- **Definition-time**: declares the actor model (kinds + reference shape) and the universal-attribution
  invariant.
- **Stamp-time**: when any component writes a bead (C19/C20) or emits an event (C23), the substrate
  stamps `created_by` with the acting actor's reference. In faithful v4 this is **automatic** — README:231
  ("Attribution flows automatically … without configuration") and AI-CONTEXT §3.1 ("automatic
  everywhere"). C41's role is to guarantee the stamp is present and well-formed, not to perform the write.
- **Chain-append-time** (D-5): C41 consumes the C23 gap-free ordered `event_id` stream and appends a
  chain entry covering each batch. This is the non-trivial custom behavior C41 performs. The append is
  triggered by the C23 flush boundary (OQ-C41-5).
- **Audit-time**: a reader (C35 override surfacing, F43 RSI visibility, meta-metrics C46, or an operator)
  queries the actor-keyed union of bead history + event bus.
- **Verify-time**: `chain_verify(from_seq, to_seq)` recomputes hashes over the stored chain entries and
  confirms they match. This is always available (not optional-pack-gated); it is the tamper-evidence
  mechanism that does NOT require signing. If verification fails → E-C41-05/E-C41-06.
- **Verify-time (optional signing)**: if the verification pack is installed, a verifier checks the
  provenance signature against the claimed actor (`actor-claimed == actor-signed`) and rejects/flags a
  mismatch. Absent the pack, this step is skipped and attribution is self-asserted (G36; D-14).

### 5.1 Sequence diagram: C23 event_ids → C41 chain append → verify

```mermaid
sequenceDiagram
    participant C23 as C23 Event Bus
    participant C41 as C41 Hash-Chain
    participant Auditor

    C23->>C41: event_id_stream(from_seq=last_seen) [gap-free ordered EventRecords]
    C41->>C41: compute payload_digest over {event_ids, created_by values}
    C41->>C41: compute entry_hash = SHA-256({seq, prev_hash, event_ids, payload_digest})
    C41->>C41: append ChainEntry to chain store (append-only)
    C41-->>C23: ack(last_event_id consumed)

    Note over C41: chain entry is now durable

    Auditor->>C41: chain_verify(from_seq=0, to_seq=N)
    C41->>C41: re-derive entry_hash for each entry; check prev_hash linkage
    alt all hashes match
        C41-->>Auditor: VerifyResult{ok=true}
    else hash mismatch at seq K
        C41-->>Auditor: VerifyResult{ok=false, first_mismatch_seq=K, error=E-C41-05}
    end
```

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C41 (faithful) |
|---|---|---|
| **F14** Attribution collapse (F-MODE §2, "Addressed") | The core mode C41 prevents: actions losing their actor. | **Addressed conditional on OQ-C41-3** at sweep-2 by the universal-attribution invariant (§3): every bead/event carries a `created_by` resolving to a valid actor; an unattributed write is invalid. This is v4's "strongest principle match" (README:231). *Caveat (RC41A-03):* the "unattributed write is invalid" guarantee is firm only if Gas City *rejects* (not merely *defaults*) an unattributed write — an unverified G11-class assumption (OQ-C41-3). If the substrate only defaults the field, F14 is discipline-dependent, not enforced. Retire OQ-C41-3 (plan T7) before declaring F14 unconditionally Addressed. |
| **F32** Mail-injection / unsigned coordination (F-MODE §2 + §7) | Unsigned inter-agent mail can be spoofed; the guard is "optional HMAC signing." | **Addressed-on-paper-only** in the faithful reading: C41 defines the provenance-verification *seam* the HMAC layer attaches at (§3.5, §4.5), but the signing is **optional** (G36). *Fidelity divergence (RC41A-02):* F-MODE-COVERAGE §2/§7 marks F32 **"Addressed"**, but that status is **not faithfully supportable** under C41's optional-signing reading — an optional guard "does not address a security failure" (G36). Per canonical-track rule 3 this divergence is recorded (not silently resolved) and routed to C57 (F-mode owner) as a residual-risk flag; the architecture stays optional. The mail bus itself is C06; C41 supplies the actor identity the signature binds. Signing is deferred to FE-3 per D-14. Residual risk flagged below + §9. |
| **F43** RSI Board-Visibility Gap (F-MODE §6, "Partial") | Need an audit trail to see what self-modifying components did. | **Partially addressed**: C41's actor-keyed audit trail (event bus + bead history, §4.3) is exactly the "P9 attribution + audit trail + bead history" mechanism. The hash-chain (§4.2, D-5) adds tamper evidence to the audit trail: a `chain_verify` failure proves the event stream was tampered. The *declaration discipline* (pack-author declares RSI status in `pack.toml`) is operator-required and out of C41's scope. |
| **G36** Attribution integrity is optional/deferred (minor) | Without signed provenance, `created_by` is self-asserted; F32's guard is "optional," which "does not address a security failure." | See the AMBIGUITY block below. Faithful resolution: C41 **defines** the verification seam and **requires** universal *self-asserted* attribution, but does **not require** verification (v4 marks it deferred; signing deferred to FE-3 per D-14, blocked on G37). The gap is acknowledged + surfaced as residual risk, not closed. |

> [AMBIGUITY: G36] **Is signed provenance required for attribution to be load-bearing, or genuinely
> optional?**
> Reading A (faithful-literal — optional): README:229 explicitly lists Identity verification as
> "**optional, deferred**" with placement "Optional pack," and F32's guard is "**optional** HMAC signing"
> (F-MODE §2). On this reading C41 must NOT require signatures; attribution is self-asserted and that is
> the intended v4 posture. The whole P9 section's claim to "strongest match" rests on `created_by`
> *presence*, not *verification*.
> Reading B (security-consistent — should be required): the Skeptic's G36 finding (minor) argues an
> *optional* guard "does not address a security failure" — F32 is marked **Addressed** on the strength of
> a guard that may not be installed. On a self-modifying factory (F43/RSI), self-asserted attribution lets
> a compromised or drifting actor forge `created_by`. A truly load-bearing audit trail would require
> verification.
> **Pick: Reading A for the *requirement*, with Reading B surfaced as named residual risk.** Canonical-track
> faithfulness is binding: v4 says "optional, deferred" in plain words (README:229), so C41 **cannot make
> verification mandatory** without an architectural change (out of scope for the canonical track). The smallest faithful
> choice is to (1) require *self-asserted* universal attribution (which v4 does mandate — "every action
> carries identity"), (2) fully **specify the verification seam** so the optional pack can be added without
> rework, and (3) record the "self-asserted by default" invariant (§3) and the F32/F43 residual risk
> (§7, §9) so no downstream component over-trusts attribution. Making verification *mandatory* is exactly
> the kind of improvement parked as a deferred enhancement (graduated-mandatory signing = **FE-3**,
> blocked on G37 per D-14: "G37 = open secrets/credential-storage gap (owned by C03; plaintext
> `city.toml`/env today). FE-3 = graduated-mandatory signing, BLOCKED ON G37 but a distinct deferred
> enhancement. Specs deferring secrets cite **G37**, not FE-3. Signing stays deferred (Bet 2 → FE-3),
> revisit at FE-3's trigger."); on the canonical track it is an open question routed to
> review-log (OQ-C41-1), not a decision C41 may take.
> **[AMBIGUITY resolution — D-5, chain ownership only]** Independent of the optional/mandatory question
> above, the integrator's ruling **D-5** settles *where* any tamper-evident provenance hash-chain lives:
> **C41 owns the provenance hash-chain**, computed over **C23-provided ordered gap-free `event_id`s** — C23
> provides the ordered ids only, never the chain. So the (optional, deferred) provenance-verification seam
> in §3.5 is C41's; if/when the chain is built, it is a C41-owned structure over C23 records, not a C23
> feature. This does not make verification mandatory on the canonical track — it only fixes the ownership boundary.

### 6.1 Error taxonomy (E-codes)

| Code | Name | Detection | Handling |
|---|---|---|---|
| **E-C41-01** | **Unattributed write** — bead/event written without `created_by` | stamp-time check; C19/C20 required-field validation (R=required on envelope) | reject the write (or flag if Gas City defaults rather than rejects — G11-gated; OQ-C41-3). Signals F14. |
| **E-C41-02** | **Unresolvable attribution** — `created_by` present but does not resolve to a valid actor (e.g., unknown rig name) | resolve_actor call returns error | reject or quarantine the record; alert auditor. Signals actor-kind-closure invariant violation. |
| **E-C41-03** | **Unknown actor kind** — `created_by` prefix not in {city, rig, agent, tool} | resolve_actor kind check | reject; actor-kind set is closed (§3 invariant). |
| **E-C41-04** | **Malformed actor reference** — `created_by` string does not parse as `kind:id` | resolve_actor parse | reject the write; the writer must supply a well-formed reference. |
| **E-C41-05** | **Hash mismatch** — chain_verify recomputes entry_hash and finds it differs from stored `entry_hash` | chain_verify per-entry recompute | return VerifyResult{ok=false, first_mismatch_seq=K}; signal tamper evidence to auditor; do NOT silently pass. This is the core tamper-detection signal. |
| **E-C41-06** | **Chain gap** — event_id sequence in a chain entry has a gap (missing `event_id` values relative to the previous entry's last id) | chain_append input validation; chain_verify gap scan | reject the chain_append (C23 must provide gap-free stream per §3.6); signal tamper evidence on verify. |
| **E-C41-07** | **Missing chain entry** — chain_verify requested seq range contains an absent entry | chain_verify seq scan | return VerifyResult{ok=false, error=E-C41-07}; signal tamper/data loss. |
| **E-C41-08** | **C23 stream out-of-order** — event_ids from C23 arrive non-monotonically | chain_append input validation | reject the batch; C23 is required to provide strictly ascending event_ids (§3.6 seam contract). |

> **Signing-deferred note.** No E-code covers signing failures because signing is deferred to FE-3 per
> D-14 (blocked on G37). The seam (§3.5 / C41-I4) names where a signing-failure E-code would attach;
> it is not defined here. C41 does not cite FE-3 as the signing mechanism — it cites **G37** as the
> blocker, per D-14.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** Attribution is **self-asserted by default** (README:229; G36).
  C41 guarantees *presence and well-formedness* of `created_by`, not its *truth*. This is sufficient for
  F14 (an action cannot be unattributed) but **not** for adversarial integrity (a malicious actor can
  claim another's identity absent the optional signature). The hash-chain (§4.2, D-5) provides tamper
  evidence for the *ordering and completeness* of the event stream without requiring signing; it does not
  prove who wrote each event. The seam for closing the identity claim — signed bead provenance / HMAC
  mail signing — is defined (§4.5) but unbuilt by default; signing is blocked on G37 (key storage gap,
  D-14). This residual risk is the load-bearing caveat on P9's "strongest match" claim and is surfaced
  to F-mode coverage (F32, F43) and the review-log (§9).
- **Cost.** Self-asserted attribution is *free* — it is a stamped field on writes that already happen
  (README:231 "without configuration"). The hash-chain adds one SHA-256 computation per C23 flush batch
  plus an append to the chain store — negligible compared to the LLM calls it records. The optional
  verification pack adds signing/verify cost (key management + per-action signature); v4 defers it, so
  the default-path marginal cost is the chain append only.
- **Scale.** No new instance store beyond the chain store (§4.4), which is append-only and grows at one
  entry per C23 flush. The audit trail is a *view* over C19/C23, which carry their own scale story.
  C41 adds no scale concern beyond keeping the actor-kind set closed and small.
- **Observability.** Attribution *is* observability's foundation — the `created_by`-keyed audit trail is
  what makes "who did what, when" answerable (README:222 "Foundation for debug, compliance, trust"). The
  hash-chain makes the *completeness* of that record verifiable. C41's invariants are what let C35
  (override surfacing), C46 (meta-metrics), and F43 (RSI visibility) attribute behavior to actors.
- **Ops.** The actor registry is sourced from `city.toml` `[[rig]]`/`[[agent]]` blocks (AI-CONTEXT §3.4,
  §13.3) under normal git review; C41 adds no separate operational surface. The chain store requires a
  backup/durability strategy consistent with C19 (same Dolt push cadence or file-sync). Enabling
  verification later is a pack install at the defined seam (§4.5) — additive, not a migration. *Caveat
  (RC41A-06):* the "additive later" property is **contingent on G37 (secrets/credential handling) being
  resolved first** — per D-14, signing is blocked on G37. The cheap-seam claim should not be oversold
  while G37 is open.

## 8. Acceptance criteria & test strategy

1. **Universal attribution (F14 closed)**: every bead write (C19/C20) and event emit (C23) produces a
   record with a non-empty `created_by`; a write path that omits it is rejected/invalid. No unattributed
   action exists.
2. **Actor resolvability**: every `created_by` resolves to a (kind, identifier) under the C41 actor model,
   with kind ∈ {city, rig, agent, tool}; an unknown-kind actor is invalid.
3. **Audit trail answerable by actor**: given an actor X, the union of bead history (C19) + event-bus
   records (C23) keyed by `created_by == X` returns X's actions; given a bead/event Y, its creating actor
   is recoverable (README:228).
4. **Append-only integrity**: attribution records in the audit trail are never rewritten (C23
   append-only; bead history immutable-by-convention) — a test attempting to alter a past `created_by`
   must not silently succeed.
5. **Verification seam present (optional path)**: with the optional verification pack installed, a
   signature over (actor reference + action content) is attachable and a verifier rejects a forged
   `created_by` (`actor-claimed ≠ actor-signed`); **without** the pack, this test is N/A and attribution
   is self-asserted (faithful to README:229). The *default* acceptance run does NOT require verification.
6. **Self-asserted caveat is explicit**: downstream components that read attribution (C35, C42, C46,
   F43 consumers) can discover whether the current install verifies provenance, so they do not over-trust
   a self-asserted `created_by`.

### 8.1 Concrete acceptance tests (AC-codes)

**Actor model (E-C41-03 / E-C41-04)**
- **AC-C41-1** — `resolve_actor("rig:worker-1")` → `{kind="rig", id="worker-1"}` without error; `resolve_actor("tool:inspect_eval")` → `{kind="tool", id="inspect_eval"}` without error (INT-4); `resolve_actor("unknown:foo")` → E-C41-03; `resolve_actor("bad_format")` → E-C41-04.
- **AC-C41-2** — Writing a bead with `created_by=""` or `created_by=null` → E-C41-01 (unattributed write rejected or flagged — enforcement strength is G11-gated; OQ-C41-3).

**Universal attribution (F14)**
- **AC-C41-3** — For every bead/event emitted by a running factory instance, `created_by` is present, non-empty, and resolves via `resolve_actor` without error. Zero unattributed records in a normal run.
- **AC-C41-4** — Audit trail: `audit_trail(actor=rig:worker-1)` returns a stream that contains every bead/event the `worker-1` rig wrote in the test run; `audit_trail_by_id` on any returned record resolves back to `rig:worker-1`.

**Provenance hash-chain: D-5 contract (chain over C23 event_ids, not C41's own ordering)**
- **AC-C41-5** — `chain_append` is called with event_ids sourced exclusively from the C23 `event_id_stream` (gap-free ordered); a chain built from C41-internal re-ordering of events (not using C23's sequence) is REJECTED. This confirms D-5: the chain consumes C23 event_ids, not its own ordering.
- **AC-C41-6** — After appending N entries covering event_ids 1..K, `chain_verify(0, N-1)` returns `ok=true`. Mutate the `payload_digest` of entry at seq=M, re-run `chain_verify(0, N-1)` → `ok=false, first_mismatch_seq=M` (E-C41-05). This is the tamper-detection test.
- **AC-C41-7** — Provide a batch with a gap (event_ids [1,2,4,5] skipping 3) to `chain_append` → E-C41-06 (chain gap rejected). Chain integrity is maintained.
- **AC-C41-8** — `chain_verify` on a seq range where entry seq=K is missing → E-C41-07 (missing chain entry).
- **AC-C41-9** — Out-of-order event_ids from C23 stream (e.g. [3,1,2]) to `chain_append` → E-C41-08 (stream out-of-order rejected).

**Append-only integrity**
- **AC-C41-10** — Attempt to overwrite/delete a chain entry → operation fails; the chain store is append-only. A `chain_verify` run after the attempted mutation still returns `ok=true` (the mutation had no effect).

**Signing deferred (D-14)**
- **AC-C41-11** — Default build (no optional pack): no signing failure E-codes are raised; attribution is self-asserted and `chain_verify` is the only tamper-evidence check. The test confirms the signing seam is *named* (§3.5) but NOT exercised on the default path.

## 9. Open questions

- **OQ-C41-1** (→ review-log): **Should provenance verification be mandatory? (G36).** v4 says
  "optional, deferred" (README:229), so canonical-track C41 leaves it optional and defines the seam (§6 AMBIGUITY).
  But the Skeptic's G36 finding argues an optional guard does not address F32/F43 on a self-modifying
  factory. This is the **top open question**: it is the load-bearing security decision and is precisely the
  deferred-enhancement candidate (graduated-mandatory signing = **FE-3**, blocked on G37 per D-14 — make signing mandatory at the F32/F43 surface). The canonical track cannot decide it
  without an architectural change; route to review-log for the integrator.
- **OQ-C41-2** (→ review-log): **Is the human operator a fourth actor kind?** v4 names only city/rig/agent
  (README:226), yet operator *overrides* are first-class actions (README P8 override-log row, README:214
  "beads with type `override`") and must be attributed. The
  faithful fill (§4.1) models the operator as acting *through* an agent/rig. Confirm against C42 (which
  partitions worker/scenario/judge roles — none of which is obviously "operator") whether a distinct
  `operator`/`human` actor kind is needed, or whether operator overrides are attributed to an agent acting
  on the operator's behalf.
- **OQ-C41-3** (→ review-log): **Does Gas City actually enforce universal `created_by`, or is it
  convention?** README/AI-CONTEXT assert attribution is "automatic everywhere," but Gas City's real
  behavior is asserted-not-run (G11-class). Confirm whether the substrate *rejects* an unattributed write
  or merely defaults the field — this determines whether the F14 invariant is enforced or
  discipline-dependent (and bears on OQ-C41-1).
- **OQ-C41-4** (→ review-log, **RESOLVED by D-29**): RESOLVED by D-29 — common wire type is the `"kind:id"` string; `ActorRef` is the parsed form. The colon-delimited `"kind:id"` string (e.g. `"rig:worker-1"`) is the canonical wire encoding in C19/C20/C21/C23; C41's `resolve_actor` parses it into `ActorRef{kind, id}`. All stores use the same actor-reference shape, so the audit-trail union in §4.3 keys cleanly across both.
- **OQ-C41-5** (→ review-log): **C23 event_id_stream seam contract — flush granularity and sequence semantics.** D-5 says C23 provides gap-free ordered event_ids; the exact flush trigger (time-based, count-based, or bead-write-based), the `event_id` sequence numbering scheme (is it C23's own monotonic sequence or a substrate sequence?), and the handshake/ack protocol between C23 and C41 must be frozen jointly before C41's chain implementation proceeds. This seam freeze is the first build action (plan §4 M0).
