# C20 — Bead schema registry  (Spec, Track B)

> Source: component-inventory.md C20 row (maps A90 `override`, A91 `fix_task`, A92 `factory_build_in_progress`, A58b loop-closure, B37-schema); README Part 4 P8 (`override` beads, l.214), P10 (bead store, l.239–242), P11 (`fix_task` l.257, loop-closure l.259), Part 6 Phase-3b ("Fix-task bead schema" l.463, "Loop closure tracking pack" l.464); AI-CONTEXT §5.3 (`{bundle_id,type,version}` type model l.218–219), §7 Layer-4 (loop-closure "bead schema" l.334), §16 cold-agent recovery (`gc bd find --type factory_build_in_progress`, `transfused_from`, `gc converge resume` l.694–699), §13.2 (`[beads] provider="file"` l.538); _meta gaps G17 (no schema for any core store — **blocker**), G18 (self-heal loop has no termination/closure contract — **blocker**); F-MODE-COVERAGE F52 ("more controller patches" / oscillation).
> Inventory ID: C20   Kind: data-store (schema registry)   Status: sweep-1
> Deltas: DELTA-01 (versioned bead-type registry as a first-class artifact, not folklore), DELTA-02 (`factory_build` / `factory_build_in_progress` modeled as one type + lifecycle state, not two types), DELTA-03 (closed bead-type catalog resolving G17 with the exact v4-referenced types), DELTA-04 (loop-closure contract: bounded fix-attempt chain with `attempt_no`/`escalated` — resolves G18 at the schema layer), DELTA-05 (every bead carries `created_by` actor + `transfused_from` provenance as schema-required, not convention), DELTA-06 (schema-version migration + validation gate at write time), DELTA-07 (bead-type ↔ CXDB type-bundle binding so a bead's payload is replayable in C21/C22).

## 1. Purpose & responsibility

C20 is the **canonical, versioned schema registry for every bead type** in v4. C19 owns the *generic* typed work-graph (nodes, edges, dependencies, persistence in file/Dolt); C20 owns **what the typed payloads of those nodes actually are** — the field-level contract for each `type` value a v4 bead can carry, the enum of legal types, the per-type lifecycle/state machine, the required attribution/provenance fields, and the schema version each instance was written under.

C20 exists because **G17 is a blocker**: the v4 corpus *names* bead types (`override`, `fix_task`, `factory_build_in_progress`, `factory_build`) and even tells a cold agent to query one (`gc bd find --type factory_build_in_progress`, AI-CONTEXT §16) — but **no document defines a single field of any of them**. Until C20 resolves this, the override loop (C35), self-heal loop (C39), and bootstrap-resume (C50/§16) have no payload to write or read. C20's job is to publish that catalog as a concrete, versioned artifact.

C20 owns:
- The **closed enum of v4 bead types** and, per type, its field schema, required vs optional fields, and value constraints (DELTA-03).
- The **per-type lifecycle** (which states a bead of that type may occupy and the legal transitions), most critically the **bounded fix-attempt chain** that gives the self-heal loop a termination contract (DELTA-04, resolves G18 at the schema layer).
- The **common bead envelope** every bead shares regardless of type: `id`, `type`, `schema_version`, `created_by` actor, `created_at`, dependency edges (delegated to C19's graph), and `transfused_from` provenance (DELTA-05).
- The **schema-version + migration policy** and the **write-time validation gate** that rejects beads not conforming to a registered schema (DELTA-06).
- The **bead-type → CXDB type-bundle mapping** (`{bundle_id, type, version}`) so a bead's payload is registerable/replayable in C21/C22 (DELTA-07).

What it is **NOT**:
- **Not the bead store.** C19 owns storage, the dependency graph, query (`gc bd`), and the file-vs-Dolt provider. C20 is pure schema/contract that C19 enforces at write time.
- **Not the self-heal control loop.** C39 *runs* the loop and decides when to escalate; C20 only supplies the **schema fields that make termination expressible and auditable** (`attempt_no`, `max_attempts`, `escalated`, `closes` edge). The *policy values* (e.g. max-attempts default) are C39/C18's to set; C20 reserves the fields and the invariant.
- **Not the override control loop.** C35 detects overrides and runs the "why" prompt; C20 defines the `override` bead it writes.
- **Not the CXDB type registry.** C22 owns the dynamic `{bundle_id,type,version}` runtime registry for *trajectory turns*. C20 owns *bead* schemas and merely **binds** each bead type to a CXDB bundle so payloads cross the seam (DELTA-07). Two registries, one mapping.
- **Not identity/attribution.** C41 defines the actor model; C20 requires the `created_by` field and points it at C41's actor type.

## 2. Context & dependencies

- **Depends on:**
  - **C19** (bead store / typed work-graph) — C20's schemas are enforced *by* C19's writer; dependency edges referenced in C20 lifecycles (`closes`, `caused_by`) are C19 graph edges.
  - **C41** (identity/actor model) — supplies the `Actor` type that `created_by` references (DELTA-05).
  - **C22 / C21** (CXDB type registry + trajectory store) — receives the bead-type→bundle binding (DELTA-07); soft dependency (a bead is valid even if CXDB is absent in a Phase-0 install).
- **Consumed by (fan-out):**
  - **C35** override→pattern→rule loop — writes/reads `override` beads.
  - **C39** fix-task generation & loop-closure — writes `fix_task` beads, walks the closure chain; C20's DELTA-04 fields are this component's termination substrate (shared gap G18).
  - **C50 / bootstrap-resume & AI-CONTEXT §16** — `factory_build_in_progress` query + `transfused_from` + `gc converge resume` all read C20 fields.
  - **C51** gene-transfusion discipline — `transfused_from` provenance field is C20-defined, C51-populated.
  - **C41** audit trail — reads the common envelope's attribution fields.
- **Sits at:** the Persistence & Memory subsystem, immediately above C19 (schema layer over the storage layer). Foundational (Batch 1) — a blocker for three downstream control loops, so it must freeze its catalog + envelope early.

## 3. Interfaces / contracts

Named-and-described (sweep 1; full field-by-field JSON Schema / msgpack shapes in sweep 2).

**Inbound (what C20 offers writers/readers via C19):**
- `BeadTypeCatalog` — the closed registry: `type_id → { schema_version, json_schema_ref, lifecycle_ref, cxdb_bundle_binding, required_envelope_fields }`. The single source of truth for "what types exist and what shape each is."
- `validate(bead) → ValidationReport` — the **write-time gate** (DELTA-06): checks envelope completeness, type ∈ catalog, payload conforms to the registered schema for `(type, schema_version)`, lifecycle state legal, and (for `fix_task`) the loop-closure invariant. Fail-closed: a non-conforming bead is rejected by C19's writer, not silently stored.
- `migrate(bead, target_version) → bead'` — applies the registered up-migration for a type whose schema has advanced (DELTA-06).

**Outbound:**
- `CXDBTypeBinding` — per bead type, the `{bundle_id, type, version}` triple to register in C22 so the bead's payload turn is replayable in C21 (DELTA-07).
- `SchemaChangeEvent` — emitted to C23 when a new schema version is registered (auditability of the catalog itself).

**Invariants:**
- **Closed catalog:** a bead whose `type` ∉ `BeadTypeCatalog` cannot be written (no anonymous types — this is what makes `gc bd find --type X` well-defined, resolving the G17 §16 dangling-query problem).
- **Envelope completeness:** every bead has non-null `id`, `type`, `schema_version`, `created_by`, `created_at` (DELTA-05). Attribution is structural, not optional.
- **Version pinning:** every instance records the `schema_version` it was written under; readers resolve fields through that version's schema, never the latest implicitly.
- **Loop-closure boundedness (DELTA-04, resolves G18):** within one anomaly's fix chain, `attempt_no` is strictly increasing and `attempt_no ≤ max_attempts`; a chain either reaches a terminal `resolved` bead (via a `closes` edge proving the originating anomaly cleared) or an `escalated=true` bead. An unbounded/oscillating chain is *unrepresentable* — you cannot write attempt N+1 once `escalated` or once `max_attempts` is hit without an explicit human/escalation actor in `created_by`.
- **Single build identity (DELTA-02):** `factory_build_in_progress` and `factory_build` are the **same bead** at two `lifecycle_state` values, so the `gc converge resume` flow (§16) operates on one stable `id` across its whole life.

## 4. Data model / state

### 4.1 Common bead envelope (every type)

| Field | Req | Notes |
|---|---|---|
| `id` | yes | C19 node id (stable across lifecycle transitions). |
| `type` | yes | ∈ closed catalog (§4.2). |
| `schema_version` | yes | semver of the *type's* schema this instance was written under (DELTA-06). |
| `created_by` | yes | C41 `Actor` (city / rig / agent / human) (DELTA-05). |
| `created_at` | yes | RFC3339. |
| `lifecycle_state` | yes | ∈ the type's lifecycle (§4.3). |
| `transfused_from` | cond | required for factory-built beads (C51); external exemplar provenance (§16, DELTA-05). |
| `deps` | — | dependency edges — owned by C19's graph, not duplicated here. |

### 4.2 Closed bead-type catalog (DELTA-03 — the G17 resolution)

The v4-referenced types, made concrete. This is the **versioned schema delta** the brief requires.

| `type` | schema v | Source | Purpose | Type-specific fields (sweep-2 finalizes value constraints) |
|---|---|---|---|---|
| `override` | 1.0.0 | README P8 l.214; A90 | Durable record of an operator override + the "why". | `tool_call_ref`, `hook` (`PreToolUse`/`PostToolUse`), `why` (operator text), `proposed_rule_id?` (link to a derived validation rule, C35) |
| `fix_task` | 1.0.0 | README P11 l.257; A91, A58 | Diagnosis output written as an actionable fix. | `caused_by` (→ anomaly bead/event), `diagnosis_ref` (CXDB trajectory), `attempt_no`, `max_attempts`, `escalated` (bool), `closes?` (→ the anomaly it resolved) — the DELTA-04 closure fields live here |
| `factory_build` | 1.0.0 | A92; §16; README Phase-3 | A factory-built component's lifecycle bead (incl. the in-progress state). | `component_id` (C-ID), `spec_ref` (`packs/*/spec.md`), `scenarios_ref` (`scenarios/<component>/`), `transfused_from` (req), `resume_token?` (for `gc converge resume`) |
| `factory_build_in_progress` | — | §16 query l.695 | **Not a distinct type (DELTA-02)** — it is `factory_build` with `lifecycle_state = in_progress`. The `gc bd find --type factory_build_in_progress` query is **redefined** as `--type factory_build --state in_progress` (see Open Questions OQ1 for the compatibility shim). |

> [DELTA-02] **v4 said:** AI-CONTEXT §16 names `factory_build_in_progress` as a queryable *type* and the inventory lists it alongside `factory_build` as if both are types. **Change:** model one `factory_build` type with a lifecycle state `in_progress`. **Rationale (simplicity + operability):** a component's identity must be stable across its whole build so `transfused_from`, `spec_ref`, and `resume_token` don't have to migrate between two bead ids when it finishes; two types would force a copy-and-relink at completion and break the single-`id` resume contract. **Tradeoff:** the literal `--type factory_build_in_progress` query string in §16 no longer resolves to a type and needs the OQ1 shim.

### 4.3 Per-type lifecycle (state machines — Mermaid in sweep-2)

- `override`: `logged → (pattern_surfaced) → rule_proposed → rule_adopted | dismissed`. (Feeds C35's override→rule loop.)
- `factory_build`: `queued → in_progress → built → human_review → deployed | rejected`. (`in_progress` is the §16 resume target; `human_review` is the README Phase-2/3 "deploy if it works" gate.)
- `fix_task` (DELTA-04, the G18 contract): `open → attempting → (verifying) → resolved | retry | escalated`.
  - `retry` re-enters `attempting` **only** while `attempt_no < max_attempts`.
  - Reaching `max_attempts` without a `closes` edge forces `escalated` (terminal; requires a human/escalation actor in `created_by` to proceed further).
  - `resolved` requires a `closes` edge to the originating anomaly bead — this is the **loop-closure proof** ("did the fix actually fix it?", README l.259 / B37).

> [DELTA-04] **v4 said:** loop-closure is "Custom bead chain: anomaly → diagnosis → fix → resolution" with "no stated bound" — G18 flags this as the exact F52 "more controller patches" oscillation trap. **Change:** make the bound a *schema invariant*: `attempt_no`/`max_attempts`/`escalated`/`closes` on `fix_task`, with the lifecycle forbidding attempt N+1 past `max_attempts` and requiring a `closes` edge for `resolved`. **Rationale (failure):** termination/non-oscillation should be unrepresentable-to-violate at the data layer, not merely hoped-for in the controller; an auditor can prove a loop closed or escalated by reading beads alone. **Tradeoff:** C20 reserves loop-control fields that are *policy-set* by C39/C18 (C20 owns the fields + the monotonicity invariant; the default `max_attempts` value is C39's), creating a deliberate shared-ownership seam (flagged OQ2).

### 4.4 Schema versioning & storage

- **Versioning:** each `type` carries an independent semver `schema_version`; instances pin the version they were written under (DELTA-06). Up-migrations are registered functions; reads of old instances either resolve through the old schema or are lazily migrated.
- **Persistence:** schemas themselves are version-controlled artifacts (JSON Schema files) shipped in a Gas City pack and loaded by C19's writer; bead *instances* live in C19's provider (file or Dolt, AI-CONTEXT §13.2). C20 adds no separate datastore.
- **CXDB binding (DELTA-07):** each bead type maps to a CXDB `{bundle_id, type, version}` (e.g. bundle `v4.beads.v1`, type `v4:fix_task`, version `1.0.0`) registered in C22, so a bead payload can be a replayable turn in C21.

## 5. Behavior

- **Write path:** writer (C35/C39/bootstrap) constructs a bead → C19 calls C20 `validate` → on pass, stored + (if CXDB present) payload registered/forwarded under its `CXDBTypeBinding`; on fail, rejected with `ValidationReport` (fail-closed).
- **Cold-agent recovery (§16) path:** `gc bd find --type factory_build --state in_progress` → read `transfused_from`, `spec_ref`, `scenarios_ref`, `resume_token` from the envelope/payload → `gc converge resume <id>`. C20 guarantees these fields exist on every such bead (DELTA-03/05), which is precisely what §16 assumes but never specified.
- **Self-heal closure path:** C39 walks `caused_by`/`closes` edges; C20's invariants guarantee the chain terminates in `resolved` (with proof) or `escalated` (with a human actor) — giving C39 a decidable "is this loop closed?" predicate (G18).
- **Schema evolution path:** registering a new `schema_version` emits `SchemaChangeEvent` to C23; old instances remain readable via version pinning + `migrate`.

## 6. Failure modes & handling

- **G17 (no schema — blocker, RESOLVED):** the closed catalog §4.2 + common envelope §4.1 define every v4-referenced type concretely; `gc bd find --type X` is now well-defined for all X in the catalog. Residual: types not yet referenced in v4 must be *added to the catalog* (closed-enum requires explicit registration, by design).
- **G18 (no loop termination — blocker, RESOLVED at schema layer):** DELTA-04 makes unbounded/oscillating fix chains unrepresentable; *policy* (default `max_attempts`, escalation routing) is C39/C18's, flagged OQ2.
- **F52 (controller-patch oscillation):** the `max_attempts`+`escalated` invariant is the direct guard — the Healer cannot endlessly emit fix beads for the same anomaly without crossing into a terminal `escalated` state that demands a human actor.
- **Schema drift / silent field-shape change:** version pinning + write-time validation + `SchemaChangeEvent` make any catalog change auditable and prevent old/new readers from silently disagreeing (DELTA-06).
- **Unattributed action (audit gap):** envelope requires `created_by`; a bead with no actor cannot be written (DELTA-05), protecting C41's audit trail and P9.
- **Cross-store payload divergence:** the CXDB binding (DELTA-07) keeps the bead schema and the trajectory-turn schema in one declared mapping rather than two drifting definitions.

## 7. Cross-cutting

- **Security/governance:** mandatory `created_by` + `transfused_from` make every bead attributable and provenance-bearing (P9, C41, C51 license/exemplar handling).
- **Cost/scale:** schemas are static artifacts; validation is O(fields) at write; no runtime registry lookups on read (version pinned in-instance). No new datastore.
- **Observability:** catalog + lifecycles make beads queryable and the self-heal loop auditable end-to-end; `SchemaChangeEvent` puts schema evolution itself on the event bus.
- **Operability:** one stable bead id per factory-built component (DELTA-02) makes `gc converge resume` robust across the build's whole life.

## 8. Acceptance criteria & test strategy

1. **Catalog completeness (G17):** every type named anywhere in the v4 corpus (`override`, `fix_task`, `factory_build`, and the §16 `factory_build_in_progress` query) resolves to a registered schema or to the DELTA-02 state mapping. No dangling type.
2. **Write-time fail-closed:** a bead with an unknown `type`, a missing envelope field, or a payload violating its registered schema is rejected by C19's writer (golden negative tests).
3. **Loop-closure bound (G18/F52):** a `fix_task` chain cannot record `attempt_no > max_attempts` without `escalated=true`; `resolved` without a `closes` edge is rejected (property test over generated chains).
4. **Resume contract (§16):** a `factory_build`/`in_progress` bead always exposes `transfused_from`, `spec_ref`, `scenarios_ref`, `resume_token`; the §16 query (via the OQ1 shim) returns it.
5. **Version pinning:** a bead written under schema v1.0.0 reads correctly after v1.1.0 is registered (no implicit latest-schema resolution).
6. **CXDB binding round-trip:** a bead payload registered under its `{bundle_id,type,version}` is replayable as a C21 turn (integration test, when CXDB present).
7. **Attribution invariant:** no bead is writable without a valid C41 actor in `created_by`.

## 9. Open questions

- **OQ1 (→ review-log):** Compatibility shim for the literal `gc bd find --type factory_build_in_progress` query that AI-CONTEXT §16 hard-codes, given DELTA-02 folds it into `factory_build` + state. Options: (a) C19 query alias mapping the legacy type-string to `type=factory_build & state=in_progress`; (b) patch §16's documented command. Affects the cold-agent recovery UX. *Top open question.*
- **OQ2 (→ review-log):** Ownership seam for loop-control *policy*. C20 owns the `max_attempts`/`escalated` fields + monotonicity invariant; who sets the default `max_attempts` and the escalation-routing target — C39 (fix-loop), C18 (reconciler bounded gates), or C03 (config)? The schema reserves the field regardless, but the binding default must be assigned.
- **OQ3:** Should `override`, `fix_task`, `factory_build` share one CXDB `bundle_id` (`v4.beads.v1`) or get per-type bundles? Affects C22 registration granularity and independent versioning of each type's payload schema.
