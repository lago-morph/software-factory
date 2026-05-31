# C22 — CXDB type registry & viewpoint tagging  (Spec, Track A)

> Source: AI-CONTEXT §5.3 ("Event schema — the 'turn' model", lines 212–220: "Dynamic type system: `{bundle_id, type, version}` per payload"; "Type registry: JSON bundles like `mycompany.agents.v1` with `mycompany:DeployEvent` schemas"; "Storage layout: `turns.log`, `blobs.pack`, `registry/`"); AI-CONTEXT §5.1 (line 200: CXDB composition includes a "type registry"); AI-CONTEXT §5.5 (line 238: "Type-aware projection → … UI can render typed payloads structurally"); F-MODE-COVERAGE §2 F50 (line 36: "Architecture/spec confusion in typed objects → CXDB type registry with viewpoint tagging on bundles → Addressed"; line 149: "F50 … CXDB type registry enforces viewpoint separation"); component-inventory C22 row (maps `A21f`; depends on C21; gaps G17; foundational: yes; one-liner "Dynamic `{bundle_id,type,version}` type system; viewpoint tagging resolves architecture/spec confusion"); ambiguities-and-gaps G17 (blocker — "the v4-specific type bundle (`{bundle_id, type, version}`) that v4 must register is never specified").
> Inventory ID: C22   Kind: data-store   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C22 is the **type system of CXDB**: the registry that gives every content-addressed payload (C21) a
machine-checkable identity of the form `{bundle_id, type, version}`, the **bundle/schema definitions**
those identities resolve to, and the **viewpoint tag** that records *from which standpoint* a typed
payload is asserted (e.g. an architecture statement vs. a spec statement vs. an implementation event).
Where C21 owns the **turn-DAG + Blob CAS** (the bytes and their parent-chain), C22 owns **what those
bytes *mean*** — the JSON bundles in CXDB's `registry/` directory and the rules for tagging,
versioning, and resolving them.

This component exists because v4 instructs the factory to store *typed* trajectory payloads and to use
**viewpoint tagging** to prevent "architecture/spec confusion in typed objects" (F50), yet the
v4-specific type bundle is **never actually specified** (gap G17, blocker). CXDB ships a *generic*
dynamic type system (`mycompany.agents.v1` / `mycompany:DeployEvent` are illustrative examples, not v4
types); C22 is the place where v4 defines its *own* bundle(s), its *own* type set, and the viewpoint
convention F50 leans on.

**Responsibilities**
- Define the **type-identity triple** `{bundle_id, type, version}` carried by every CXDB payload
  (AI-CONTEXT §5.3) — its grammar, uniqueness rules, and how it indexes into `registry/`.
- Define the **bundle** unit: a JSON document (`<bundle_id>`, here `softwarefactory.v4.trajectory` — D-2)
  that declares a set of `type` schemas at a `version`, stored under CXDB's `registry/` (AI-CONTEXT §5.3 line 220).
- Define the **viewpoint tag** that F50 requires: an enumerated standpoint attached to a typed payload
  so that "architecture" assertions and "spec" assertions about the same subject are *separable* and do
  not collapse into one another (F-MODE-COVERAGE §2 F50, §11 line 149 "enforces viewpoint separation").
- Provide **type-aware projection** metadata so the CXDB UI/clients can render a typed payload
  structurally rather than as raw JSON (AI-CONTEXT §5.5 line 238).
- Define **versioning / evolution** rules so a type schema can change without breaking replay of
  already-stored payloads addressed under an older `version`.

**Explicitly NOT**
- NOT the trajectory **store** (C21). C21 owns turns, parent pointers, BLAKE3 Blob CAS, O(1) branching,
  and the binary/HTTP ingest APIs. C22 owns *type definitions, bundles, viewpoint tags, and resolution*
  that ride **inside** C21's payloads. C22 adds no new storage engine — it lives in C21's `registry/`.
- NOT the **bead** type registry (C20). C20 types nodes in the *work-graph* (`override`, `fix_task`,
  `factory_build_in_progress`, …); C22 types payloads in the *trajectory* store. They are parallel
  registries on different stores; v4 keeps these stores distinct (AI-CONTEXT §3.2 bead-store vs §5 CXDB).
  > [FAITHFUL-FILL] v4 never states the C20↔C22 relationship. Treating them as **separate, parallel**
  > registries is the minimal consistent reading: v4 describes two distinct stores (bead work-graph in
  > §3.2, CXDB trajectory store in §5) with two distinct type vocabularies, and never unifies them.
- NOT the OTLP/telemetry schema (C25/C26). CXDB has "no native OTLP receiver" (AI-CONTEXT §5.2); typed
  CXDB payloads arrive via the bridge (C24), already shaped, and are typed *here*, not in OTel space.
- NOT a runtime authorization or policy engine. C22 says what a payload *is*; it does not decide who may
  write it (that is C41 identity/attribution + C42/C43 partitioning).

## 2. Context & dependencies

**Depends on**
- **C21 (CXDB trajectory store)** — C22 is C21's `registry/` and the type layer over C21's payloads.
  C22 cannot exist without the Blob CAS + turn model it annotates. (component-inventory: C22 depends on C21.)

**Consumed by (downstream readers of types/viewpoints)**
- **C24 (telemetry→CXDB bridge)** — must stamp each posted payload with a `{bundle_id, type, version}`
  and a viewpoint when it ingests raw API bodies (AI-CONTEXT §5.4; G26 seam).
- **C37 (trajectory clustering)** / **C36 (anomaly detection)** / **C38 (diagnosis)** — read typed,
  viewpoint-tagged payloads so embedding/clustering operates over *meaningfully typed* trajectories
  rather than raw JSON (AI-CONTEXT §5.5 "type-aware projection").
- **C49 (counterfactual replay)** — branches CXDB turns (O(1) fork, AI-CONTEXT §5.3); replay must
  resolve historical payloads against the *version* they were written under.
- **CXDB UI / browser** (part of C21's React frontend, AI-CONTEXT §5.1) — renders typed payloads
  structurally via projection metadata.

**Where it sits.** Persistence & Memory subsystem; the type/semantics layer of CXDB, foundational
(Batch 1 in the inventory build order). It is small in surface but load-bearing: every downstream
consumer that reads CXDB *by type* depends on this registry being defined.

## 3. Interfaces / contracts

Sweep-1: interfaces are **named and described**; signatures are deferred to sweep 2.

**Inbound (write/define side)**
- **`register_bundle`** — install or update a JSON bundle under `registry/`. Input: a bundle document
  (`bundle_id`, `version`, a map of `type` → schema, viewpoint declarations). Establishes the schemas
  that subsequent payloads may claim. (AI-CONTEXT §5.3 "Type registry: JSON bundles … with … schemas".)
- **`tag_payload`** — the contract a writer (C24, event bus, Go client) satisfies when it appends a
  payload to CXDB: it MUST attach a `{bundle_id, type, version}` triple and a `viewpoint` value. The
  payload bytes are then BLAKE3-addressed by C21 as usual. C22's role here is the **validation
  precondition**: the triple must resolve to a registered schema, and the payload must conform.

**Outbound (read/resolve side)**
- **`resolve_type`** — given a `{bundle_id, type, version}`, return the schema (for validation and for
  type-aware projection). Used by the UI and by typed consumers.
- **`project`** — given a typed payload, return the structured view metadata so a client renders it by
  field rather than as opaque JSON (AI-CONTEXT §5.5).
- **`filter_by_viewpoint`** — given a query, restrict results to one viewpoint (or assert separation)
  so "architecture" and "spec" assertions about the same subject never silently merge (F50).

**Invariants / pre/postconditions**
- **I1 (resolvability).** Every stored payload's `{bundle_id, type, version}` MUST resolve to a schema
  present in `registry/`. A payload claiming an unregistered triple is rejected at `tag_payload`.
- **I2 (immutability of versions).** A published `{bundle_id, type, version}` schema is **immutable**;
  evolving a type means publishing a new `version`, never mutating the old one — so payloads addressed
  under the old version still resolve. (Consistent with C21's content-addressed, append-only model:
  AI-CONTEXT §5.3 "no Postgres/Redis/Kafka", append-only `turns.log`.)
  > [FAITHFUL-FILL] v4 states the triple includes a `version` but never states version immutability.
  > Immutability is the minimal choice consistent with CXDB being content-addressed and append-only
  > (§5.3/§5.5 "tamper-evidence"); a mutable schema would silently break replay of older turns, which
  > contradicts the replay guarantee that is CXDB's reason to exist (§5.5).
- **I3 (viewpoint totality).** Every typed payload carries exactly one viewpoint; "untagged" is not a
  legal state, because F50's separation guarantee fails if some payloads are viewpoint-less.
  > [FAITHFUL-FILL] v4 (F50) says viewpoint tagging exists but does not say it is mandatory. Making it
  > total is the *minimal choice that lets the F50 "Addressed" claim hold* — an optional tag cannot
  > *enforce* separation, the same defect G36 flags for optional attribution. **Caveat:** mandatory-on-
  > write changes the ingest contract for every writer (C24, event bus, Go clients). Whether totality is
  > *enforced at write time* (hard-reject untagged writes) vs *audited after the fact* is a Track-B / C57
  > detect-vs-prevent decision (see OQ1); a faithful builder must NOT hard-reject untagged writes without
  > the integrator's sign-off, or it will break any legacy/untyped ingest path.

## 4. Data model / state

**Owned state** lives entirely inside CXDB's `registry/` directory (AI-CONTEXT §5.3 line 220) — C22
introduces no new store.

- **Type-identity triple** (per payload, stored alongside the payload in the turn record):
  - `bundle_id` — namespace of the owning bundle (v4's own bundle, see below).
  - `type` — the type name within the bundle (CXDB example form `mycompany:DeployEvent`; for v4,
    `softwarefactory.v4.trajectory:<TypeName>` — D-2).
  - `version` — the bundle/schema version this payload was written against.
  - `viewpoint` — the standpoint tag (see below). *(F50 — the v4-specific addition over stock CXDB.)*

- **Bundle** (JSON document in `registry/`):
  - `bundle_id` (`softwarefactory.v4.trajectory` — D-2; analogous to CXDB's `mycompany.agents.v1`).
  - `version`.
  - `types`: map of `type` name → JSON schema (field shapes for projection + validation).
  - `viewpoints`: the enumerated set of legal viewpoint values this bundle uses.

- **Viewpoint enumeration.** v4 names the *problem* (architecture/spec confusion, F50) but not the
  enumerated values. Minimal faithful set, drawn directly from the failure F50 describes:
  - `architecture` — an assertion about how the system *is structured*.
  - `spec` — an assertion about what the system is *required to do* (the load-bearing source-of-truth, C08).
  - `implementation` — an assertion about what *ran* (the default for ingested trajectory/event payloads).
  > [FAITHFUL-FILL] The 3-value set is inferred. F50's title is literally "Architecture/spec confusion
  > in typed objects", so `architecture` and `spec` are mandated by the failure name; `implementation`
  > is the minimal third value needed because the *bulk* of CXDB payloads are runtime trajectory turns
  > (AI-CONTEXT §5.3) which are neither architecture nor spec assertions. Kept to three to avoid
  > inventing taxonomy v4 does not state; a downstream bundle may add viewpoints under its own version.
  > **Cross-track note:** the optimized track (C22-B) widens this to a five-value enum
  > (`architecture | spec | trajectory | telemetry | control`). The canonical enum is an integrator
  > decision — a closed enum is a breaking registry migration to change later (C22-B OQ2 raises the same).

**The v4 bundle.** G17 (blocker) is that *the v4-specific bundle is never specified*. Faithfully, C22's
deliverable is exactly that bundle: a single v4 bundle that registers the payload
types the rest of v4 stores in CXDB (trajectory turns, raw-body conversation payloads, and any typed
projections the Healer/clustering tier reads). Sweep-1 fixes its **existence and shape**; the
concrete per-type schemas are a sweep-2 deliverable (they depend on C24's payload shapes and C37's
projection needs).
> [AMBIGUITY: XC-4 — RESOLVED by D-2] The bundle's *existence* is faithfully forced (reading (b) below);
> its literal *id string* was not v4-stated. The integrator's canonical-namespace ruling (review-log **D-2**)
> settles it: one factory-owned reverse-DNS root with per-store sub-bundles — `softwarefactory.v4.beads`
> (C20 bead types), `softwarefactory.v4.trajectory` (C22 CXDB turn/trajectory types), `softwarefactory.v4.packs`
> (C02 pack ids). The earlier candidates (`softwarefactory.v4`, `strongdm.factory.v4`, `softwarefactory.trajectory.v1`,
> `v4.beads.v1`) and vendor `strongdm.*` are dropped. C22's CXDB-payload bundle is therefore
> **`softwarefactory.v4.trajectory`**.
> [AMBIGUITY: G17] v4 gives two readings of "the type bundle". (a) CXDB's generic registry is *enough*
> and v4 needs no bundle of its own (the `mycompany.*` examples are the whole story). (b) v4 must
> **register its own** bundle for its payloads to be typed/resolvable at all. Reading (b) is forced by
> the rest of v4: F50 is marked **Addressed** *on the strength of* viewpoint tagging on v4 bundles
> (F-MODE-COVERAGE §2), and §5.5 promises type-aware projection of v4 payloads — both require a
> registered v4 bundle. So C22 adopts (b): define one `softwarefactory.v4.trajectory` bundle (D-2).
> Reading (a) is rejected because it leaves F50 unaddressed and §5.5 unfulfillable.

**Lifecycle.** Bundles are append-only/versioned (I2). Registering a new bundle version is additive;
old versions remain to keep historical turns resolvable for replay (C49) and audit.

## 5. Behavior

**Write path (tag-on-ingest).** A writer (C24 bridge, event bus, or Go client) constructs a payload,
selects the `{bundle_id, type, version}` and `viewpoint`, and submits via C21's ingest. C22's
validation gate checks I1 (triple resolves) and conformance; on success C21 BLAKE3-addresses and
appends the turn; on failure the write is rejected with a typed error (see §6).

**Read/projection path.** A reader fetches a turn, reads its triple, calls `resolve_type` to get the
schema, and `project` to render it structurally (AI-CONTEXT §5.5). A viewpoint-scoped query uses
`filter_by_viewpoint` so the UI can show, e.g., only `spec`-viewpoint assertions about a subject — the
mechanism by which F50 "enforces viewpoint separation".

**Viewpoint separation (the F50 flow).** Two payloads may describe the *same* subject (say, component
C30) — one from the `architecture` viewpoint, one from the `spec` viewpoint. Because each carries a
distinct viewpoint tag, a consumer can never mistake the architectural assertion for the spec
requirement; queries that omit a viewpoint filter return both, *labelled*, rather than a merged,
ambiguous object. That labelling **is** the addressing of F50.

Sequence/state diagrams and the concrete validation algorithm are deferred to sweep 2/3 per the brief.

## 6. Failure modes & handling

**Primary F-mode owned: F50 — "Architecture/spec confusion in typed objects."** C22 is the *named
mechanism* for F50 (F-MODE-COVERAGE §2 line 36, §11 line 149). Addressing: mandatory viewpoint tag
(I3) + `filter_by_viewpoint` keeps architecture and spec assertions separable. **Faithful caveat:** v4
marks F50 **Addressed**, but the mechanism is *tagging + query discipline*, not enforcement that a
writer chooses the *correct* viewpoint — a writer can still mis-tag a spec assertion as architecture.
This is the same detect-vs-prevent gap pattern the Skeptic flags elsewhere (G21/G36); recorded as an
open question, not resolved, since Track A may not redesign.

**Other handling**
- **Unregistered/invalid type (I1 violation).** Reject at write with a typed error; never silently
  store an un-resolvable payload (which would corrupt downstream typed projection and clustering).
- **Schema evolution (I2).** Never mutate a published version; publish a new `version`. Old turns keep
  resolving — preserves C21 replay (C49) and tamper-evidence (§5.5).
- **Missing viewpoint (I3 violation).** Reject; "untagged" is not legal.
- **Registry unavailable / payload references a version not yet replicated.** Faithfully undefined by
  v4 (part of G33 — no partial-failure story for the OSS stack). Deferred with reason: Track A cannot
  invent a replication/degradation design v4 does not state; noted as open question.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** Tamper-evidence rides on C21's BLAKE3 addressing (§5.5); immutable versioned schemas
  (I2) mean a type definition cannot be retroactively altered to re-interpret stored payloads. C22 does
  *not* authenticate writers — actor attribution is C41's job.
- **Scale.** Resolution is a lookup into `registry/` (file-backed, no DB — §5.3). Type-aware projection
  adds no storage cost; the triple + viewpoint are small per-payload metadata. Consistent with CXDB's
  perf contract (p50 <1ms append, §5.5) — C22 adds a bounded validation lookup on the write path.
- **Observability.** C22 is itself a precondition for meaningful observability: clustering/anomaly/
  diagnosis (C36–C38) operate over *typed* payloads; without C22 they see raw JSON.
- **Ops.** Bundles are JSON files under `registry/` — version-controllable, diffable, no migration tool
  needed for additive evolution.

## 8. Acceptance criteria & test strategy

Sweep-1 (high-level; concrete tests at sweep 2):
- **AC1.** The `softwarefactory.v4.trajectory` bundle (D-2) is defined and registrable under CXDB `registry/`,
  closing G17 for the CXDB type side: the previously-undefined v4 type bundle now exists. *(G17)*
- **AC2.** Every payload carries a resolvable `{bundle_id, type, version}` (I1); a write claiming an
  unregistered triple is rejected.
- **AC3.** Every payload carries exactly one viewpoint from the bundle's enumeration (I3); an untagged
  write is rejected.
- **AC4.** Two payloads describing the same subject under `architecture` vs `spec` viewpoints are
  independently retrievable and never merge under a viewpoint-omitting query — demonstrating F50
  separation. *(F50)*
- **AC5.** Publishing a new schema `version` does not break resolution/projection of payloads stored
  under the prior version (I2) — replay-safety for C49.
- **AC6.** A typed payload renders structurally via `project` (AI-CONTEXT §5.5), not as opaque JSON.

## 9. Open questions

- **OQ1 (→ review-log).** F50 is marked **Addressed**, but C22's mechanism is *tagging + query
  separation*, not enforcement that the *correct* viewpoint is chosen at write time. Is detect-and-label
  sufficient to call F50 "Addressed", or does it share the detect-vs-prevent weakness of G21/G36? Track
  A flags; resolution belongs to Track B / the residual-risk register (C57).
- **OQ2 (→ RESOLVED by D-3).** C20 (bead type registry) and C22 (CXDB type registry) are parallel
  registries on two stores; this faithful reading is upheld. The integrator's ruling **D-3** confirms
  the ownership split: **C20 authors the bead-type payload schemas**; **C22 owns the registration
  *mechanism* + the CXDB-turn/trajectory types only** and registers C20's bead types via a documented
  binding seam (C22 does not author bead schemas). The optimized track's earlier "one registry" framing
  (C22-B DELTA-04) is reconciled to this seam. Bead namespace `softwarefactory.v4.beads`; CXDB-turn
  namespace `softwarefactory.v4.trajectory` (D-2).
- **OQ3.** The concrete per-`type` schemas in `softwarefactory.v4.trajectory` depend on C24's raw-body
  payload shape (G26) and C37's projection needs; pinned at sweep 2 once those seams are fixed.
