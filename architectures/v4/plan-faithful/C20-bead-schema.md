# C20 — Bead schema registry  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C20-bead-schema.md`](../spec/C20-bead-schema.md)
> Status: sweep-2. Binding: D-2 (bundle `softwarefactory.v4.beads`), D-3 (C20 authors schemas / C22 owns
> registration), D-4 (C20→C19), XC-3 (slots `attempt_no`/`max_attempts`/`escalated`/`closes` owned here,
> policy in C39). Sweep-2 deepens: the C22 registration task (T9), the XC-3 slot-name freeze, and the
> three seams to freeze first (C19 envelope, C22 `register_bundle`, C39 slot identifiers).

## 1. Work breakdown

Ordered tasks to build C20. Sizes: S (≤½ day), M (~1–2 days), L (multi-day).

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Common envelope schema.** Fix `id`, `type`, `created_by`, `dependencies`, `status` as the fields on every bead (spec §4.1). Decide `status` enum values. | S | C19 envelope shape known |
| T2 | **Named-type registry.** Define field schemas for the four v4-named types: `override`, `fix_task`, `factory_build`, `factory_build_in_progress` (spec §4.2). | M | T1 |
| T3 | **Chain-derived types.** Define `anomaly`, `diagnosis`, `resolution` (the closure-chain nodes the P11 chain implies; spec §4.2 FAITHFUL-FILL), pending OQ-C20-2 confirmation. | M | T1, OQ-C20-2 resolved |
| T4 | **Closure-chain shape + termination slots.** Encode the `anomaly→diagnosis→fix_task→resolution` edges + attempt-count / terminal-state / escalation-marker fields (spec §4.3, G18 slots). | M | T2, T3 |
| T5 | **Resume contract.** Pin the `factory_build_in_progress` fields (`transfused_from`, spec pointer, scenario pointer, workflow handle) sufficient for `gc converge resume <bead_id>` (spec §3 invariant, §8.3). | S | T2 |
| T6 | **Write-time validation rule.** Reject unregistered `type`; require envelope + per-type fields (spec §5, invariants). | M | T1–T4 |
| T7 | **Registry/store conformance + schema-version pin.** Ensure C19 store accepts exactly C20's types/fields; add a schema-version (AI-CONTEXT §3.5 drift risk; spec §4.4). | M | T6; C19 store contract |
| T8 | **Query smoke set.** Verify `gc bd find --type <T>` resolves for all four named types (G17 acceptance, spec §8.1 / AC-S2-G17). | S | T2, T6 |
| T9 | **C22 registration bundle (D-3 seam).** Emit the `softwarefactory.v4.beads` bundle document (spec §3.1) and install it via C22 `register_bundle`; assert namespace == D-2 string (AC-S2-R1/R2), no `viewpoints` key. | M | T2–T5; C22 `register_bundle` available |
| T10 | **XC-3 slot-name freeze.** Freeze the concrete identifiers `attempt_no`/`max_attempts`/`escalated` (on `fix_task`) + `closes`/`verdict` (on `resolution`) so C39 writes against them (spec §4.5.5; resolves C39 RC39-01). | S | T4 |

## 2. Dependency graph

```
C19 (bead store/work-graph)        ← hard upstream; provides node persistence + gc bd surface
        │
        ▼
       T1 ──▶ T2 ──▶ T5 ──▶ T9 (C22 register_bundle)
        │      │
        │      ├──▶ T6 ──▶ T7
        ▼      │              ▲
       T3 ──▶ T4 ──▶ T10 ────┘
                     │
                     └──▶ T8
```

- **Critical path**: C19 → T1 → T2 → T4 → T6 → T7. T7 (registry/store conformance) is the last gate
  because it requires the C19 store contract to be real, which is itself G11-blocked (Gas City behavior
  unverified).
- **External prerequisites**: C19 must expose its node/field contract before T1 can finalize the
  envelope. The C39 loop-closure policy (OQ-C20-1) and the type-boundary question (OQ-C20-2) gate T3/T4's
  *finalization* but not their first draft.

## 3. Parallelization

- **Parallel after T1**: T2 (named types) and T3 (chain-derived types) are independent field-schema work
  once the envelope is fixed — two workstreams.
- **T5 (resume contract)** runs concurrently with T3/T4 — it only needs T2's `factory_build*` types.
- **T8 (query smoke)** can be drafted as soon as T2 lands, in parallel with T6/T7 hardening.
- **T9 (C22 registration)** runs after the field schemas (T2–T5) stabilize, in parallel with T6/T7; it
  needs only the C22 `register_bundle` interface (Batch-1 co-foundational), not the full C19 store.
- **T10 (slot freeze)** is a fast follow on T4 and unblocks C39 (Batch-4) immediately — do it early so
  the downstream self-heal builder is never blocked on a C20 naming decision.
- **Cross-component**: C20 is a Batch-1 foundational schema authored in parallel with C19; the two teams
  must co-design the envelope (T1) so C19's store and C20's registry agree (spec §4.4). This is the one
  hard synchronization point.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents (C35, C39, C51, C52) can build against stubs. **Three external seams
must be frozen first** (they gate the rest): the **C19 envelope shape** (T1, the D-4 co-design point),
the **C22 `register_bundle` artifact shape** (T9 / spec §3.1, the D-3 seam), and the **C39 slot
identifiers** (T10 / XC-3 — already frozen this sweep at spec §4.5.5).

1. **Common envelope (T1)** — `id`/`type`/`created_by`/`dependencies`/`status` (+ the `status` enum
   `{open,in_progress,closed}`) — freeze first; C41 (`created_by`) and every downstream consumer reads it.
   This is the D-4 co-design point with C19 (M1 interface freeze breaks the write-path cycle).
2. **Named-type tags (T2)** — the literal strings `override` / `fix_task` / `factory_build` /
   `factory_build_in_progress` — freeze the *names* immediately (already in v4 verbatim + cold-start);
   field schemas (spec §4.5) follow.
3. **XC-3 slots (T10)** — freeze `attempt_no`/`max_attempts`/`escalated`/`closes`/`verdict` (spec §4.5.5)
   so **C39** writes its bound against them. **Frozen this sweep** — resolves C39 RC39-01/OQ1.
4. **Resume contract (T5)** — freeze `factory_build_in_progress` fields (`workflow_handle` + spec/scenario
   pointers) so **C52** / `gc converge resume` can be built against a stub.
5. **C22 registration bundle (T9)** — freeze the `softwarefactory.v4.beads` bundle document shape (spec
   §3.1) so C22's `register_bundle` and bead-type resolution can be wired against a stub.

## 5. Risks & de-risking order

| Risk | De-risking action | Order |
|---|---|---|
| **G11**: Gas City bead-type enforcement *and* the registration mechanism are unverified (OQ-C20-4) — the registry may not be enforceable as designed, and `register_bundle` may not be the bead install path. | The **D-23 Test-A spike** (Sweep-2 first action): run `gc bd` against a real install; confirm (a) whether `type` is a closed set or free-form (prevent vs detect), and (b) whether beads register via C22 `register_bundle` or a native Gas City config. Retires the most uncertainty. | **First** |
| **G18 / OQ-C20-1**: the termination slots may be insufficient for C39's bound, forcing a schema redo. | Co-design the slot set with C39 *before* freezing T4; get C39 to sketch its bound against the draft slots. | Second |
| **OQ-C20-2**: anomaly/diagnosis/resolution may not be beads (could be CXDB turns), invalidating T3. | Confirm the type boundary with C19/C21/C22 owners before investing in T3 field schemas. | Second |
| **OQ-C20-3**: `status` vs type-encoded lifecycle dual representation could cause query ambiguity. | Decide canonical representation during T1/T2; document in registry. | Third |
| Schema drift (AI-CONTEXT §3.5). | Add schema-version pin in T7. | Last |

## 6. Definition of done

**Per-component (ties to spec §8 acceptance criteria):**
- **DoD-1**: `gc bd find --type <T>` resolves for `override`, `fix_task`, `factory_build`,
  `factory_build_in_progress` — G17 closed (spec §8.1).
- **DoD-2**: every registered type carries the common envelope; a bead missing `created_by` is rejected
  (spec §8.2).
- **DoD-3**: a `factory_build_in_progress` bead is resume-complete for `gc converge resume <bead_id>`
  (spec §8.3).
- **DoD-4**: the self-heal closure chain is well-formed (acyclic, ≤1 `resolution`) and carries the
  attempt-count / terminal-state / escalation-marker slots so C39 can express a bound — G18 schema-slots
  delivered, policy correctly deferred to C39 (spec §8.4).
- **DoD-5**: writing an unregistered `type` is rejected (closed registry; spec §8.5 / AC-S2-3). *G11-gated:
  prevent natively vs detect via C02 pack — resolved by the D-23 Test-A spike (OQ-C20-4).*
- **DoD-6 (D-3 registration)**: the `softwarefactory.v4.beads` bundle registers all seven types via C22
  `register_bundle`; `resolve_type` returns a schema for each; a non-D-2 namespace is rejected (AC-S2-R1/R2).
- **DoD-7 (XC-3 freeze)**: the five slot identifiers (`attempt_no`/`max_attempts`/`escalated`/`closes`/
  `verdict`) are frozen and C39 builds against them with no remaining "C20 will name these later" deferral
  (AC-S2-6; closes C39 RC39-01).

**Per-task**: each Tn lands with its field schema documented in the registry and a unit check covering
its validation rule. T7 lands with a registry↔store conformance check and a schema-version pin.

**Open-question exit**: OQ-C20-1 (C39 bound ownership) and OQ-C20-2 (chain-type boundary) must be
resolved or explicitly carried to sweep 2 before T3/T4 are considered frozen rather than draft.
