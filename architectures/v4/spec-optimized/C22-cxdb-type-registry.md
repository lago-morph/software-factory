# C22 — CXDB type registry & viewpoint tagging  (Spec, Track B)

> Source: AI-CONTEXT §5.3 (the "turn" model: `{bundle_id, type, version}` per payload, type registry of JSON bundles like `mycompany.agents.v1` with `mycompany:DeployEvent` schemas, `registry/` storage layout), §5.1 (CXDB composition includes a "type registry" component), §5.5 (type-aware projection: "UI can render typed payloads structurally"); README Part 4 P9 (attribution), Part 4 P8 override/fix_task bead types, AI-CONTEXT §16 cold-start (`gc bd find --type factory_build_in_progress`); _meta component-inventory C22 row (depends C21; gap G17; foundational); _meta gaps G17 (assigned, blocker). F-MODE-COVERAGE: F50 (architecture/spec confusion in typed objects → "CXDB type registry enforces viewpoint separation").
> Inventory ID: C22   Kind: data-store (schema/registry)   Status: sweep-1
> Deltas: DELTA-01 (define the concrete v4 type bundle — provisionally `strongdm.factory.v4` — so cold-start works — the direct G17 resolution, not deferred. **⚠ COLLISION (review-log XC-4): the literal bundle-id conflicts with C22-A `softwarefactory.v4`, C21-B `softwarefactory.trajectory.v1`, and especially C20-B `v4.beads.v1` — and DELTA-04 below registers the SAME bead types (`fix_task`/`override`/…) that C20-B DELTA-07 independently binds to `v4.beads.v1`, so the bead-payload round-trip fails until one namespace is ruled canonical. Also `strongdm.` is the upstream *vendor's* reverse-DNS — pinning the factory's own bundle there is lock-in. The literal value is PROVISIONAL pending the integrator's canonical-namespace ruling.**), DELTA-02 (viewpoint promoted from a free tag to a closed enum that is a *first-class registry-enforced field* on every bundle entry, with a typed-object validation rule — the F50 mechanism v4 only names), DELTA-03 (registry is **append-only + version-monotonic**; types are never mutated in place, only superseded by a higher `version`, giving replay/counterfactual determinism), DELTA-04 (single source of truth for both bead types *and* CXDB payload types — one registry, two namespaces — so the bead-type vocabulary in AI-CONTEXT §16 stops being undefined. **⚠ COUPLING + CROSS-TRACK CONTRADICTION: this inverts the inventory's C20→C21 dependency by routing bead cold-start through CXDB's `registry/`, coupling the Phase-0 bead work-graph's queryability to the Phase-1 CXDB process being up; and it contradicts C20-B, which keeps its OWN bead-type schemas and only *binds* to a CXDB bundle (C20-B DELTA-07). RESOLUTION: the registry-of-record for bead types stays with C20 (Phase-0, no CXDB dependency); C22 MAY import/mirror the bead-type vocabulary for projection, but bead cold-start MUST NOT require the CXDB process. Integrator must reconcile with C20-B.**), DELTA-05 (schema discipline: every registered type carries a machine-checkable JSON Schema, not just a name, so "type-aware projection" and ingest validation are real, not aspirational).

## 1. Purpose & responsibility

C22 is **the type registry**: the authoritative catalog that gives every persisted object in the factory a stable, versioned identity `{bundle_id, type, version}` and a **viewpoint** tag, plus the JSON Schema that defines that type's payload shape. It is the component that turns CXDB's "dynamic type system" (AI-CONTEXT §5.3) and the scattered bead-type names (`override`, `fix_task`, `factory_build_in_progress`, `factory_build` — README Part 4, AI-CONTEXT §16) from prose into a single registered, queryable, validatable artifact. Concretely C22 owns:

1. **The bundle/type/version namespace** — the registered set of `{bundle_id, type, version}` triples and their JSON Schemas, stored in CXDB's `registry/` layout (AI-CONTEXT §5.3).
2. **Viewpoint tagging** — every registered type declares a `viewpoint` from a closed enum (`architecture | spec | trajectory | telemetry | control`). This is the mechanism F50 ("architecture/spec confusion in typed objects") is marked **Addressed** by; v4 names it but never defines it (DELTA-02).
3. **The concrete v4 bundle `strongdm.factory.v4`** — the actual list of types the factory ships with, so a cold agent running `gc bd find --type factory_build_in_progress` (AI-CONTEXT §16) hits a defined type, not a void (DELTA-01, G17).
4. **Validation services** — given a payload + claimed type, answer "does this conform to the registered schema, and is its viewpoint legal in this context?" This is what C21's ingest path and the UI projection (AI-CONTEXT §5.5) call.
5. **Version resolution** — resolve a type reference (with or without explicit version) to a concrete registered schema; enforce append-only/version-monotonic evolution (DELTA-03).

What C22 is **NOT**:
- **Not** the trajectory store itself — turn storage, BLAKE3 content-addressing, the turn-DAG, O(1) branching, and the ingest HTTP/binary APIs are **C21**. C22 is the *type layer C21 consults*; it owns `registry/`, not `turns.log`/`blobs.pack`.
- **Not** the bead *store* — the bead work-graph (C19) and its persistence are separate; C22 owns the bead-type *vocabulary* (the `type=` field's legal values and schemas), C19 owns the bead records.
- **Not** the bead generic *schema* (C20) — C20 defines the common bead envelope (id, status, created_by, edges); C22 defines the per-`type` payload schemas that ride inside it (DELTA-04: one registry serves both bead-type and CXDB-payload-type namespaces).
- **Not** the attribution stamp (C41) — C22 may register the `created_by`/`transfused_from` *fields'* schema, but the stamping mechanism is C41.
- **Not** a general-purpose schema registry service for arbitrary external systems — its scope is the factory's own types. (Contrast Confluent-style registries.)

## 2. Context & dependencies

- **Depends on (declared in inventory):**
  - **C21** (CXDB trajectory store) — C22's `registry/` lives inside the CXDB storage layout (AI-CONTEXT §5.3 lists `registry/` alongside `turns.log`, `blobs.pack`). C22 is the *type-system half* of CXDB; C21 is the *storage/DAG half*. They are co-located in the same Rust server process (AI-CONTEXT §5.1 lists "type registry" as a CXDB composition element) but are distinct components for diffability.
- **Consumed by (directly):**
  - **C21 ingest path** — validates `{bundle_id,type,version}` on every binary/HTTP append (AI-CONTEXT §5.2); a payload with an unregistered type or a schema-violating body is rejected at the seam.
  - **C19/C20** (bead work-graph + schema) — bead `type` values are C22-registered; `gc bd find --type X` (AI-CONTEXT §16) resolves `X` against C22.
  - **C24** (telemetry→CXDB bridge) — stamps the right `{bundle_id,type,version}` on bridged turns; reads C22 to know the telemetry-viewpoint types.
  - **C37/C38/C49** (clustering, diagnosis, counterfactual-replay) — read typed payloads by viewpoint; C49's replay determinism depends on version-pinned types (DELTA-03).
  - **CXDB UI** (AI-CONTEXT §5.5) — type-aware structural projection reads C22 schemas to render payloads.
- **Sits at:** Persistence & Memory subsystem, the *vocabulary/schema* foundation. Foundational (inventory Batch 1): everything that reads/writes typed persisted objects references C22.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, JSON Schemas, and the wire format in sweep 2).

**Inbound (what C22 offers):**
- `Register(bundle_id, type, version, json_schema, viewpoint) → {ok | conflict}` — add a new type version. **Append-only**: fails if `{bundle_id,type,version}` already exists with a different schema (DELTA-03); a changed schema requires a bumped `version`.
- `Resolve(bundle_id, type, version?) → RegisteredType` — return the schema + viewpoint for a triple. **Read/replay paths resolve against the version the payload was *written under* (the turn already carries `{bundle_id,type,version}` — C21 stores it), NOT "latest"** — this is the safe default, since C49 replay and C37 clustering read historical turns whose correct schema is their original version (DELTA-03 determinism). `version?`-omitted resolve-latest is permitted **only on the live-write path**, never on replay (resolve-latest on a historical turn is a determinism footgun — see §6/OQ-1).
- `Validate(bundle_id, type, version, payload) → {valid | violations[]}` — schema-check a payload body against its registered type (DELTA-05).
- `CheckViewpoint(type_ref, expected_viewpoint) → {ok | mismatch}` — the F50 guard: assert a payload's declared viewpoint is the one the caller's context permits (DELTA-02).
- `List(bundle_id?, viewpoint?) → RegisteredType[]` — enumerate registered types, filterable by bundle and viewpoint (drives UI projection + cold-start discovery).

**Outbound (what C22 depends on):**
- C21's storage primitive for the `registry/` directory (read/write JSON bundle files); C22 does not own raw bytes-on-disk, it owns their content and lifecycle.

**Invariants (sweep-1 level; formalized sweep 2):**
- **I1 — Append-only/version-monotonic:** a registered `{bundle_id,type,version}` is immutable; evolution = new higher version. (Replay/counterfactual determinism — DELTA-03.)
- **I2 — Total typing:** every payload persisted via C21 carries a `{bundle_id,type,version}` that resolves in C22. No untyped writes (closes the G17 "type the schema never defines" hole).
- **I3 — Viewpoint enum (provisional, closing at sweep 2):** `viewpoint ∈ {architecture, spec, trajectory, telemetry, control}`; every registered type declares exactly one. (F50 mechanism — DELTA-02.) **Only `architecture`/`spec` are F50-motivated; the other three are inferred — the enum stays EXTENSIBLE until C24/C37/C38 confirm their payload classes (OQ-2), because closing a wrong enum is a breaking registry migration.**
- **I4 — Schema-present:** every registered type has a non-empty JSON Schema (DELTA-05).

## 4. Data model / state

C22 owns the **registry**, stored as JSON bundle files in CXDB's `registry/` (AI-CONTEXT §5.3 names the layout). One registry, two namespaces (DELTA-04): CXDB payload types and bead types.

**Bundle** (`registry/strongdm.factory.v4.json` and any imported bundles like the upstream `mycompany.agents.v1` example):
| Field | Meaning |
|---|---|
| `bundle_id` | reverse-DNS id, e.g. `strongdm.factory.v4` |
| `types[]` | the registered types in this bundle |

**RegisteredType** (one entry):
| Field | Meaning |
|---|---|
| `type` | namespaced name, e.g. `strongdm.factory:factory_build_in_progress` |
| `version` | integer, monotonic per (bundle,type) |
| `viewpoint` | closed enum (I3) |
| `schema` | JSON Schema for the payload body |
| `kind` | `bead` \| `payload` (namespace tag — DELTA-04) |
| `description` | human/agent-readable purpose |

**The concrete `strongdm.factory.v4` bundle (DELTA-01, the G17 resolution).** Initial registered types, derived from the type names v4 actually uses (README Part 4, AI-CONTEXT §16):

| type | kind | viewpoint | source citation |
|---|---|---|---|
| `factory_build_in_progress` | bead | control | AI-CONTEXT §16 cold-start query |
| `factory_build` | bead | control | AI-CONTEXT §16; README Part 6 phases |
| `fix_task` | bead | control | README Part 4 P8 ("diagnosis agent writes bead of type `fix_task`") |
| `override` | bead | control | README Part 4 P8 ("Gas City beads with type `override`") |
| `spec_artifact` | payload | spec | README Part 4 P1; ties to C08 spec-artifact — **see note** |
| `architecture_doc` | payload | architecture | F50 — the viewpoint that must not be confused with `spec` — **see note** |
| `trajectory_turn` | payload | trajectory | AI-CONTEXT §5.3 turn model |
| `telemetry_event` | payload | telemetry | AI-CONTEXT §5.4 bridge (C24) |
| `anomaly` | payload | telemetry | README Part 4 P11 anomaly detection (C36) |
| `diagnosis` | payload | control | README Part 4 P11 Healer (C38) |

> This table is the **G17-resolving artifact**: it is the concrete `{bundle_id, type, version}` bundle the gap demanded. Sweep 2 fills each row's JSON Schema; sweep 1 fixes the namespace, viewpoints, and kinds.
>
> **NOTE on `spec_artifact` / `architecture_doc`:** the spec artifact is C08's git-versioned Markdown source-of-truth, not a CXDB trajectory payload; v4's model keeps specs as git artifacts, not CXDB turns. These two rows must be justified by an *actual* stored CXDB payload class (e.g. a reference/pointer turn into the spec) or reduced to viewpoint-tags-on-references rather than full payload types. Resolve with C08 at sweep 2 — they currently exist mainly to give F50 a concrete architecture-vs-spec pair, which is not sufficient grounds to assert specs flow through CXDB.

**Lifecycle:** bundles are loaded at CXDB startup from `registry/`; `Register` appends (never mutates — I1); a bundle export is a git-committable JSON artifact (cold-start reproducibility).

## 5. Behavior

Key flows (sequence/state diagrams in sweep 2):

1. **Cold-start type resolution.** Agent runs `gc bd find --type factory_build_in_progress` → C19 query → resolves `factory_build_in_progress` against C22's `strongdm.factory.v4` bundle → returns matching beads. Previously (v4 as written) this type was undefined; DELTA-01 makes it resolve.
2. **Ingest validation (tiered — cost-bounded).** C21 receives an append with `{bundle_id,type,version,payload}`. On the hot path it does only **cheap structural checks** (triple resolves in C22; required envelope fields present) so the p50<1ms append budget (AI-CONTEXT §5.5) is preserved. **Deep JSON-Schema body validation** of high-volume trajectory turns (whole raw-API-body payloads from C24) is NOT mandatory inline — it is sampled / async / or restricted to low-volume control-plane types (beads, judge verdicts). On a structural-check failure, reject at the seam (I2). Exact tier policy + per-class cost budget is a sweep-2 freeze.
3. **Viewpoint guard (F50).** A consumer that expects spec-viewpoint objects calls `CheckViewpoint(type_ref, spec)`; an `architecture_doc` (viewpoint=architecture) tagged where a `spec_artifact` is expected → `mismatch`, preventing the architecture/spec confusion F50 names (DELTA-02).
4. **Type evolution.** Author bumps a payload schema → `Register(...,version=N+1,...)` → old version N stays resolvable for replay of historical turns (I1, DELTA-03).

## 6. Failure modes & handling

| F-mode / failure | Detection | Mitigation / handling |
|---|---|---|
| **F50** (architecture/spec confusion in typed objects) | `CheckViewpoint` mismatch | Closed viewpoint enum + registry-enforced per-type viewpoint; reject mis-viewpointed writes (DELTA-02). This is the concrete mechanism F50 is marked Addressed by. |
| **Unregistered type write** (G17 hole) | `Resolve` miss on ingest | Reject append (I2); surfaces a clear "type not registered" error instead of silent untyped storage. |
| **Schema drift / in-place mutation** | `Register` conflict (same triple, different schema) | Append-only invariant (I1); force a version bump. Protects C49 replay determinism. |
| **Implicit-latest non-determinism** | n/a (design risk) | `Resolve` with omitted version returns latest **and flags it**; replay/counterfactual paths (C49) MUST pin version. Documented as open question OQ-1. |
| **Bundle file corruption** | startup schema-validate of `registry/*.json` | Fail-closed at CXDB boot; registry is a small git-committed artifact, restore from VCS. |

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** registry is the type-authority; write access to `Register` is privileged (only authoring/bootstrap flows). Viewpoint tagging is also a containment boundary (an architecture doc cannot masquerade as a shippable spec).
- **Cost/scale:** registry is small (tens–hundreds of types), in-memory after load; validation cost is per-append JSON Schema check — bounded, on C21's hot ingest path, so schemas must stay cheap (sweep 2: compile schemas at load).
- **Observability:** `List` by viewpoint gives a live catalog; the UI's type-aware projection (AI-CONTEXT §5.5) is a direct consumer.
- **Ops:** the `strongdm.factory.v4` bundle is a versioned, git-committed JSON file — cold-start reproducible; adding a type is a registry append + commit, not a code change.

## 8. Acceptance criteria & test strategy

(Concrete test cases in sweep 2.) The component is correct when:
- **AC1 (G17):** the `strongdm.factory.v4` bundle exists and every type name v4 uses in prose (`factory_build_in_progress`, `factory_build`, `fix_task`, `override`) resolves via `Resolve`. Test: `gc bd find --type factory_build_in_progress` returns without "unknown type."
- **AC2 (I2):** an append with an unregistered type is rejected by C21's ingest; an append with a schema-violating payload is rejected.
- **AC3 (F50/DELTA-02):** `CheckViewpoint` flags an `architecture`-viewpoint object presented where a `spec`-viewpoint is required.
- **AC4 (I1/DELTA-03):** re-registering an existing `{bundle_id,type,version}` with a changed schema fails; registering it at `version+1` succeeds and leaves the old version resolvable.
- **AC5 (DELTA-05):** every registered type returns a non-empty JSON Schema from `Resolve`.

## 9. Open questions

- **OQ-1 (→ review-log):** Should `Resolve` without an explicit version be **forbidden** on replay/counterfactual paths (C49) rather than merely flagged? Pinning everywhere is safest for determinism but burdens every caller; "latest" is ergonomic for live writes. Proposed split: live writes may omit version (resolve-latest), replay paths MUST pin. Needs C49's confirmation.
- **OQ-2 (→ review-log):** Is the viewpoint enum (`architecture | spec | trajectory | telemetry | control`) complete? F50 only motivates the architecture↔spec split; the other three are inferred from the store's payload classes. C24/C37/C38 owners should confirm before the enum is frozen (changing a closed enum later is a breaking registry migration).
