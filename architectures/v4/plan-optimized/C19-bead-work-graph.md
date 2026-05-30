# C19 — Bead store / typed work-graph  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C19-bead-work-graph.md
> Track B, sweep 1. Foundational (Batch 1). Deltas referenced: DELTA-01…07 (see spec header).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prereqs by task id (and external C-IDs).

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Bead envelope + `BeadStore` contract freeze** — `{id, type, bead_format_version, schema_version, created_by, created_at, seq, lifecycle_state, payload, edges}`; `create`/`update`/`get`/`exists` signatures. Payload opaque-to-C19. DELTA-02 (`created_by` non-null), DELTA-06 (`bead_format_version`). | S | — (confirm C01 native bead shape; OQ via G11) |
| T2 | **Edge taxonomy + graph model** — `blocks`/`child_of`/`caused_by`/`closes`; `add_edge`/`walk`/`ready_frontier` signatures; `blocks`-acyclicity invariant. DELTA-03. | S | T1 |
| T3 | **Query contract freeze** — `find(predicate)` by type/state/actor/time; the `gc bd find` CLI surface §16 needs. DELTA-07. | S | T1 |
| T4 | **File provider — durability core** — append log + rebuildable indexes (by id/type/state/edge); append→fsync→atomic-rename; `seq` = log ordinal; crash-replay recovery. DELTA-04, DELTA-05. | M | T1, T2 |
| T5 | **C20 validation seam** — wire `create`/`update` to call C20 `validate(bead)` fail-closed; reject-and-report on failure. DELTA-06. | M | T1, **C20** (stub then real) |
| T6 | **Acyclicity enforcement** — cycle check over the `blocks` sub-graph at `add_edge`; reject-or-commit. DELTA-03. | S | T2, T4 |
| T7 | **`ready_frontier()` + dependency walk impl** — `blocks`-frontier; `caused_by`/`closes` chain walk; `child_of` tree. | M | T2, T4 |
| T8 | **C23 mutation-event emission** — `BeadMutationEvent` per mutation; decoupled from store durability (store write must not block on bus). DELTA-05. | M | T4, **C23** (stub), **C41** |
| T9 | **Cross-session resume path** — stable-`id` guarantee + `seq`-ordered replay; honor the §16 `find(type=factory_build, state=in_progress)` query (via C20 OQ1 shim). | M | T3, T4, T7 |
| T10 | **Dolt provider** — same `BeadStore` contract over Dolt transactions + monotonic seq; branching deliberately NOT exposed. DELTA-01. | L | T1–T7 (contract frozen), **C03** (`[beads] provider`) |
| T11 | **Provider-parity contract test suite** — one suite runs identically against `file` and `dolt`. DELTA-01. | M | T4, T10 |
| T12 | **`gc bd` CLI surface** — `find`/`create`/`update`/edge ops over the library; the operator + cold-agent surface (§16). | M | T3, T5, T7 |

## 2. Dependency graph

- **Upstream (must precede C19 being *complete*):** C01 (native bead primitive + `gc bd` — C19 specs the contract it must honor; G11 makes this an unverified-third-party assumption to spike). C20 for the fail-closed write path (T5) — but the *generic* envelope + graph (T1–T4, T6, T7) build ahead of C20's catalog. C03 selects the provider (T10). C23 + C41 only gate T8.
- **Downstream (gated *by* C19):** C13 (molecule = bead-tree), C18 (reconciler reads `ready_frontier`), C05 (sling routes a bead), C35/C39 (write override/fix_task beads + walk closure chains), C33/C50/C41/C51, and bootstrap-resume (§16). They consume the `BeadStore` + query contract; none re-implement storage.
- **Critical path inside C19:** T1 → T2 → T4 → T6/T7 → T9. T5 (C20 seam) and T8 (C23 seam) hang off T1/T4 with stubs. T10/T11 (Dolt) are a parallel later track once the contract is frozen.
- **System critical-path note:** C19 is Batch-1 foundational; its **contract freeze (T1–T3)** unblocks the largest downstream fan-out in the inventory. The freeze matters more than full impl — ship file-provider + frozen contract first, Dolt later.

## 3. Parallelization

Explicit fan-out after the T1–T3 interface freeze:

- **Stream A (storage core):** T1 → T4 → T6 → T7. The durable file graph.
- **Stream B (schema seam):** T5 — codes against a C20 `validate` stub, swaps to real C20 when its catalog lands. Independent of A's internals.
- **Stream C (observability seam):** T8 — codes against a C23 stub; independent until A's `seq` exists.
- **Stream D (resume + CLI):** T9 → T12 — joins A at T7.
- **Stream E (Dolt provider):** T10 → T11 — a self-contained later workstream that only consumes the *frozen contract* (T1–T3), so it can be built by a separate worker against the parity suite without touching Stream A.

T1 is the single gate; T2/T3 follow immediately and in parallel. Streams B, C, E each depend only on the frozen contract + a stub, so three independent workers can proceed once T1–T3 land.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs:

1. **`BeadStore` write/read API + bead envelope (T1)** — the single store surface; every dependent codes against this, never raw provider storage. Freeze first.
2. **Edge taxonomy + `add_edge`/`walk`/`ready_frontier` (T2)** — so C18/C39/C13 know the edge kinds and traversal contract before storage is done.
3. **Query contract `find`/`gc bd find` (T3)** — so §16 cold-agent recovery + C41 audit code against a stable predicate surface.
4. **`BeadMutationEvent` shape (T8 contract)** — so C23/C24 reserve the schema (the §5.4 highest-impedance-ranked ingest feed).
5. **C20 `validate` call shape (T5 contract)** — co-frozen with C20's `validate` signature so the write seam is agreed both ways.

Stub strategy: ship the `BeadStore` interface + file provider + a no-op C20/C23 stub first; dependents validate against that while Streams B/C/E finish. The edge-kind enum ownership (OQ2) must be settled at freeze time since both C19 and C20 reference it.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **G11 — does Gas City's native bead already define the envelope / `gc bd` semantics?** Spike T1 against the real `gc` before freezing. If Gas City's bead shape conflicts with the v4 envelope (e.g., no `seq`, optional `created_by`), DELTA-02/05 become conform-or-extend-via-pack decisions touching C01/C02. Retire first — it gates the whole contract.
2. **DELTA-04 file-provider durability** — prototype append→fsync→atomic-rename + crash-replay early; a torn index or lost mutation on restart is the exact P10 "scratchpad lost" failure C19 exists to prevent. Crash-injection harness is the de-risking artifact.
3. **OQ2 — edge-kind enum ownership (C19 vs C20).** Decide before T2 + C20's lifecycle work scale, or the two drift. Proposed split (C19 owns kinds, C20 owns per-type required-edge rules) must be ratified at freeze.
4. **OQ1 — C23-down emission policy (at-least-once vs drop).** De-risk by shipping the decoupled seam (store write never blocks on bus) and a buffer stub; the durability-vs-completeness tradeoff (touches G26/G27) can be tuned after the core lands.
5. **DELTA-01 provider parity** — the Dolt provider (T10) is the highest-effort, latest item; de-risk by writing the parity suite (T11) against the file provider *first* so Dolt is built test-first against a frozen, already-passing contract.

## 6. Definition of done

Per-component (ties to spec §8 acceptance):

- **DoD-1 Durability (DELTA-04):** crash mid-`create` leaves a complete bead or none — never torn; index rebuilds from `seq`-ordered log. [T4]
- **DoD-2 Attribution (DELTA-02 / G36):** no `create`/`update` succeeds with null/unknown `created_by`. [T1,T5]
- **DoD-3 Acyclicity (DELTA-03):** a `blocks` edge that would close a cycle is rejected; non-blocking edges may chain. [T6]
- **DoD-4 Resume (§16):** a `factory_build`/`in_progress` bead is recoverable by state query with a stable `id` after restart. [T9]
- **DoD-5 Provider parity (DELTA-01):** the parity suite passes identically on `file` and `dolt`; no dependent branches on provider. [T11]
- **DoD-6 Validation seam (DELTA-06):** a payload failing C20 `validate` is never persisted; the report surfaces. [T5]
- **DoD-7 Ordering/replay (DELTA-05):** `seq`-ordered replay reconstructs the identical graph; `seq` strictly increases across restart. [T4,T9]
- **DoD-8 Query contract (DELTA-07):** `find`/`walk`/`ready_frontier` honor the frozen signatures the dependents stubbed against. [T3,T7]

Per-task DoD: each task lands with unit tests for its acceptance bullet against the frozen §4 interfaces; no task is "done" until the contract it implements is unchanged from freeze (or the change is propagated to all stub consumers).

Component is **done** when DoD-1…8 pass, the §4 contracts are frozen and consumed by at least one real downstream component (C13 molecule-as-bead-tree, or C39 fix-task closure walk, is the canonical integration check), and the §16 cold-agent resume flow works end-to-end against the file provider.
