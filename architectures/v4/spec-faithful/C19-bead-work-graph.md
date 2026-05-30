# C19 — Bead store / typed work-graph  (Spec, Track A)

> Source: AI-CONTEXT §3.2 ("nine concepts" #2 — "Bead Store: Durable typed work-graph (Dolt or file); P1, P5, P9, P10"); AI-CONTEXT §2 ("Persistence — event store (CXDB) + work ledger (Beads)"); AI-CONTEXT §3.1 (coverage map: P10 "Strong (bead store, file or Dolt)"); AI-CONTEXT §13.1 (`[beads] provider = "file"`); AI-CONTEXT §16 cold-start (`gc bd find --type factory_build_in_progress`; `gc converge resume <bead_id>`; `transfused_from`); AI-CONTEXT §15.1 (`github.com/gastownhall/beads`); README Part 4 — P2 persistence row (line 122 "Gas City beads (file or Dolt)"), P8 override-log row (214 "beads with type `override`"), P9 attribution rows (227–229 "native `created_by`", "bead history", "signature on bead provenance"), P10 rows (239–242 "Tasks with dependencies", "`gc bd` commands"), P11 rows (257–259 `fix_task` bead / "bead chain anomaly → diagnosis → fix → resolution"); README Phase 0 (368–372 "beads as persistence", "every bead … carries `created_by`", "bead store handles task graph + cross-session"); component-inventory C19 row (`A20, A19e, A21b, B44`; depends on C01; gap G17; foundational yes).
> Inventory ID: C19   Kind: data-store   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C19 is the **bead store**: a durable, typed **work-graph** of units of work ("beads") with
**dependency edges** between them, persisting **across agent sessions**. It is Gas City concept #2
(AI-CONTEXT §3.2) and the "**work ledger**" half of the persistence layer (AI-CONTEXT §2) — the
**memory layer** that lets a restarted or new agent recover *what work exists, what it depends on, who
created it, and what state it is in* without re-deriving anything from a scratchpad. In v4's terms it is
the load-bearing native match for **P10 (memory layer)** and a primary carrier for **P9 (attribution)**.

**Responsibilities**
- Own the **persistent typed work-graph**: beads (nodes) + dependency edges, durable across sessions
  (AI-CONTEXT §3.2 #2; README:235 "Survives across agent sessions … Replaces flat scratchpads").
- Carry **universal attribution**: every bead records `created_by`, natively (README:227, 371; the "P9
  strongest match in the corpus", AI-CONTEXT §3.1).
- Support **typing of beads** via the bead schema registry (C20) — every bead has a *type*
  (`override`, `fix_task`, `factory_build_in_progress`, `factory_build`, …) that the store stores and can
  filter on (README:214, 257; AI-CONTEXT §16).
- Provide a **query interface** — `gc bd` commands (e.g. `gc bd find --type <t>`) for reading the
  work-graph by type/attribution/state, and **bead history** as the queryable audit trail
  (README:228, 242; AI-CONTEXT §16).
- Offer **two storage backends** behind one interface: **file** (Phase 0 default) and **Dolt** (later,
  versioned-SQL), selected by config `[beads] provider = "file"` (AI-CONTEXT §3.2 #2, §13.1, README:122).
- Hold **bead state/lifecycle** sufficient to support `gc converge resume <bead_id>` and the self-healing
  **bead chain** (anomaly → diagnosis → fix → resolution) and bootstrap **resume** of an in-progress build
  (AI-CONTEXT §16; README:259).

**Explicitly NOT**
- NOT the **bead *schema*** (C20). C19 stores and indexes typed beads; the *canonical definition* of each
  bead type and its fields lives in C20. C19 is the graph + persistence engine; C20 is the type catalog.
  (See §2 dependency note and OQ-C19-1 on the C19↔C20 direction.)
- NOT the **CXDB trajectory store** (C21). Beads are the **work ledger** (coarse-grained tasks/dependencies);
  CXDB is the **content-addressed turn-DAG** of fine-grained trajectories (AI-CONTEXT §2, §5; README:241,
  244 "CXDB adds content-addressed trajectory storage when self-healing needs richer trajectory analysis").
  Different granularity, different store. **Bead types are a *separate type space* from CXDB turn types**
  (AI-CONTEXT §5 keeps the two stores distinct); C19 asserts **no shared `{bundle_id,…}` namespace** with
  CXDB. Any bead↔CXDB payload binding is a C20/C22 concern, not C19's, and C19 takes no position on the
  bead `bundle_id` (see OQ-C19-5 and the bundle-id collision flagged to the integrator).
- NOT the **event bus** (C23). The event bus is append-only JSONL of *every action* (AI-CONTEXT §3.2 #3);
  beads are the *durable typed graph of work*. README:228 pairs "event bus + bead history" as two
  audit-trail sources; they are distinct components.
- NOT **dispatch** (C05/Sling), **molecules** (C13), or the **reconciler** (C18). Sling *routes* a
  bead/wisp to an agent; a molecule is a formula *instantiated into a bead-tree*; the reconciler converges
  bead state per tick. Those consume/produce beads but are separate components. C19 owns only the store.
- NOT **identity verification** (C41). C19 records the *self-asserted* `created_by` value natively; the
  *optional, deferred* "signature on bead provenance" that verifies the claimed actor is C41's concern
  (README:229 "optional, deferred"; see G36, §6).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | C19 is Gas City native concept #2; the `gc` binary provides the bead store and `gc bd` commands (AI-CONTEXT §3.2, §16; inventory: C19 depends on C01). |
| Upstream (depends on) | **C03** Config/feature-flags | `[beads] provider = "file"` (the backend selector) is a C03 section (AI-CONTEXT §13.1). C19's backend is config-gated. |
| Upstream-of (C20 depends on C19) | **C20** Bead schema registry | C19 stores *typed* beads; C20 defines the types. **Canonical direction (inventory): C20 depends on C19.** The dispatch brief's reversed arrow (C19→C20) is best read as "co-foundational," not a real reversal; the proposed co-foundational resolution lives in OQ-C19-1 / XC-1, not as a faithful fact here. |
| Downstream (consumes) | **C05** Sling, **C13** Molecule, **C18** Reconciler | route / instantiate / converge over beads stored here. |
| Downstream (consumes) | **C35** Override loop, **C39** Fix-task loop-closure, **C52** Self-bootstrap | write/read `override`, `fix_task`, `factory_build_in_progress` beads and the resolution **bead chain** (README:214, 257–259; AI-CONTEXT §16). |
| Downstream (consumes) | **C41** Identity/attribution, **C33** Satisfaction | C41 reads `created_by` off every bead (inventory: C41 depends on C19); C33 reads judge-output beads (README:426 "reading judge outputs from beads"). |

C19 is **foundational** (inventory: yes), in **Batch 1**, authored in parallel with C20/C21/C23 — it is the
work-graph schema/engine everything downstream references for "what work exists and who created it."

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; concrete signatures/schemas deferred to sweep 2.

1. **Bead write/create** — create a bead of a given **type** (C20-defined), with payload fields,
   `created_by`, and zero-or-more **dependency edges** to existing beads. (`fix_task` writing, README:257;
   `override` logging, README:214.)
2. **Bead read / find / query** — the `gc bd` surface: lookup by id, **filter by type**
   (`gc bd find --type factory_build_in_progress`, AI-CONTEXT §16), by `created_by` (attribution query),
   and by state. Returns beads and their dependency edges (the work-graph). (README:242.)
3. **Dependency-edge interface** — declare/inspect "bead A depends on bead B"; this is what makes it a
   *graph* and not a flat list (README:235, 239 "Tasks with dependencies").
4. **Bead state/lifecycle interface** — read/advance a bead's state enough to support **resume**
   (`gc converge resume <bead_id>`, AI-CONTEXT §16) and the self-heal **chain** to a `resolution`
   (README:259). Exact state machine is C18's (reconciler) concern at the convergence layer; C19 owns the
   *durable state field* and its transitions-of-record.
5. **Bead history / audit interface** — queryable per-bead history (README:228 "bead history") as one of
   the two attribution/audit sources (the other being the event bus, C23).
6. **Backend-selection interface** — `[beads] provider = "file" | "dolt"` chooses the storage engine behind
   the *same* bead interface (AI-CONTEXT §3.2 #2, §13.1).

**Invariants**
- **Attribution-native**: *every* bead carries a `created_by` — it is "automatic everywhere", with no
  configuration (AI-CONTEXT §3.1 P9; README:227, 371). v4 states the create path **always stamps** a
  non-empty `created_by`; it does not itself state the store *rejects* an un-attributed write.
  > [FAITHFUL-FILL] To make "total" *testable* without exceeding v4, the minimal faithful mechanism is
  > **stamping**: the C19 create path *always fills in* a non-empty `created_by` from the acting actor, so
  > no bead can exist without one. This is the smallest elaboration consistent with "native/automatic
  > everywhere" (a property of the *write path*, not of input validation). It is distinct from a *rejecting
  > validation gate* that refuses a caller-supplied null/empty `created_by` — that store-side rejection is
  > the explicit Track-B choice (C19-B DELTA-02) and is **not** asserted here as faithful.
- **Typed-total**: every bead has a type drawn from the C20 registry (no untyped beads;
  `gc bd find --type` presupposes every bead is type-tagged).
- **Durable across sessions**: a bead written in one session is readable, with its edges and state, by a
  later/other session (README:235; the defining property of "memory layer").
- **Backend-transparent**: the bead interface (write/find/depends-on/history) is identical whether the
  backend is `file` or `dolt`; backend choice changes durability/concurrency properties, not the contract
  (AI-CONTEXT §3.2 #2 "Dolt **or** file").

## 4. Data model / state

C19 **owns the work-graph state**: the set of beads, their typed payloads, their dependency edges, their
`created_by` attribution, and their per-bead state/history. This is the only component that *persists* the
work-graph.

**Bead (node) — faithful minimal field set** (fields v4 names or unambiguously implies; full per-type
schema is C20):

| Field | Source | Notes |
|---|---|---|
| `id` (bead id) | AI-CONTEXT §16 (`gc converge resume <bead_id>`) | stable handle used by resume/dispatch. |
| `type` | README:214, 257; AI-CONTEXT §16 | drawn from C20 registry (`override`, `fix_task`, `factory_build_in_progress`, `factory_build`, …). |
| `created_by` | README:227, 371 | universal attribution; native, mandatory. |
| dependency edges | README:235, 239 | "tasks with dependencies"; directed edges to other beads. |
| state | AI-CONTEXT §16; README:259 | enough to drive resume + the resolution chain. |
| payload fields | per-type | type-specific content (e.g. `transfused_from` on factory-build beads, AI-CONTEXT §16; the fix-task linkage on `fix_task`). C20 owns these. |
| history | README:228 | per-bead change history (audit). [FAITHFUL-FILL] README:228 names "bead history" as a *query/audit surface*; whether it is a stored field on the record or a *derived view* over C23/Dolt versioning is unspecified by v4 and deferred to sweep 2. |

> [FAITHFUL-FILL] v4 names `id`, `type`, `created_by`, dependency edges, state, and `transfused_from`
> (on bootstrap beads) but never enumerates a complete bead record. The minimal faithful field set above
> is exactly the union of fields v4 *uses* in commands/examples (§16, README:214/227/235/257/259); no
> field is invented beyond what a cited v4 operation requires. The authoritative per-type field list is
> deferred to **C20** (this is C19's storage view, not the schema catalog).

**Edges.** Dependency edges are directed bead→bead ("A depends on B"). The self-heal **chain**
(anomaly → diagnosis → fix → resolution, README:259) and the `fix_task` re-entry into the build flow are
expressed as edges/links between beads; C19 stores them, C20 names the link semantics per type.

> [AMBIGUITY] v4 names only an **untyped** "dependency" ("Tasks with dependencies", README P10) — it never
> states whether the self-heal chain uses *typed* edges or a single untyped depends-on edge with the
> distinction carried on the *node* type. The two faithful readings are: (a) one untyped `depends-on`
> edge, chain semantics inferred from node types (what §8 AC-4 below presumes); (b) typed chain edges —
> which is the elaboration C20-A §4.3 supplies as `diagnosed_by`/`produces`/`resolved_by`. The C19/C20
> faithful pair must agree on **one** model; today C19-A leans (a) and C20-A states (b). C19 stores
> whatever edges C20 names; the canonical edge-kind ownership and whether edges are typed is routed to the
> C19↔C20 interface freeze (OQ-C19-1) and the optimized siblings' edge-taxonomy OQ. No edge *names* are
> invented here.

**Backends.**
- **`file`** (Phase 0 default, AI-CONTEXT §13.1): single-node, local-file persistence; the smallest viable
  install (no Dolt server — AI-CONTEXT §3.4 "Explicitly off: … Dolt server").
- **`dolt`** (later): versioned-SQL backend (Dolt = git-for-data) for richer history/branching/concurrency.
  v4 names it only as the alternative provider behind the same interface; no migration procedure is given.

> [FAITHFUL-FILL] v4 states the *choice* "Dolt or file" and that Phase 0 uses `file` with the Dolt server
> off, but gives no file-layout, no schema-version, and no file→Dolt migration path. Minimal faithful
> position: C19 persists the work-graph in a Gas-City-owned on-disk representation under `[beads]
> provider`; the concrete file layout and any migration are Gas City internals (G11 — unverified) and are
> deferred to sweep 2 / the upstream `gastownhall/beads` repo, not invented here.

**Consistency.** v4 asserts durability and cross-session readability but specifies no isolation level,
concurrency model, or ordering guarantee for concurrent bead writes from parallel agents. Faithfully:
durable-and-readable across sessions is required; stronger consistency claims are not made by v4 (see §6
and OQ-C19-3).

## 5. Behavior

C19 has **no control loop of its own** (the loop that *acts on* beads is the reconciler C18; the loop that
*routes* them is Sling C05). C19's behavior is store-level:

- **Create**: an actor (agent/tool/city/rig) writes a typed bead with `created_by` and dependency edges
  (e.g. diagnosis agent writes a `fix_task`, README:257). The bead becomes durable immediately.
- **Query/recover**: a new or restarted agent recovers state by *querying* the graph rather than reading a
  scratchpad — e.g. cold-start recipe (AI-CONTEXT §16): `gc bd find --type factory_build_in_progress` →
  read `transfused_from` → `gc converge resume <bead_id>`. This is the "memory layer surviving sessions"
  in action.
- **State advance / chain**: a bead's state advances and new beads are linked as work proceeds; the
  self-heal **bead chain** records anomaly → diagnosis → fix → resolution as a connected sub-graph that
  *proves the fix worked* (README:259; the loop-closure contract itself is C39).
- **Audit read**: bead history + event bus give the queryable "who did what" record (README:228).

(Sequence/state diagrams for create/resume/chain and the file-vs-Dolt write paths are deferred to sweep 2
per BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance to C19 | Handling (faithful) |
|---|---|---|
| **G17** — *blocker*: no schema for the core stores; bead types are *used* (`override`, `fix_task`, `factory_build_in_progress`, `factory_build`) but never defined; `gc bd find --type factory_build_in_progress` references an undefined type | C19 is the store that *holds* these typed beads; the missing schema makes the type-filtered queries unbuildable. | **Split + defer to C20.** C19 faithfully owns the *graph engine, attribution, edges, persistence, and query-by-type surface*; the **canonical type catalog and per-type fields** are C20's deliverable (inventory assigns G17 to both C19 and C20). C19's contract is "every bead is typed and attributed and findable by type"; what the legal types *are* is C20. This is the minimal faithful division consistent with the inventory's two-component split. (See OQ-C19-1.) |
| **G36** — *minor*: attribution integrity is optional/deferred; without signed provenance, `created_by` is self-asserted | C19 records `created_by` natively but cannot *verify* it. | Faithful: C19 guarantees attribution is **present and total**; *verification* of the claimed actor is C41's "optional, deferred … signature on bead provenance" (README:229). C19 surfaces that the recorded actor is self-asserted (residual risk, §7/§9); inventing signing here would exceed v4 and duplicate C41. |
| **Backend durability / crash mid-write** | A `file`-backend write could be interrupted (single-node, Phase 0). | v4 claims durability but gives no crash/atomicity spec for the file backend; faithfully noted as a Gas City internal (G11 unverified) and an open question (OQ-C19-3). "Orders survive crashes" is claimed for Orders (C40), *not* for the bead file backend. |
| **Concurrent writes from parallel agents** | L4/L5 runs fan out many agents writing beads. | v4 states no concurrency/isolation model for the `file` backend; Dolt would add it. Faithful: flag as open (OQ-C19-3); do not invent locking semantics v4 does not state. |
| **Unknown / unregistered bead type** | A bead written with a type absent from C20's registry. | Faithful: by the **typed-total** invariant every bead's type must be in C20's registry; enforcement of "reject unknown type" is the C19↔C20 contract, finalized once C20 exists (sweep 2). **Caveat (G11 / OQ-C20-4):** closed-type enforcement presupposes Gas City's native bead store *rejects* unregistered `type` strings — unverified. If the substrate accepts free-form types, this enforcement becomes pack work (C02), not a native guarantee. |

No v4 F-mode is *owned* by C19 beyond the persistence/attribution role; F32 (mail-injection) and the
attribution F-modes are addressed via P9 `created_by` flowing through beads (C41 owns the security framing).

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security**: C19 is the attribution substrate — "every action carries identity … native `created_by`"
  (README:227) — but attribution is **self-asserted** until C41's optional signing is added (G36). The
  bead store is also a write target for auto-generated `fix_task`/factory-build beads at L4/L5; integrity
  of *that* write path is part of the broader RSI/goal-subversion concern (G35, owned by C57/C56), not
  resolved in C19.
- **Cost**: negligible direct storage cost at Phase 0 (`file` backend, single node). Dolt adds operational
  cost only when adopted. No v4 cost model touches beads (G32 is about model tokens, not bead storage).
- **Scale**: the `file` backend is single-node (Phase 0); v4 offers Dolt as the scale/concurrency path but
  pins no thresholds. The agent-side throughput ceiling (G34) is a Max-seat concern, not a bead-store one.
- **Observability**: bead history + `gc bd` queries are themselves the observability surface for the
  work-graph ("read patterns from memory", README:242). The store *is* queryable by design.
- **Ops**: backend selection is a one-line config change (`[beads] provider`); migration file→Dolt is
  unspecified by v4 (OQ-C19-2). Gas City schema-drift (AI-CONTEXT §3.5, "1–2 breaking pack-schema/
  formula-format changes per quarter") is an ops risk for the bead record shape (sweep 2: pin a schema
  version with C20).

## 8. Acceptance criteria & test strategy

1. **Attribution-native**: every bead created through the C19 interface has a non-empty `created_by` —
   the create path always **stamps** one from the acting actor ("native, automatic everywhere",
   README:227/371). The minimal testable form of this is that no bead is ever persisted without a
   non-empty `created_by` because the write path fills it in (stamping, FAITHFUL-FILL §3). The *store-side
   rejecting validation gate* on an externally-supplied null is the Track-B enforcement (C19-B DELTA-02),
   not a v4-stated fact.
2. **Cross-session durability**: a bead (with type, edges, state) written in session S1 is readable —
   identical — from a separate session S2 after process restart (the "survives across sessions" property,
   README:235).
3. **Type-filtered query**: `gc bd find --type <t>` returns exactly the beads of type `<t>` and no others,
   for every type registered in C20 — specifically including `factory_build_in_progress` (the §16 recipe
   must run end-to-end once C20 lands).
4. **Dependency graph**: declaring "A depends on B" and "B depends on C" yields a queryable directed graph;
   the self-heal chain (anomaly→diagnosis→fix→resolution) is recoverable as a connected sub-graph
   (README:259).
5. **Resume handle**: a `factory_build_in_progress` bead's `id` and state are sufficient for
   `gc converge resume <bead_id>` to pick the work back up (AI-CONTEXT §16).
6. **Backend transparency** *(sweep-2 / Dolt-era; G11-gated)*: the same test suite (1–5) passes against
   both `provider = "file"` and `provider = "dolt"` with identical observable contract. Not exercisable at
   sweep 1 — Phase 0 turns the Dolt server "explicitly off" (AI-CONTEXT §3.4) and the Dolt backend itself
   is unverified Gas City behavior (G11). Stated now so the contract is frozen; tested when Dolt lands.
(Concrete bead record schema, `gc bd` signatures, edge/link semantics per type, and file-layout/migration
test vectors are sweep-2 deliverables, jointly with C20.)

## 9. Open questions

- **OQ-C19-1** (→ review-log): **C19↔C20 dependency direction / G17 split.** The inventory lists *C20
  depends on C19*; the dispatch brief lists *C19 depends on C20*. They are a mutually-dependent foundational
  pair (a typed store needs a type catalog; a type catalog needs a store to live in). Faithful resolution:
  treat them as co-foundational and freeze the **C19↔C20 interface** (a bead has `{id, type, created_by,
  edges, state}`; C20 supplies the legal `type` set and per-type fields) *before* either is built, so the
  cycle is broken at the contract, not the implementation. Needs explicit confirmation of which doc's
  direction is canonical.
- **OQ-C19-2** (→ review-log): **file → Dolt migration is unspecified.** v4 names both backends behind one
  interface but gives no migration path, file layout, or schema versioning. Is a faithful migration spec in
  scope, or is it a Gas City internal deferred upstream (G11 — Gas City behavior unverified)?
- **OQ-C19-3** (→ review-log): **Concurrency / crash semantics of the `file` backend.** v4 asserts
  durability + cross-session readability but states no isolation level, write atomicity, or ordering for
  concurrent multi-agent bead writes at L4/L5 fan-out. Needed before parallel write contracts can be
  asserted; today flagged, not invented.
- **OQ-C19-5** (→ review-log): **Bead `bundle_id` / CXDB type-namespace (XC-4, DEFERRED to integrator).**
  C19 faithfully treats bead types as a *separate* type space from CXDB turn types and asserts no shared
  bundle namespace. But the optimized siblings collide: C20 binds beads to `v4.beads.v1`, C22-faithful uses
  `softwarefactory.v4`, C22-optimized claims one registry owning *both* bead and CXDB namespaces under
  `strongdm.factory.v4`, and C21-optimized names `softwarefactory.trajectory.v1`. C19 takes no position on
  the bead `bundle_id`; the canonical namespace ruling and whether bead types are registered in C22 at all
  belong to C20/C22 + the integrator. Recorded so C19's *silence* is not read as assent to C22 owning the
  bead namespace. **The collision is not merely a string disagreement — it is an *ownership* fork:** C20-B
  asserts "two registries, one mapping" (C20 owns bead-type schemas and *binds* each to a CXDB bundle),
  while C22-B asserts "one registry, two namespaces" (C22 is the single source of truth that *owns* the
  per-type bead payload schemas, `kind: bead`). Both currently define the `fix_task`/`override` payload
  schema. The integrator must resolve *who authors bead-type schemas* before any bundle string can be
  pinned; C19 recommends C20 authors them and C22 hosts the registration mechanism (see review).
- **OQ-C19-4** (→ review-log): **Attribution integrity (G36).** `created_by` is self-asserted in C19;
  C41's signed provenance is "optional, deferred." For an L5 self-modifying factory, is unsigned
  attribution acceptable as the *only* integrity control, or must the C19↔C41 seam reserve a place for
  signing now? (Faithfully recorded as residual risk; resolution belongs to C41/C57.)
