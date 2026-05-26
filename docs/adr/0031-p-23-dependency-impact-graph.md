# ADR 0031: P-23 dependency-impact graph

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1b parallel fanout)

## Context

Three candidates claim P-23 as a load-bearing substrate primitive: [BF-S/S-2](../../architectures/v3/tracks/brownfield-substrate-first.md) consumes it directly as the per-symbol blast-radius store the V&V step queries every cycle; [BF-L](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md) composes it inside the [P-26 Codebase Model](../../architectures/v3/primitives/P-26-codebase-model.md) as the structural-dependency view; and [U-C](../../architectures/v3/tracks/unified-C.md) reads it via the [P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) to compute graph-distance to a frozen anchor. The [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage) rates P-23 shared-by-3 and earmarks it for a common ADR. The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-23-dependency-impact-graph.md) verdicts the primitive `designed-system` — per-language reference / call / type / data-flow facts are commodity; the load-bearing design content is (i) the typed-edge schema that unifies impact-specific relations across languages, (ii) the role-visibility predicates that fold into transitive-closure queries, and (iii) the rate-limited side-channel posture against partition-leakage.

The forcing failure modes are [F34 — cross-layer drift](../../architectures/v3/failure-modes-v3.md#3-f34-f35--round-3-promotions) (brownfield severity *critical*) and [F35 — federation-as-family drift](../../architectures/v3/failure-modes-v3.md#3-f34-f35--round-3-promotions) (brownfield severity *high*); BF-S §1.S-2 makes the explicit claim these are unaddressable without substrate-level blast-radius compute. Secondary forcing mode is [F37 — silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md#f37--silent-contradictory-prompt-collapse), detectable when a proposed diff's forward closure reaches a latent invariant elsewhere in the call graph.

## Decision

**Build P-23 on Glean (the P-22 fact-store from [ADR 0017](./0017-p-22-polyglot-codebase-index.md)) by extending its predicate set with a typed-edge namespace for impact-specific relations, and by defining transitive-closure rules in Angle over the per-language `Reference` / `Call` / `Inherits` / `DataFlow` predicates Glean's tree-sitter indexers already populate.** P-23 does not stand up a second graph backend: it is a *schema layer* and *query-rule layer* on the same Glean store P-22 maintains.

Concretely, the substrate adds:

- A typed-edge namespace declaring impact-relations Glean's per-language schemas do not natively carry — for example `predicate TestCovers(t: Symbol, s: Symbol)`, `predicate FeatureFlagGates(flag: Symbol, s: Symbol)`, `predicate ConfigReads(s: Symbol, k: ConfigKey)`. [Stack Graphs](https://github.com/github/stack-graphs) emits the cross-language name-binding facts joining per-language references into one symbol namespace.
- Transitive-closure rules: `predicate forward_call_closure(s: Symbol, c: Symbol)` and `reverse_call_closure(...)` as Angle Datalog derivations over the union of edge predicates, parameterised by an edge-type filter set.
- A role-visibility predicate `visible_to(s: Symbol, r: Role)` that closure rules join against, so closures returned to a builder-role token traverse only role-visible nodes. The hidden-node count is exposed as a rate-limited side channel ("N hidden-impacted symbols; escalate to V&V") rather than being either silently dropped (breaks F34 detection) or fully revealed (defeats holdout discipline).

The query API exposes `forward_closure(s, edge_types) → set<Symbol>`, `reverse_closure(...)`, and `impact(diff) → ranked set<Symbol × edge-path>`. Incremental maintenance falls out of Glean's append-only fact model + tree-sitter's edit-proportional re-parse.

## Alternatives considered

**B. Neo4j as a standalone graph database, populated by a separate ingestion pipeline.** Recursive Cypher (`MATCH (s)-[:CALLS*]->(t)`) realises transitive closure directly, and Neo4j's tooling is mature. *Why rejected:* this duplicates the fact universe Glean already maintains for P-22. Two ingestion pipelines reading the same source means two drift surfaces — when Glean reflects commit *N* and Neo4j reflects commit *N − k*, blast-radius answers and codebase-index answers disagree, and which one is "right" is a deploy-environment accident. Building P-23 on Glean keeps one fact-store, one freshness clock, and one set of indexer bugs. The Neo4j path remains a documented fallback in the buildability sketch for languages outside Glean / Stack Graphs coverage, but not as the primary substrate. See [P-23 sketch — fallback path](../../architectures/v3/primitives/P-23-dependency-impact-graph.md#construction-path).

**C. LSP servers only (query-time blast radius via `textDocument/references` and `callHierarchy/incomingCalls`).** *Why rejected:* same shape as the alternative rejected for P-22 in [ADR 0017](./0017-p-22-polyglot-codebase-index.md#alternatives-considered) — LSP is a query-time protocol over live compilation state, not a durable index. There is no cross-language join (each LSP server only knows its own language), no place to store the impact-specific typed edges (`TestCovers`, `FeatureFlagGates`) that are not standard LSP concepts, and no way to materialise multi-hop transitive closures cheaply. LSP remains useful as a type-resolution feeder into Glean's facts, exactly as in P-22; it is not the substrate.

## Consequences

**Easier:** [BF-S/S-2](../../architectures/v3/tracks/brownfield-substrate-first.md)'s blast-radius query is a single Angle query against the shared store. [BF-L's P-26 Codebase Model](../../architectures/v3/primitives/P-26-codebase-model.md) inherits the dependency view without a second backend; the structural / historical / conventional / runtime / invariant / debt views compose as additional Glean schemas on the same fact-store. [U-C's P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) reads `graph_distance` straight off the closure predicates. Single freshness clock across P-22 and P-23 closes one whole class of cross-substrate disagreement bugs.

**Harder:** Angle / Datalog derivation authoring for the closure + role-visibility rules is the named cost — Glean's schema and rule surface is not commodity. Mitigation: the impact-namespace schema and the closure-rule pack ship as starter content, versioned alongside P-22's per-language schemas.

**Explicitly NOT promising:** that partition-leakage is eliminated. The transitive closure of a connected graph carries hidden-node information by count, edge-type, and path-length even with `visible_to` filtering; the rate-limited side channel is a *designed-system* answer, not a clean fix. This carries forward as a research-grade uncertainty flag from the [P-23 sketch §"Partition-leakage risk"](../../architectures/v3/primitives/P-23-dependency-impact-graph.md#partition-leakage-risk-b7-robust-claim-engaged-honestly). Also not promised: uniform cross-language fidelity for ad-hoc FFI / JNI / ctypes bindings outside Stack Graphs' curated pairs and outside schema-mediated RPC.

## References

- [P-23 buildability sketch](../../architectures/v3/primitives/P-23-dependency-impact-graph.md) — full construction-path enumeration, partition-leakage analysis, fidelity ceiling
- [Phase-4.2 overlap verdict on P-23](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage) — shared by 3 (BF-S, BF-L via P-26, U-C via P-32)
- [ADR 0017: P-22 polyglot codebase index](./0017-p-22-polyglot-codebase-index.md) — the Glean fact-store P-23 extends
- [F34 cross-layer drift and F35 federation-as-family drift](../../architectures/v3/failure-modes-v3.md#3-f34-f35--round-3-promotions) — forcing failure modes
- [BF-L Codebase Model (P-26)](../../architectures/v3/primitives/P-26-codebase-model.md) and [U-C distance estimator (P-32)](../../architectures/v3/primitives/P-32-distance-estimator.md) — downstream composers
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.1b parallel-fanout ADR pattern
