# C20 — Bead schema registry  (Build Plan, Track B)

> Source / Spec ref: [C20 spec](../spec-optimized/C20-bead-schema.md)
> Track B, sweep 1. Deltas governed by the spec header (DELTA-01…07). Foundational / Batch-1 blocker for C35, C39, C50/§16, C51.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze the common bead envelope** (§4.1): fields, required-set, `created_by`→C41 actor binding, `transfused_from` provenance. Publish as the load-bearing contract. | S | C41 actor-type stub, C19 node-id shape |
| T2 | **Freeze the closed bead-type catalog enum** (§4.2): `override`, `fix_task`, `factory_build` (+ DELTA-02 state mapping). This is the G17 resolution surface every dependent waits on. | S | T1 |
| T3 | Author per-type JSON Schemas (field constraints, required/optional) for the three types. | M | T2 |
| T4 | Define per-type lifecycle state machines (§4.3), especially the `fix_task` bounded-attempt machine (DELTA-04 / G18). | M | T2 |
| T5 | Implement the **write-time validation gate** (`validate(bead)→ValidationReport`) wired into C19's writer; fail-closed. | M | T3, T4, C19 writer hook |
| T6 | Implement schema-version pinning + `migrate()` + `SchemaChangeEvent`→C23 (DELTA-06). | M | T3, C23 |
| T7 | Define the bead-type **CXDB type-bundle bindings** `{bundle_id,type,version}` in the canonical **`softwarefactory.v4.beads`** bundle (D-2) and register them via C22's seam (DELTA-07). C20 **authors** the bead schemas; C22 owns only the registration mechanism (D-3). | S | T2, C22 |
| T8 | Resolve OQ1 shim: legacy `--type factory_build_in_progress` → `type=factory_build & state=in_progress` query alias in C19 (or doc patch). | S | T2, T4, C19 query layer |
| T9 | Loop-closure invariant tests + resume-contract tests + attribution tests (acceptance §8). | M | T5, T8 |

## 2. Dependency graph

- **Upstream (must precede C20 freeze):** C19 (writer + query + node-id), C41 (actor type — can be a stub at T1), C22/C21 (only for T7, soft).
- **Critical path:** **T1 → T2 → {T3, T4} → T5 → T9.** T2 (the catalog enum + envelope) is the single point three downstream control loops block on — it must freeze first and earliest.
- **Downstream blocked on C20's T2 freeze:** C35 (override loop), C39 (fix-loop / G18), C50 + AI-CONTEXT §16 resume, C51 (gene-transfusion provenance).
- T6 (versioning), T7 (CXDB binding), T8 (query shim) hang off T2/T3 but are **not** on the path to first-dependent-unblock.

## 3. Parallelization

Once **T2 freezes** (envelope + enum), fan out independently:
- **Stream A:** T3 (JSON Schemas) ∥ T4 (lifecycles) — disjoint files per type.
- **Stream B:** T7 (CXDB bindings) — touches only C22 registration, no overlap with A.
- **Stream C:** T8 (query shim) — touches only C19 query layer.
- T3 itself fans out three ways (one schema file per bead type: `override`, `fix_task`, `factory_build`).
- Serialization points: T5 (validation gate) needs both A streams; T9 (acceptance) needs T5 + T8.

## 4. Interfaces-first / contract milestones

Freeze in this order so dependents build against stubs:
1. **M1 — Common envelope + closed type enum (T1+T2).** *Earliest, highest-leverage freeze.* Unblocks C35/C39/C50/C51 to start writing against named types. This is the G17-resolving milestone.
2. **M2 — `fix_task` closure-field contract (`attempt_no`/`max_attempts`/`escalated`/`closes`) + lifecycle (T4 subset).** Unblocks C39's G18 termination work; reserve fields even before C39 picks the default `max_attempts` (OQ2).
3. **M3 — `validate()` signature + `ValidationReport` shape (T5 contract).** Lets C19's writer integrate the gate against a stub.
4. **M4 — CXDB `{bundle_id,type,version}` bindings in `softwarefactory.v4.beads` (T7, D-2).** C20-authored bead schemas (D-3) that C22/C21 register via the C22 seam.

## 5. Risks & de-risking order

1. **DELTA-02 / §16 query compatibility (highest uncertainty):** spike T8 early — confirm C19's `gc bd find` supports a `--state` predicate (or an alias mechanism). If not, the resolution is a doc-patch to §16; decide before M1 advertises the type enum.
2. **G18 closure invariant expressibility:** prototype the `fix_task` property test (T9 subset) against the T4 state machine *before* C39 builds on it, to confirm "unbounded chain is unrepresentable" actually holds under C19's edge model.
3. **OQ2 ownership seam:** confirm with C39/C18/C03 who sets `max_attempts` default before T5 hard-codes any policy; C20 must ship the *field + invariant* only.
4. **CXDB-absent install (Phase 0):** verify beads validate and store with no CXDB present (T7 binding is soft); a Phase-0 `[beads] provider="file"` install must not require C21/C22.

## 6. Definition of done

- **Per-task:** each catalog type has a registered JSON Schema + lifecycle; `validate()` rejects every malformed case in the §8 golden negatives; the `fix_task` property test proves boundedness (no `attempt_no > max_attempts` without `escalated`; no `resolved` without `closes`).
- **Per-component (ties to spec §8):**
  1. G17 closed: every v4-named bead type resolves to a schema (or DELTA-02 state mapping); no dangling `gc bd find --type X`.
  2. G18 closed at schema layer: fix-chain termination is a write-time invariant, not a hope.
  3. §16 resume contract holds: in-progress factory-build beads always expose `transfused_from`/`spec_ref`/`scenarios_ref`/`resume_token`.
  4. Every bead is attributable (`created_by` required) and version-pinned (`schema_version` required).
  5. CXDB bindings round-trip when CXDB is present; beads still validate when it is absent.
- **Open questions** OQ1–OQ3 are mirrored to `_meta/review-log.md` (per [DOC-TEMPLATES](../_meta/DOC-TEMPLATES.md) §9), with OQ1 (the §16 query shim) flagged as the top item.
