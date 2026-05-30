# C17 — Tool-node Abstraction  (Build Plan, Track B)

> Source / Spec ref: [`spec-optimized/C17-tool-node-abstraction.md`](../spec-optimized/C17-tool-node-abstraction.md)

## 1. Work breakdown

| id | description | size | prereqs |
|---|---|---|---|
| T1 | **Adopt-vs-define spike (OQ1/G11).** With a `gc` install, observe whether Gas City's native tool-bead mechanism already provides a registry / typed interface / caching. Output: a note deciding whether C17 *defines* the registry+facade or *adopts-and-extends* an existing native one. Gates DELTA-01/02 framing. | M | C01 install; C02 T1 |
| T2 | **Freeze the `NodeInterface` descriptor** (DELTA-02): `node_id`, `version`, input/output schema refs, `determinism_class`, `capability_needs`, `origin`, `falsifying_scenario_ref`, `abi_version`. This is the caller-facing contract every formula and downstream pack binds to. | M | T1; C02 `ToolNodeManifest` (C02 M2) |
| T3 | **Freeze the `determinism_class` taxonomy** (DELTA-03): pure / capability-scoped-deterministic / nondeterministic; the cacheability + replay + guard implications of each. | S | T2 |
| T4 | **Specify the `ToolNodeRegistry`** (DELTA-01/05): `register`/`resolve`/`list`/`is_enabled`; native+pack parity invariant; global `node_id` uniqueness + fail-closed collision. | M | T2 |
| T5 | **Specify the `invoke` facade** (DELTA-01): input validation → cache check → C02 wire delegation → output validation → exit-code→`status` mapping → `NodeResult`. Explicitly *delegates* to C02's `ToolNodeRequest`/`ToolNodeResponse` + exit-code taxonomy; does not redefine them. | M | T2,T3; C02 wire freeze (C02 M1) |
| T6 | **Specify the result cache** (DELTA-04): key `(node_id, node_version, input_hash, granted_caps_hash, abi_version)`; bypass for `nondeterministic`; eviction/persistence as C03 config; resolve the C17-vs-C49 ownership question (OQ2). | M | T3,T5; C49 seam; C03 seam |
| T7 | **Specify the C16 guard-metadata hook** (DELTA-06): `falsifying_scenario_ref` is a queryable registry field; C16 reads it from `list`, not from prose. | S | T2,T4; C16 seam |
| T8 | **Stub registry + facade harness:** an in-memory registry pre-loaded with a fake native bead + a fake pack node, and an `invoke` that drives C02's stub harness. Lets every downstream pack (C10/C14/C24/C31/C33/C36–38/C44/C47–48) bind to `node_id` and test before C01/C02 specifics settle. | M | T2,T4,T5; C02 stub harness (C02 T8) |
| T9 | **Parity + cache conformance suite:** acceptance §8 as runnable tests — native↔pack parity, typed binding, determinism partitioning, cache hit/miss, collision fail-close, C02 exit-code mapping, determinism-honesty/replay, attribution carriage. | L | T4,T5,T6,T8 |
| T10 | **Sweep-2 deepening:** Mermaid invocation sequence (caller→C17→C02→C01→node and back), registry/cache JSON schemas, active-determinism-check decision (OQ3), service-node boundary (OQ4). | M | T2–T7 |

## 2. Dependency graph

- **Hard upstream:** **C02** — C17's `invoke` serializes through C02's wire ABI and its registry consumes C02 `ToolNodeManifest`s. C17's wire-facing tasks (T5) cannot freeze before C02's M1 (request/response + exit-code) and its registry tasks (T2/T4) need C02's M2 (`ToolNodeManifest`). **C01** — native tool beads + subprocess spawning. T1 (adopt-vs-define) needs a `gc` install, inheriting C02's OQ1/G11 verification debt one layer up.
- **Seam co-dependencies (co-designed, not blocking):** **C03** (which nodes enabled; cache persistence/eviction config), **C49** (replay — cache may be a view over C49's store; OQ2), **C16** (discipline linter reads guard metadata; T7), **C43** (capability enforcement — threaded, not owned). These are contract touchpoints, run jointly.
- **Critical path:** **T1 → T2 → T4 → T5 → T8 → T9.** The descriptor + registry + facade + stub harness is the spine every deterministic step in the system binds to. T2 (`NodeInterface` freeze) is the single highest-leverage unblock — it is the contract C12 formulas and all pack-shaped components reference.
- **Downstream gated on C17 contract freeze (T2/T4/T5):** C12 (formula step→node binding), C05/C18 (invocation), and every pack-shaped component that registers a node (C10, C14, C15, C16, C24, C30, C31, C33, C36, C37, C38, C44, C47, C48). C49 (replay) gated on T3/T6.

## 3. Parallelization

Once **T1** lands and C02's M1/M2 are visible, three workstreams run concurrently:

1. **Descriptor/registry stream:** T2 → T4 → T7. Defines what callers bind to. The spine.
2. **Invocation/cache stream:** T5 → T6 → (feeds T9). The call path + cost lever; meets stream 1 at the `NodeInterface` and at C02's wire freeze.
3. **Determinism stream:** T3, feeding both the cache (T6) and the C49/C16 seams. Small but cross-cutting.

T8's stub harness, once published, fans out the *entire downstream architecture* — each pack-shaped component (≈14 of them) builds against it independently. T9's conformance suite is partitionable by acceptance criterion (each §8 item is an independent test), and the parity test (criterion 1) is itself a 2-way fan-out (build a fake native bead and a fake pack node, prove they're indistinguishable).

## 4. Interfaces-first / contract milestones

Freeze early, in this order, to unblock maximum downstream fan-out:

1. **M1 — `NodeInterface` descriptor + `determinism_class` taxonomy frozen (T2+T3).** The single contract every formula step and downstream pack binds to. Highest-priority freeze; publish as versioned schema. Depends on C02's M1/M2 being visible.
2. **M2 — `ToolNodeRegistry` ops + parity/collision invariants frozen (T4).** Unblocks formula authoring (C12) and operator tooling.
3. **M3 — `invoke` facade + `NodeResult` + exit-code→status mapping frozen (T5).** The runtime call contract C05/C18 drive; pins C17↔C02 delegation.
4. **M4 — stub registry+facade harness published (T8).** Lets all ~14 downstream pack-shaped components develop and green-test against C17 without a working C01/C02 — the maximal parallelism unlock for the whole architecture.

## 5. Risks & de-risking order

| order | risk | de-risk action |
|---|---|---|
| 1 | **OQ1/G11 — is C17 a real layer or a thin facade?** If Gas City natively provides registry+typing+cache, T2/T4 become adopt-and-extend, and over-building duplicates the native mechanism. | **T1 spike first**, jointly with C02's T1 `gc`-install spike (shared install, one trip). Decide define-vs-adopt before any schema freeze. |
| 2 | **OQ2 — cache ownership straddles C17/C49.** Building a separate C17 cache that duplicates C49's content-addressed trajectory store is waste; making C17's cache a view over C49 couples them. | Joint design touchpoint with C49 owner during T6; pick one store, make the other a view. Resolve before the cache schema freezes (T10). |
| 3 | **Determinism dishonesty → cache poisoning.** A mislabeled `pure` node returns stale results. | Bake `granted_caps_hash` into the cache key (T6) so cap-scoped nodes can't share keys across grants; rely on C49 replay-divergence detection; decide active-vs-passive checking in T10 (OQ3). |
| 4 | **OQ4 — service-shaped nodes (C24 watch-loop, C44 twin) don't fit single-shot `invoke`.** | Coordinate with C02 OQ4 + C44; decide in T10 whether C17 catalogs `[[service]]` nodes (one registry) or stays tool-node-only (separate service registry) before C24/C44 commit. |
| 5 | **Registry collision / native-shadowing by a pack.** | Global `node_id` uniqueness + fail-closed-on-collision at load (T4), surfaced through C02's pack-load failure path — no silent override. |

## 6. Definition of done

**Per-component (C17 sweep-1):**
- Spec §3 contracts named: `NodeInterface` (3a), `ToolNodeRegistry` (3b), `invoke` facade + cache (3c); each layers *on top of* C02 without redefining the wire format or grant mechanism.
- Every acceptance criterion in §8 has a corresponding planned test in T9.
- The four open questions recorded in the spec and mirrored to [`_meta/review-log.md`](../_meta/review-log.md); OQ1 flagged as the top blocker (decides built-component vs documented-facade).

**Per-task DoD:**
- **T1:** a written adopt-vs-define verdict for C17, citing observed Gas City native tool-bead behavior.
- **T2/T3:** versioned `NodeInterface` + `determinism_class` schema merged; no downstream component binds to an entrypoint path instead of a `node_id`.
- **T4:** registry ops specced with parity + global-uniqueness + fail-closed-collision invariants; a native bead and a pack node are demonstrably resolvable through one path.
- **T5:** `invoke` correctly maps every C02 exit code to a typed `NodeResult.status`; delegates to (never reimplements) C02's wire ABI.
- **T6:** cache key includes all five components; `nondeterministic` nodes bypass; C17-vs-C49 ownership ruled.
- **T8:** a downstream team builds and green-tests a pack-registered node against the C17 stub with no running C01/C02.
- **T9:** all §8 criteria pass as automated tests; native↔pack parity, cache hit/miss, and collision fail-close are proven.
