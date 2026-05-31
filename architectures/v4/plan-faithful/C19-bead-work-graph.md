# C19 — Bead store / typed work-graph  (Build Plan, Track A)

> Source / Spec ref: [`spec/C19-bead-work-graph.md`](../spec/C19-bead-work-graph.md)

## 1. Work breakdown

Ordered tasks to build C19. Sizes: S/M/L. Sweep-1 altitude — make the work-graph **real, typed, attributed,
durable, and queryable**; deep record schema / file-layout / migration code is sweep 2+. C19 is a *native
Gas City capability* (AI-CONTEXT §3.2 #2), so much "build" work is **adopt + verify + bind the contract**,
not author-from-scratch.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | Freeze the **C19↔C20 bead-record contract**: every bead is `{id, type, created_by, dependency-edges, state, history}`; C20 supplies the legal `type` set + per-type fields. This is the load-bearing freeze that breaks the C19/C20 cycle (OQ-C19-1, G17). | M | spec §3/§4; C20 stub |
| **T2** | Verify Gas City's **native bead store + `gc bd`** against an actual `gc` install (G11): `gc bd` create/find/by-type/by-`created_by`, dependency edges, durability across a process restart. Record what is native vs. must-be-packed. | M | C01 verification |
| **T3** | Fix the **attribution-total** + **typed-total** + **durable-across-sessions** invariants as the adopted contract C41/C20/C18/C05 build against. | S | T1, T2 |
| **T4** | Bind the **`[beads] provider = "file"`** backend (Phase 0): prove cross-session durability + the §16 cold-start recipe (`gc bd find --type factory_build_in_progress` → `transfused_from` → `gc converge resume <id>`) runs end-to-end (with C20 types stubbed). | M | T2, T3 |
| **T5** | Specify the **dependency-edge + self-heal-chain** representation (anomaly→diagnosis→fix→resolution as a connected sub-graph) so C39/C35 can write/read chains. | M | T1 |
| **T6** | Bind the **`created_by` attribution path** end-to-end (every create stamps a non-empty actor) and mark the *self-asserted* limitation (G36) at the C19↔C41 seam. | S | T3 |
| **T7** | (sweep 2) Concrete **bead record schema + `gc bd` signatures + edge/link semantics per type** (jointly with C20). | L | T1, T2 |
| **T8** | (sweep 2) **`file` backend crash/concurrency semantics** + **file→Dolt migration** + schema-version pin (AI-CONTEXT §3.5). | L | T2, T7 |

## 2. Dependency graph

- **Upstream gates**: **C01** (the `gc` binary providing the native bead store) must be real before T2 can
  verify — the G11 "Gas City unverified" dependency. **C03** supplies `[beads] provider`. T1/T5 (contract,
  edge model) can proceed on v4 text alone; T2/T4 need a live `gc`.
- **Mutual pair**: **C20** — C19 and C20 are co-foundational (OQ-C19-1). The **T1 contract freeze** is what
  lets both build in parallel against a stub: C20 against "a bead has `{id,type,created_by,edges,state}`",
  C19 against "the legal type set comes from C20."
- **Downstream dependents**: **C05** (Sling), **C13** (Molecule), **C18** (Reconciler), **C35** (override),
  **C39** (fix-task chain), **C41** (attribution), **C33** (judge-output beads), **C52** (bootstrap resume).
  All can build against the **frozen T1 contract + T3 invariants** before T4/T7/T8 land.
- **Critical path**: T1 → T3 → (contract+invariants frozen, unblocks C20 and all dependents) → T2 → T4.
  T7/T8 are sweep-2, off the sweep-1 critical path.

## 3. Parallelization

Within C19, after **T1** freezes the bead-record contract:
- **Stream A** (adopt/verify): T2 → T4 (verify native store, then prove file-backend durability + §16 recipe).
- **Stream B** (graph semantics): T5 (dependency edges + self-heal chain) — depends only on T1.
- **Stream C** (attribution): T6 — depends on T3; independent of A/B.
- **Stream D** (sweep 2): T7 → T8 — starts once T1/T2 stabilize.

Streams A, B, C run concurrently once T1+T3 are frozen. T4 is the join point where the verified store
(A) meets the invariants (C) for the end-to-end §16 recipe. **C20 builds in lockstep against T1** as a fifth
parallel stream owned by that component.

## 4. Interfaces-first / contract milestones

Freeze early so dependents and C20 build in parallel against stubs:

1. **M1 — Bead-record contract (T1)**: `{id, type, created_by, edges, state, history}` + "type set owned by
   C20." *Highest-leverage freeze* — breaks the C19/C20 cycle and unblocks every downstream writer. Freeze first.
2. **M2 — Store invariants (T3)**: attribution-total, typed-total, durable-across-sessions, backend-transparent.
   The guarantees C41/C18/C05/C39 rely on. Freeze with M1.
3. **M3 — Query surface (`gc bd`) (T2)**: find-by-id / by-type / by-`created_by`; the read contract C33/C52/§16
   depend on. Verified against real Gas City.
4. **M4 — Edge / chain model (T5)**: the directed dependency edge + the anomaly→diagnosis→fix→resolution chain
   shape; the integration target for C39 loop-closure and C35 override patterns.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **Gas City bead-store reality (G11)** — T2/T4 rest on an unverified third party; the entire "native"
   claim (AI-CONTEXT §3.1 P10) is unproven until a real `gc bd` is exercised. *De-risk first*: confirm
   create/find-by-type/edges/`created_by`/cross-session-durability on an actual install. If any is not
   native, it becomes pack work and the plan grows.
2. **C19↔C20 cycle / G17 (blocker)** — until the T1 contract is frozen, neither store nor schema can build,
   and the §16 `--type factory_build_in_progress` recipe cannot run. *De-risk second*: freeze M1 with C20
   in the same sitting; this is the single most important coordination point in Batch 1's persistence pair.
3. **`file` backend crash/concurrency (OQ-C19-3)** — at L4/L5 fan-out, concurrent writes to a single-node
   file backend are unspecified by v4. Bounded risk for sweep 1 (Phase 0 is low-concurrency), but flag
   loudly to review-log; it gates the Dolt-migration decision (T8).
4. **Attribution integrity (G36)** — `created_by` is self-asserted; loud-flag the residual risk at the
   C19↔C41 seam, but do not build signing (that is C41, optional/deferred).

## 6. Definition of done

**Per-component (sweep 1):**
- The bead-record contract (M1) is committed; C20 and all downstream writers build against it. The C19↔C20
  direction question (OQ-C19-1) is recorded in review-log with the co-foundational resolution.
- Attribution-total / typed-total / durable-across-sessions / backend-transparent invariants stated and
  adopted by C41/C20/C18/C05.
- The `file` backend proves cross-session durability and the §16 cold-start recipe runs end-to-end (with
  C20 types stubbed): find-by-type → `transfused_from` → `gc converge resume`.
- Dependency edges + the self-heal chain shape are specified well enough for C39/C35 to write/read chains.
- `created_by` is stamped on every create; the self-asserted limitation (G36) is surfaced as residual risk
  and mirrored to review-log — no silent acceptance of unsigned provenance as sufficient.

**Per-task:** each task exits when its spec-§8 acceptance criterion holds:
- T3↔AC "attribution-total"; T4↔AC "cross-session durability" + "resume handle" + (with C20) "type-filtered
  query"; T5↔AC "dependency graph / chain recoverable"; T2/T4↔AC "backend transparency" (file now, Dolt at T8).
- Sweep-2 tasks (T7/T8) deferred with their open questions (OQ-C19-2 migration, OQ-C19-3 concurrency)
  recorded in spec §9 and the review-log.
