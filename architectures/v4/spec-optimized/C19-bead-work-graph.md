# C19 — Bead store / typed work-graph  (Spec, Track B)

> Source: component-inventory.md C19 row (maps A20 memory-layer, A19e attribution-via-beads, A21b cross-session continuity, B44 work-ledger); README Part 4 P9 (`created_by` on every bead, l.227–229), P10 ("Dependency-aware persistent task graph… survives across agent sessions… replaces flat scratchpads", l.233–244), Part 6 Phase-0 (`[beads] provider="file"`, l.361–372: "P10 memory layer; bead store handles task graph + cross-session"), Persistence row (l.122 "Gas City beads file or Dolt"); AI-CONTEXT §2 (Persistence = "work ledger (Beads)", l.52), §3.2 concept-2 ("Bead Store — Durable typed work-graph (Dolt or file)", l.86; P1/P5/P9/P10), §3.4 Phase-0 (`[beads] provider="file"`, l.118; Dolt server "explicitly off" l.122), §3.6 ("P10 native"), §13.2 (`[beads] provider="file"` config block l.537–539), §16 cold-agent recovery (`gc bd find`, `gc converge resume <bead_id>` l.694–699); _meta gaps **G17** (no schema for any core store — **blocker**, shared with C20/C21/C22), G36 (attribution optional/deferred — touches the graph's `created_by` invariant); F-MODE-COVERAGE P9/P10 rows.
> Inventory ID: C19   Kind: data-store   Status: sweep-1
> Deltas: DELTA-01 (single provider-abstraction seam — file ⇄ Dolt is one interface, not two code paths); DELTA-02 (`created_by` is a NON-NULL graph invariant enforced at the store, closing G36's "optional/deferred" gap at the work-graph layer); DELTA-03 (dependency edges are typed + acyclic-by-construction, with a named edge taxonomy `blocks`/`closes`/`caused_by`/`child_of` shared with C20); DELTA-04 (file-provider durability contract: append + fsync + atomic-rename, so a Phase-0 install survives crash without Dolt); DELTA-05 (monotonic per-store `seq` on every bead mutation → cheap event-bus/C23 emission + ordered cross-session replay); DELTA-06 (schema enforcement is delegated to C20 at the write seam, but C19 owns a `bead_format_version` envelope so the store can evolve independently of any one type's schema); DELTA-07 (graph query contract — `gc bd find`/dependency-walk — frozen as a stable interface so C13/C18/C35/C39/C50 build against it before the Dolt provider exists).

## 1. Purpose & responsibility

C19 is the **durable, typed work-graph**: the memory layer that survives across agent sessions. It is Gas City's "Bead Store" (AI-CONTEXT §3.2 concept-2) rendered as a v4 component. A *bead* is a node of work (task, override record, fix-task, factory-build, …); the **graph** is the set of beads plus their **typed dependency edges**; the **store** is the durable backing (file in Phase 0, Dolt later) that persists the graph and lets a cold agent reconstruct exactly where work stood (README §16, "find its bead… resume the workflow").

C19's load-bearing transform: **"every unit of work and its dependencies is a durable, attributed node that outlives the session that created it"** — replacing the flat scratchpad (README l.235) so that a restarted or resumed agent reads the graph, not a lost in-memory TODO list.

C19 owns:
- **The node container** — the generic bead *envelope* (`id`, `type`, `created_by`, `created_at`, `seq`, `lifecycle_state`, `bead_format_version`) and the storage of an opaque typed *payload* whose shape C20 governs.
- **The typed dependency graph** — edges between beads with a named edge taxonomy (`blocks`, `closes`, `caused_by`, `child_of`; DELTA-03), and the **acyclicity invariant** over blocking edges.
- **Durable persistence + the provider seam** — one abstraction (`BeadStore`) with two backends, `file` and `dolt` (DELTA-01); the file backend carries a concrete durability contract (DELTA-04).
- **Cross-session continuity** — stable bead `id`s and a monotonic `seq` (DELTA-05) so an agent resuming after restart sees a consistent, ordered graph and can answer "what was in progress?" (the §16 query substrate).
- **The query / traversal contract** — `gc bd find` by type/state/actor, dependency-walk (`closes`/`caused_by` chains for C39, `blocks` frontier for C18/C13), frozen early (DELTA-07).
- **The mutation seam where C20 validation fires** — C19 is the *writer* that calls C20's `validate(bead)` before committing (DELTA-06).

What it is **NOT**:
- **Not the bead schema.** C20 owns the closed type catalog, per-type field schemas, per-type lifecycle state machines, and the loop-closure invariant. C19 owns the *generic* container, the *graph*, and *storage*; it treats payloads as opaque-but-validated blobs. (Clean split: C20 says "a `fix_task` has fields X and may move open→attempting"; C19 says "here is the node, its edges, and how it persists.")
- **Not the trajectory store.** C21 (CXDB) is the content-addressed turn-DAG for *conversation/trajectory* replay; C19 is the *work*-graph. They meet only at C20's bead-type→CXDB-bundle binding. A bead is **not** a CXDB turn (README l.241–244: beads = work-graph layer, CXDB = richer trajectory analysis when self-healing needs it).
- **Not the event bus.** C23 is the append-only action log; C19 *emits* a mutation event to C23 per bead change (DELTA-05) but does not own the event stream.
- **Not identity.** C41 defines the `Actor` model; C19 *requires and stores* `created_by` as a non-null reference to a C41 actor (DELTA-02) but does not mint or verify identities (verification is C41's optional signed-provenance layer).
- **Not the control loops.** C18 (reconciler), C35 (override), C39 (fix-loop), C13 (molecule), C50 (promotion) all *read/write* beads; their policy lives in those components. C19 is the substrate they share.

## 2. Context & dependencies

- **Depends on:**
  - **C01** (Gas City substrate) — beads are a native Gas City primitive; C19 is the v4 spec of that primitive + the `gc bd` CLI surface. Per the inventory, C19 depends on C01 only.
  - **C20** (bead schema) — **co-foundational; canonical direction (review-log D-4): C20 depends on C19** (the schema layer sits over the graph store). C19 calls C20's `validate` at the write seam (DELTA-06); that call is the only reverse arrow, and the production write-path cycle is broken by the **M1 interface freeze + a no-op `validate` stub** (the stub lets C19 build/store the generic envelope before C20's catalog is final; the production path is then fail-closed against C20). Interface-first; see plan.
  - **C41** (identity/actor) — supplies the `Actor` referenced by `created_by` (DELTA-02). In a Phase-0 single-agent install the actor set is trivial (one `worker`), so this is a *type* dependency, not a runtime blocker.
  - **C03** (config / feature-flags) — `[beads] provider = "file"|"dolt"` selects the backend (AI-CONTEXT §13.2); section presence/value is the feature flag.
  - **C23** (event bus) — receives the per-mutation event (DELTA-05); soft dependency (a Phase-0 install can run with the bus off, buffering or no-op'ing emission).
- **Consumed by (fan-out — C19 is a Batch-1 load-bearer):**
  - **C13** molecule — a molecule *is* an instantiated bead-tree (AI-CONTEXT §3.2 concept-7); C13 builds on C19's graph.
  - **C18** reconciler — reads the `blocks` frontier to compute desired-state convergence.
  - **C05** sling/dispatch — routes a bead/wisp to an agent (C05 depends on C18 + C01; the bead it routes is a C19 node).
  - **C35** override loop — writes `override` beads; **C39** fix-loop — writes `fix_task` beads + walks `closes`/`caused_by` chains; **C50** promotion gate; **C33** satisfaction aggregator (reads judge-output beads, README l.426); **C41** audit trail (reads `created_by` history); **C51** gene-transfusion (`transfused_from` provenance lives on factory-build beads); **bootstrap-resume / AI-CONTEXT §16** (`gc bd find` + `gc converge resume`).
- **Sits at:** the base of the **Persistence & Memory** subsystem — the storage/graph layer that C20 schemas sit on top of, and that nearly every control loop reads/writes. Foundational; freeze the envelope + edge taxonomy + query contract first so dependents build against stubs.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures, JSON/msgpack shapes, and Mermaid state/sequence diagrams in sweep 2).

**Inbound — the `BeadStore` write/graph API (what writers call, exposed via `gc bd` CLI + library):**
- `create(bead_draft) → BeadId` — validates via C20, assigns `id` + monotonic `seq`, persists, emits a mutation event. Fail-closed on C20 validation failure (DELTA-06).
- `update(id, mutation) → seq` — applies a lifecycle/field mutation; re-validates against C20; bumps `seq`; emits event. Concurrent-update conflicts resolved per the provider's concurrency contract (§4.4).
- `add_edge(from, to, edge_type) → ()` — adds a typed dependency edge; **rejects** any edge that would introduce a cycle in the `blocks` sub-graph **or** the `child_of` tree (DELTA-03 acyclicity invariant). `caused_by`/`closes` are not cycle-checked here (bounded by C20).
- `get(id) → Bead` / `exists(id) → bool`.

**Inbound — the query / traversal contract (frozen early, DELTA-07):**
- `find(predicate) → [Bead]` — by `type`, `lifecycle_state`, `created_by`, time range; this is the `gc bd find --type … --state …` surface §16 depends on.
- `walk(id, edge_type, direction) → [Bead]` — dependency traversal: the `closes`/`caused_by` chain (C39 loop-closure proof), the `child_of` tree (C13 molecule), the `blocks` frontier (C18 ready-work).
- `ready_frontier() → [Bead]` — beads with no unsatisfied `blocks` predecessor (the dispatchable set C05/C18 consume).

**Outbound:**
- → **C20** `validate(bead) → ValidationReport` at every `create`/`update` (DELTA-06).
- → **C23** `BeadMutationEvent { bead_id, seq, type, lifecycle_state, created_by, op }` per mutation (DELTA-05) — the "lowest-impedance" attributed/trajectory-shaped feed (AI-CONTEXT §5.4 ranks Gas City event-bus JSONL highest for CXDB ingest).
- → **C41** reads (audit): the `created_by` + `seq` history of any bead.

**Invariants:**
- **Attribution (DELTA-02, closes G36 at the graph layer):** no bead is creatable/mutable without a non-null `created_by` resolving to a C41 actor. Attribution is structural, not "optional/deferred" — README l.227 says P9 is "the strongest principle match… attribution flows automatically through beads"; making it nullable would contradict that. C41's *signature* verification remains optional, but the *presence* of an actor is mandatory here.
- **Durability (DELTA-04):** once `create`/`update` returns, the mutation survives process crash — file provider does append-then-fsync-then-atomic-rename of its index; Dolt provider commits. No "scratchpad lost on restart" (the exact failure README l.235 calls out).
- **Acyclic blocking graph + acyclic molecule tree (DELTA-03):** `add_edge` enforces acyclicity on the `blocks` sub-graph (a DAG at all times, so `ready_frontier()` always terminates) **and** on `child_of` (a tree — a `child_of` cycle would make a molecule its own ancestor and break C13's tree walk). `caused_by`/`closes` may form chains across distinct anomaly instances and are *not* cycle-checked at the graph layer; their termination is C20's loop-closure invariant, not C19's.
- **Monotonic ordering (DELTA-05):** `seq` is strictly increasing per store; a cross-session reader replays mutations in `seq` order and reaches the same graph state — the basis of deterministic resume (§16).
- **Stable identity:** a bead's `id` is immutable across all lifecycle transitions, so `gc converge resume <id>` (§16) and `transfused_from`/`closes` references never dangle.
- **Provider transparency (DELTA-01):** the same `BeadStore` contract holds whether `provider="file"` or `"dolt"`; switching providers is a config change (C03), not a code change for dependents.

## 4. Data model / state

### 4.1 Generic bead envelope (C19-owned; payload is C20-owned)

| Field | Req | Owner | Notes |
|---|---|---|---|
| `id` | yes | C19 | Stable, immutable across lifecycle (§3 invariant). |
| `type` | yes | C20 catalog | ∈ C20's closed type enum; C19 stores it, C20 constrains it. |
| `bead_format_version` | yes | C19 | Envelope/storage-format version (DELTA-06) — distinct from C20's per-type `schema_version`; lets the *store* evolve independently of any type's payload schema. |
| `schema_version` | yes | C20 | The payload schema version C20 validated against. |
| `created_by` | yes | C41 ref | Non-null actor (DELTA-02). |
| `created_at` | yes | C19 | RFC3339. |
| `seq` | yes | C19 | Monotonic per-store mutation ordinal (DELTA-05). |
| `lifecycle_state` | yes | C20 lifecycle | C19 stores it; C20's per-type state machine constrains legal transitions. |
| `payload` | yes | C20 | Opaque-to-C19 typed body; validated by C20 at the write seam. |
| `edges` | — | C19 graph | Typed dependency edges (§4.2). Stored in the graph, not duplicated in payload. |

### 4.2 Edge taxonomy (DELTA-03 — shared vocabulary with C20)

| Edge | Semantics | Acyclic? | Primary consumer |
|---|---|---|---|
| `blocks` | source must complete before target is dispatchable | **yes (enforced at `add_edge`)** | C18 reconciler / C05 sling `ready_frontier()` |
| `child_of` | target is a sub-bead of source (molecule tree) | **yes (enforced at `add_edge`)** | C13 molecule |
| `caused_by` | source bead/event caused this bead (anomaly → fix) | chain | C39 fix-loop, C38 diagnosis |
| `closes` | this bead closes/resolves the target (fix proves anomaly cleared) | chain | C39 loop-closure proof (G18, in C20) |

> **Acyclicity enforcement scope (review fix RC19B-03):** `add_edge` enforces acyclicity on **both**
> `blocks` (the dispatch DAG) *and* `child_of` (the molecule tree — a tree is by definition acyclic; a
> `child_of` cycle would make a molecule its own ancestor and break C13's tree walk). `caused_by`/`closes`
> are chains that may legitimately revisit a node only across *distinct* anomaly instances; they are not
> cycle-checked, but C20's loop-closure invariant bounds them. Earlier wording named `blocks` as the
> "single enforcement point", contradicting this table's "yes (tree)" for `child_of`; reconciled here.

> [DELTA-03] **v4 said:** beads are "tasks with dependencies" (README l.239) — "dependency" is singular and untyped; the corpus never names edge kinds. **Change:** a typed edge taxonomy with one *acyclicity-enforced* kind (`blocks`). **Rationale (correctness + simplicity):** the self-heal loop's `caused_by`→`closes` chain (C39/C20 G18) and the reconciler's ready-frontier need *different* edge semantics; collapsing them into one untyped "dependency" forces every consumer to re-derive intent and makes the acyclicity guarantee unstatable. **Tradeoff:** four named edge kinds is a small fixed vocabulary C20 + downstream loops must agree on (shared seam, flagged OQ2).

### 4.3 Provider model (DELTA-01)

| Provider | Backing | When | Durability (DELTA-04) | Concurrency |
|---|---|---|---|---|
| `file` | `turns`-style append log + index files under the city dir | Phase 0 (smallest install, AI-CONTEXT §3.4) | append → fsync → atomic-rename of index | single-writer (one agent in Phase 0); **advisory** lock for multi-process — see caveat |
| `dolt` | Dolt SQL/versioned DB server | later phases (multi-rig, branching, AI-CONTEXT §3.4 "Dolt server explicitly off" in P0) | transactional commit | MVCC / Dolt transactions |

Both satisfy the identical `BeadStore` contract (§3). Provider is selected by `[beads] provider = …` (C03 / AI-CONTEXT §13.2). **No dependent code branches on provider** (DELTA-01) — this is what lets Phase-0 (`file`) work be carried forward unchanged when Dolt arrives.

> [DELTA-01] **v4 said:** "Gas City beads (file or Dolt)" stated as two interchangeable backings (README l.122/239, AI-CONTEXT §3.2). **Change:** make "file or Dolt" a single explicit `BeadStore` provider seam with a frozen contract, not two parallel narratives. **Rationale (operability + parallelizability):** dependents (C13/C18/C35/C39) must build against one stable interface during Phase 0 (file-only) and survive the Dolt migration with zero changes; an unspecified seam invites two divergent feature sets. **Tradeoff:** the contract must be conservative — it can only expose capabilities *both* backends can honor (e.g., O(1) branching is a Dolt/CXDB property, deliberately NOT a `BeadStore` guarantee).

### 4.4 Storage & consistency

- **File provider:** mutation = append a record to the bead log + update derived indexes (by `id`, by `type`, by `lifecycle_state`, edge adjacency) under fsync + atomic-rename so a crash mid-write leaves either the old or new index, never a torn one (DELTA-04). `seq` is the log ordinal. Recovery = replay the log in `seq` order (DELTA-05).
- **Dolt provider:** mutation = a transaction; `seq` from a monotonic sequence; branching/merge available but **not** exposed through `BeadStore` (DELTA-01 conservatism).
- **Consistency:** single-writer linearizable in Phase 0; the contract specifies read-your-writes and `seq`-monotonic reads. Multi-writer (multi-rig) consistency is a Dolt-era concern (OQ3).
  > **Caveat (review fix RC19B-04):** the multi-process *advisory* lock on the `file` provider is cooperative — a writer that ignores it (or a crash that strands the lock) can still corrupt the shared append log + indexes. The DELTA-04 durability guarantee (no torn write) holds *per writer* under atomic-rename, but **cross-writer serialization on the file provider is best-effort, not enforced**. True multi-writer safety is the Dolt provider's MVCC, deferred to OQ3. Phase 0 is single-writer by construction, so this is a correctness footnote, not a Phase-0 blocker — but the L4/L5 fan-out (OQ3) must move to Dolt before multiple agents share one file store.

## 5. Behavior

Key flows (Mermaid sequence/state diagrams in sweep 2):

- **Write path:** writer builds a `bead_draft` → `BeadStore.create` → **C20 `validate`** (fail-closed) → assign `id`+`seq` → persist (provider durability contract) → emit `BeadMutationEvent` to C23. A validation failure returns the `ValidationReport`; nothing is persisted.
- **Edge path:** `add_edge(from,to,blocks)` → cycle check over the `blocks` sub-graph → reject-or-commit. Other edge kinds skip the cycle check but must reference existing beads.
- **Cross-session resume (§16, the headline P10 flow):** agent restarts → `find(type=factory_build, state=in_progress)` (C20 DELTA-02 folds the §16 `factory_build_in_progress` *type* query into this state query — C19 honors it via the C20 OQ1 shim) → read `transfused_from`/`spec_ref`/`resume_token` from payload → `gc converge resume <id>`. C19's stable `id` + durable store are what make this deterministic.
- **Self-heal closure walk:** C39 calls `walk(anomaly_id, caused_by, forward)` then checks for a `closes` edge back to the anomaly — C19 supplies the traversal; C20's invariant guarantees the chain terminates (resolved/escalated).
- **Ready-frontier dispatch:** C18/C05 call `ready_frontier()` → beads whose `blocks` predecessors are all in a terminal state → dispatched via sling.
- **Audit read (P9):** C41 reads any bead's `created_by` + `seq`-ordered mutation history.

## 6. Failure modes & handling

- **G17 (no store schema — blocker; RESOLVED for the *generic container + graph*):** C19 defines the envelope (§4.1), edge taxonomy (§4.2), provider/durability model (§4.3) concretely; the *typed payload* schema is C20's half of G17 (the two components jointly close it). Residual: C20 must land its catalog for the write path to be fully fail-closed.
- **G36 (attribution optional/deferred — RESOLVED at the graph layer):** `created_by` is a non-null store invariant (DELTA-02); a bead with no actor is unwritable. Signature *verification* stays optional (C41), but the corpus's "strongest match" claim for P9 (README l.227) is now structurally true at the store, not convention.
- **Scratchpad-loss-on-restart (the P10 motivating failure, README l.235):** durability contract (DELTA-04) + deterministic `seq`-ordered replay (DELTA-05) guarantee a resumed agent sees the committed graph, not a lost in-memory list.
- **Dependency cycle / non-terminating frontier:** `add_edge` acyclicity enforcement on `blocks` (DELTA-03) prevents a `ready_frontier()` that can never advance.
- **Dangling reference after lifecycle transition:** stable immutable `id` invariant — `closes`/`caused_by`/`transfused_from`/`resume_token` references never break across state changes (relevant to C20 DELTA-02's single-build-identity contract).
- **Torn write / partial index on crash (file provider):** append + fsync + atomic-rename (DELTA-04); recovery replays the log, rebuilding indexes from `seq` order.
- **Provider divergence:** the conservative `BeadStore` contract (DELTA-01) prevents dependents from accidentally relying on Dolt-only capabilities (e.g., branching), which would break under the `file` provider.
- **Event-bus down (C23 absent/failing):** mutation emission is best-effort/buffered; a store write does NOT fail because the bus is down (decouples the work-graph's durability from the observability path) — flagged OQ1 (at-least-once vs drop policy).

## 7. Cross-cutting

- **Security / governance:** mandatory `created_by` (DELTA-02) is the substrate for P9 attribution and C41's audit trail; every mutation is attributable and `seq`-ordered. The store does not grant capabilities — it records who acted.
- **Cost / scale:** file provider is O(1)-append per mutation + O(index) update; query cost is index-bounded. No external service in Phase 0 (zero marginal cost over the city dir). Dolt provider scales to multi-rig + history at the cost of running a server (deferred until multi-rig need, AI-CONTEXT §3.4).
- **Observability:** every mutation is an event to C23 (DELTA-05) — the highest-ranked CXDB ingest source (AI-CONTEXT §5.4). The graph itself is queryable (`gc bd find`) for ops/debug.
- **Operability:** one config flag toggles the backend (C03); stable `id` + deterministic replay make resume robust; the frozen query contract (DELTA-07) de-risks the whole downstream fan-out.

## 8. Acceptance criteria & test strategy

1. **Durability (DELTA-04):** kill the process mid-`create`; on restart the store contains either the complete bead or none — never a torn record; the index rebuilds from the log in `seq` order. (Crash-injection test on the file provider.)
2. **Attribution invariant (DELTA-02 / G36):** `create`/`update` with null/unknown `created_by` is rejected; no path writes an unattributed bead. (Golden negative test.)
3. **Acyclicity (DELTA-03):** `add_edge(blocks)` that would close a cycle is rejected; non-blocking edges may chain. (Property test over generated graphs.)
4. **Cross-session resume (§16):** write a `factory_build`/`in_progress` bead, restart, `find` it by state, read `resume_token` — the §16 flow returns the same stable `id`. (Integration test.)
5. **Provider parity (DELTA-01):** the full `BeadStore` contract test suite passes identically against `file` and `dolt`; no dependent test branches on provider. (Contract test, both backends.)
6. **Validation seam (DELTA-06):** a payload that fails C20 `validate` is never persisted; the `ValidationReport` surfaces. (Integration test against a C20 stub then the real C20.)
7. **Ordering/replay (DELTA-05):** replaying mutations in `seq` order reconstructs the identical graph; `seq` is strictly increasing across a restart. (Deterministic-replay test.)
8. **Query contract (DELTA-07):** `find`/`walk`/`ready_frontier` honor the frozen signatures dependents (C18/C39/C13) built stubs against. (Contract-conformance test.)

## 9. Open questions

- **OQ1 (→ review-log):** Event-emission delivery policy when C23 is down — at-least-once with buffer/replay vs best-effort drop. The store-durability path must not block on the bus, but losing mutation events degrades CXDB trajectory completeness (AI-CONTEXT §5.4) and the self-heal feed. *Top open question* — it sets the C19↔C23↔C24 seam contract that G26/G27 also touch.
- **OQ2 (→ review-log):** The edge taxonomy (`blocks`/`closes`/`caused_by`/`child_of`, DELTA-03) is shared with C20's lifecycle invariants and C39's closure walk. Which component is the canonical owner of the edge-kind enum — C19 (graph) or C20 (schema)? Proposed: C19 owns the *kinds*, C20 owns the *per-type rules about which kinds are required* (e.g., `fix_task.resolved` requires a `closes` edge).
- **OQ3:** Multi-writer consistency once `provider="dolt"` and multiple rigs write concurrently — does `BeadStore` expose any branching/merge, or stay single-logical-writer with Dolt purely as durable backing? DELTA-01 currently keeps branching out of the contract; revisit when C42 rig-partitioning lands.
