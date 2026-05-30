# C22 — CXDB type registry & viewpoint tagging  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C22-cxdb-type-registry.md](../spec-optimized/C22-cxdb-type-registry.md)
> Track B, sweep 1. Foundational. Deltas referenced: DELTA-01…05 (see spec header).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prereqs by task id (and external C-IDs).

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Triple + RegisteredType schema** — freeze `{bundle_id, type, version}` identity and the `RegisteredType` record `{type, version:int, viewpoint, schema, kind, description}`; `version` is a per-(bundle,type) monotonic integer. Spec §4. | S | — |
| T2 | **Viewpoint enum freeze** — close the enum `architecture | spec | trajectory | telemetry | control` (invariant I3 / DELTA-02). Closing it is a breaking-migration-later decision, so resolve OQ-2 before this task lands. | S | — (gated on OQ-2 sign-off from C24/C37/C38) |
| T3 | **`registry/` storage layout + load** — read/write JSON bundle files in CXDB's `registry/` dir via C21's storage primitive; startup loader that schema-validates every `registry/*.json` and fails closed on corruption. Spec §4 lifecycle, §6 corruption row. | M | T1, **C21** (storage primitive) |
| T4 | **`Register` (append-only)** — add a `{bundle_id,type,version}` + schema + viewpoint; reject same-triple-different-schema (invariant I1 / DELTA-03); a changed schema requires a higher `version`. | M | T1, T2, T3 |
| T5 | **`Resolve`** — triple → `RegisteredType`; version-omitted returns highest registered version **and flags implicit-latest** (OQ-1). | S | T1, T3 |
| T6 | **`Validate`** — JSON-Schema-check a payload body against its registered type; return `violations[]` (DELTA-05). Schemas compiled at load for hot-path cost. | M | T1, T3, T5 |
| T7 | **`CheckViewpoint`** — the F50 guard: assert a payload's declared viewpoint matches the caller's expected viewpoint; `mismatch` on architecture-where-spec-expected (DELTA-02). | S | T2, T5 |
| T8 | **`List`** — enumerate registered types, filter by `bundle_id?` / `viewpoint?` (drives UI projection + cold-start discovery). | S | T1, T3 |
| T9 | **Author `softwarefactory.v4.trajectory` bundle + register C20's `softwarefactory.v4.beads` types (G17 resolution)** — C22 authors the CXDB-turn-type rows (`spec_artifact`, `architecture_doc`, `trajectory_turn`, `telemetry_event`, `anomaly`, `diagnosis`) in the canonical `softwarefactory.v4.trajectory` bundle (namespace, viewpoint, kind per row). The bead-type rows (`factory_build_in_progress`, `factory_build`, `fix_task`, `override`) are **authored by C20** (D-3) in `softwarefactory.v4.beads` and registered here via the documented binding seam — C22 does not author bead schemas. Sweep-1 freezes the rows; per-row JSON Schemas are sweep-2 content (bead schemas are C20-owned). | M | T1, T2, **C20** (supplies bead-type schemas via the registration seam) |
| T10 | **C21 ingest-path wiring** — C21's binary/HTTP append calls `Resolve`+`Validate`; reject unregistered/schema-violating writes at the seam (invariant I2). | M | T4, T5, T6, **C21** (ingest path) |

## 2. Dependency graph

- **Upstream (must precede C22 being *complete*):** **C21** — owns the CXDB storage primitive and the `registry/` directory's bytes-on-disk plus the ingest seam C22 plugs into (T3, T10). C22 is the type-system half of CXDB; C21 is the storage/DAG half, co-located in the same server process. The C21↔C22 storage and ingest-hook contracts are the only hard external blockers.
- **Adjacent (coordination, not blocking):** **C20** (bead schema registry) — C20 **authors the bead-type schemas** (D-3); C22 registers the bead-type→bundle bindings (`kind=bead` rows in §4) into `softwarefactory.v4.beads` via the documented seam. The bundle-id namespace is **RESOLVED by D-2**: bead payloads bind to `softwarefactory.v4.beads`, CXDB-turn types to `softwarefactory.v4.trajectory` (vendor `strongdm.*` and the earlier `v4.beads.v1` candidate are dropped). No naming seam left to reconcile.
- **Downstream (gated *by* C22):** C21 ingest validation, C19/C20 bead-type resolution (`gc bd find --type X`), C24 (telemetry-viewpoint typing), C37/C38/C49 (typed-by-viewpoint reads; C49 replay determinism needs version-pinned types), CXDB UI (type-aware projection).
- **Critical path inside C22:** T1 → T3 → T4 → T6 → T10. T2/T7 (viewpoint guard) and T9 (bundle authoring) hang off T1/T2 and are not on the longest path, but T9 is the **G17-resolving deliverable** and T2's enum-freeze gates both.
- **System critical-path note:** C22 is Batch-1 foundational and named on the inventory critical path (#1, with C21). Its **interface freeze** (§4) unblocks every component that reads/writes typed persisted objects, so the contract milestone matters more than full impl completion.

## 3. Parallelization

Explicit fan-out after the §4 interface freeze:

- **Stream A (storage + resolution core):** T1 → T3 → T4 → T5. The backbone; everything else joins here.
- **Stream B (validation):** T6 → T10. Joins A at T4/T5; T10 also needs C21's ingest path.
- **Stream C (viewpoint):** T2 → T7. Independent of A after T1, except T2's enum-freeze must clear OQ-2 first; pure tagging/guard logic.
- **Stream D (bundle content authoring):** T9 — authors the `softwarefactory.v4.trajectory` CXDB-turn rows against the T1 schema and registers C20's `softwarefactory.v4.beads` bead types via the seam; proceeds as soon as the triple/viewpoint/kind shape is frozen (namespace already settled by D-2). Does not block A/B/C.
- **Stream E (discovery):** T8 — small, hangs off T3; can land any time after the loader.

T1 is the single same-day unblocker. T2 (enum) and T9 (bundle) are the two streams that depend on *other components' input* (OQ-2 sign-off; C20's bead-type schemas via the registration seam), so they are the natural background/last-to-land work that must not stall the storage core.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs:

1. **`{bundle_id, type, version}` triple + `RegisteredType` record (T1)** — the single identity surface; freeze first. Every downstream typed read/write codes against this.
2. **`Resolve` + `Validate` signatures (T5, T6)** — so C21's ingest path can wire the reject-at-seam behavior against a stub returning fixed schemas.
3. **Closed viewpoint enum + `CheckViewpoint` (T2, T7)** — so C24/C37/C38 know the legal viewpoints before the enum is frozen (post-freeze changes are breaking registry migrations).
4. **`softwarefactory.v4.trajectory` bundle row-set (T9, sans schemas)** — so C19/C20 and cold-start (`gc bd find --type factory_build_in_progress`) resolve the type names immediately, even before per-row JSON Schemas land in sweep 2.
5. **Bead-type `bundle_id` is fixed by D-2** — bead payloads bind to `softwarefactory.v4.beads`; C20's `CXDBTypeBinding` (its DELTA-07) and C22's `kind=bead` registration rows both reference that one canonical bundle. No agreement step remains; just apply the adopted id on both sides.

Stub strategy: ship the triple schema + a hard-coded `softwarefactory.v4.trajectory` bundle (CXDB-turn names + viewpoints + kinds, schemas stubbed to `{}`) plus the `softwarefactory.v4.beads` registration slots for C20's bead types first; C21 ingest and C19 type-resolution validate against that while Streams A/B finish the real `Validate`.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **C20↔C22 bundle-id collision — RESOLVED by D-2/D-3 (XC-4).** The earlier disagreement (C20's `v4.beads.v1` vs C22's `strongdm.factory.v4`) is settled: **D-2** fixes the canonical namespace (`softwarefactory.v4.beads` for beads, `softwarefactory.v4.trajectory` for CXDB turns) and **D-3** assigns bead-schema authorship to C20 with C22 owning only the registration mechanism. No de-risking spike remains; the residual task is mechanical — **apply the adopted ids in T9** and wire C20's bead types through the registration seam so the round-trip (C20 AC6) passes. The only open sub-question is the sweep-2 granularity detail (one shared `softwarefactory.v4.beads` bundle vs per-type bundles), which is not a foundational blocker.
2. **OQ-2 — is the viewpoint enum complete?** F50 only motivates `architecture↔spec`; the other three (`trajectory|telemetry|control`) are inferred. Get C24/C37/C38 owners to confirm before T2 freezes the enum — re-opening a closed enum later is a breaking migration of `registry/`.
3. **OQ-1 — implicit-latest determinism.** `Resolve` with omitted version returns latest; C49 counterfactual replay needs version-pinned determinism. De-risk by shipping `Resolve` with the flag (T5) and deciding with C49 whether replay paths must hard-fail on unpinned references vs merely warn.
4. **C21 storage-primitive shape (G11-adjacent).** C22 assumes C21 exposes a read/write primitive for the `registry/` dir. Confirm that primitive exists in the real CXDB server before building T3 — a registry that can't durably persist its bundles is fail-closed-at-boot (spec §6).

## 6. Definition of done

Per-component (ties to spec §8 acceptance):

- **DoD-1 G17 resolved (AC1):** the `softwarefactory.v4.beads` bundle (bead types, C20-authored) and the `softwarefactory.v4.trajectory` bundle (CXDB turns) exist and every type v4 names in prose (`factory_build_in_progress`, `factory_build`, `fix_task`, `override`) resolves via `Resolve`; `gc bd find --type factory_build_in_progress` returns without "unknown type." [T9, T5]
- **DoD-2 Total typing (AC2/I2):** an append with an unregistered type is rejected by C21's ingest; an append with a schema-violating payload is rejected. [T6, T10]
- **DoD-3 Viewpoint guard (AC3/F50/DELTA-02):** `CheckViewpoint` flags an `architecture`-viewpoint object presented where a `spec`-viewpoint is required. [T7]
- **DoD-4 Append-only (AC4/I1/DELTA-03):** re-registering an existing `{bundle_id,type,version}` with a changed schema fails; registering at `version+1` succeeds and leaves the old version resolvable. [T4]
- **DoD-5 Schema-present (AC5/DELTA-05):** every registered type returns a non-empty JSON Schema from `Resolve` (sweep-2 schema content; sweep-1 freezes the requirement + stub gate). [T6, T9]
- **DoD-6 Fail-closed boot:** a corrupt `registry/*.json` fails CXDB boot rather than serving an invalid type-authority. [T3]
- **DoD-7 Bundle-id agreement:** the bead-type `bundle_id` is identical in the C20 and C22 specs and a bead payload round-trips through `Register`→`Resolve` under that one id. [T9, §5 risk 1]

Per-task DoD: each task lands with a unit test for its acceptance bullet above, written against the frozen §4 interfaces; no task is "done" until the contract it implements is unchanged from its freeze (or the change is propagated to all stub consumers).

Component is **done** when DoD-1…7 pass, the §4 contracts are frozen and consumed by at least one real downstream component (C21 ingest validation via `Validate` is the canonical integration check), and the C20↔C22 bundle-id seam (§5 risk 1) is reconciled in both specs.
