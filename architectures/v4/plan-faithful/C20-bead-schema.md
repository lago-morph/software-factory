# C20 — Bead schema registry  (Build Plan, Track A)

> Source / Spec ref: [`spec/C20-bead-schema.md`](../spec/C20-bead-schema.md)

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
| T8 | **Query smoke set.** Verify `gc bd find --type <T>` resolves for all four named types (G17 acceptance, spec §8.1). | S | T2, T6 |

## 2. Dependency graph

```
C19 (bead store/work-graph)        ← hard upstream; provides node persistence + gc bd surface
        │
        ▼
       T1 ──▶ T2 ──▶ T5
        │      │
        │      ├──▶ T6 ──▶ T7
        ▼      │              ▲
       T3 ──▶ T4 ────────────┘
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
- **Cross-component**: C20 is a Batch-1 foundational schema authored in parallel with C19; the two teams
  must co-design the envelope (T1) so C19's store and C20's registry agree (spec §4.4). This is the one
  hard synchronization point.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents (C35, C39, C51, C52) can build against stubs:

1. **Common envelope (T1)** — `id`/`type`/`created_by`/`dependencies`/`status` — freeze first; C41
   (`created_by`) and every downstream consumer reads it.
2. **Named-type tags (T2)** — the literal strings `override` / `fix_task` / `factory_build` /
   `factory_build_in_progress` — freeze the *names* immediately (they are already in v4 verbatim and in
   cold-start instructions); field schemas can follow.
3. **Closure-chain shape + termination slots (T4)** — freeze the chain edges and the attempt-count /
   terminal-state / escalation-marker slot names so **C39** can write its bound against them (OQ-C20-1).
4. **Resume contract (T5)** — freeze `factory_build_in_progress` fields so **C52** / `gc converge resume`
   can be built against a stub.

## 5. Risks & de-risking order

| Risk | De-risking action | Order |
|---|---|---|
| **G11**: Gas City bead-type enforcement is unverified — registry may not be enforceable as designed (OQ-C20-4). | Spike: run `gc bd` against a real install; confirm whether `type` is a closed set or free-form. This retires the most uncertainty. | **First** |
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
- **DoD-5**: writing an unregistered `type` is rejected (closed registry; spec §8.5).

**Per-task**: each Tn lands with its field schema documented in the registry and a unit check covering
its validation rule. T7 lands with a registry↔store conformance check and a schema-version pin.

**Open-question exit**: OQ-C20-1 (C39 bound ownership) and OQ-C20-2 (chain-type boundary) must be
resolved or explicitly carried to sweep 2 before T3/T4 are considered frozen rather than draft.
