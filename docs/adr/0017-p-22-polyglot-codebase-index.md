# ADR 0017: P-22 polyglot codebase index

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a parallel fanout)

## Context

Four candidates claim P-22 as a load-bearing substrate primitive: [BF-S/S-1](../../architectures/v3/tracks/brownfield-substrate-first.md) (continuously-maintained index queried every cycle), [BF-M Stage-2 Comprehension](../../architectures/v3/tracks/brownfield-methodology-first.md) (code-traversal capability feeding the archaeological brief), [BF-L Codebase Model](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md) (the *structural view* component of P-26), and [U-C](../../architectures/v3/tracks/unified-C.md) (via P-32 distance estimator which reads the fact-store to compute graph-distance to a frozen anchor). The [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#shared-substrate-primitives) rates P-22 shared-by-4 and earmarks it for a common ADR. The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md) verdicts the primitive `designed-system` — the per-language parsers and the storage backend are commodity; the load-bearing design content is (i) how facts from many languages are reconciled into one queryable surface, (ii) the slice-sized query contract that makes the F21 mitigation real, and (iii) the per-language fidelity calibration callers must respect.

The forcing failure modes are [F21 — context-window exhaustion](../../architectures/v3/failure-modes-v3.md#f21--context-window-exhaustion--silent-degradation) (brownfield severity *critical*) and [F61 — context fragmentation across agents](../../architectures/v3/failure-modes-v3.md#f61--context-fragmentation-across-agents) (brownfield severity *high*). The index is the substrate's structural answer: agents query a persisted artifact and receive scoped slices instead of re-loading the repo.

## Decision

**Build P-22 on [Glean](https://github.com/facebook/Glean) as the durable polyglot fact-store, with tree-sitter parsers as the per-language indexer frontends emitting facts into Glean's schemas.** Glean is Meta's open-source code-knowledge system: an append-only fact-store on RocksDB, typed per-language schemas, and an Angle/Datalog query language whose `glean derive` cross-language derivation rules materialise polyglot queries ("all callers of an exported symbol, regardless of caller language") as a single derived predicate. Tree-sitter supplies incremental AST parsing for ~40 languages on every push — `Parser.parse(source, old_tree)` runs in time proportional to the edit — and emits symbol/definition/reference facts conforming to per-language Glean schemas. Per-language type queries delegate to LSP servers (`pyright`, `gopls`, `rust-analyzer`, `typescript-language-server`) whose responses are cached back as Glean facts.

The substrate exposes one query API across languages — `find_definition`, `find_references`, `list_symbols_in_file`, `resolve_type`, `list_callers(symbol_id)` — and returns **slices sized to the caller's context budget**, not full file dumps. The slice-sized contract is the load-bearing F21 mitigation: a "give me everything" return shape would defeat the index's reason for existing.

## Alternatives considered

**B. Sourcegraph + SCIP indexers as the primary substrate.** Sourcegraph publishes the SCIP protocol and ships per-language SCIP indexers; the API is a polyglot GraphQL surface deployed at scale across enterprise monorepos (Stripe, Uber, Lyft). *Why rejected:* Sourcegraph's open-source core was substantively narrowed and the project's commercial trajectory has reduced its viability as a freely-extensible polyglot substrate; downstream callers (BF-L's P-26, U-C's P-32) need to add new derived predicates and per-language fact tables, which is structurally easier against Glean's Datalog derivations than against Sourcegraph's resolver layer. See [P-22 sketch — Sourcegraph option](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md#construction-path).

**C. Per-language indexers without a unifying fact-store (federated query at read-time).** A thin facade that fans queries to per-language LSP servers and merges results. *Why rejected:* this defeats the polyglot contract — cross-language queries ("all callers of a Python-exported symbol, including Java/Go callers") need a *durable joined* fact-store; query-time federation can't materialise the join cheaply, and the F21 slice-sized contract breaks when each backend independently chooses what to return. The buildability sketch's [polyglot fidelity gap](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md#polyglot-fidelity-gap) names this directly.

**D. LSP servers as the primary backend (no separate index layer).** *Why rejected:* LSP is a query-time protocol over a *live* compilation state; it is not a durable index. Restarting a server reloads from source; queries that need ranking by historical reference counts or cross-cycle stability have no place to read from. P-22's contract demands a persisted artifact; LSP fills the *type-resolution* role within that architecture but cannot be the substrate.

## Consequences

**Easier:** F21 and F61 mitigations become substrate-enforced — agents query slices rather than re-grepping. [BF-L's P-26 Codebase Model](../../architectures/v3/primitives/P-26-codebase-model.md) inherits P-22 directly as its structural view substrate; the other five views (conventional, historical, runtime, invariant, debt) compose on top of the same fact-store via additional Glean schemas. [U-C's P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) reads `graph_distance` straight from P-22's reference table via an Angle query, with no separate code-graph build. BF-S/S-1's continuous-maintenance loop is incremental-by-construction (tree-sitter edit-proportional re-parse → append-only fact write).

**Harder:** Glean's operational complexity is the named cost — Datalog schema authoring, derivation-rule maintenance, and RocksDB ops are not commodity skills. Mitigation: ship per-language schemas as starter content; treat schema evolution as a versioned interface (callers depend on schema versions, not on raw facts).

**Explicitly NOT promising:** uniform polyglot *type* fidelity. The [polyglot fidelity gap](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md#polyglot-fidelity-gap) is real: symbols/references are uniform; types are per-language variable; cross-language type resolution at RPC boundaries is essentially nil. Downstream consumers (BF-M's archaeological brief; U-C's distance estimator) must be told what fidelity they get per language. This calibration is a *contract obligation on callers*, not a substrate bug.

## References

- [P-22 buildability sketch](../../architectures/v3/primitives/P-22-polyglot-codebase-index.md) — full construction-path enumeration and fidelity gap
- [Phase-4.2 overlap verdict on P-22](../../architectures/v3/primitives/overlap.md#shared-substrate-primitives) — shared by 4 (BF-S, BF-M, BF-L via P-26, U-C via P-32)
- [F21 context-window exhaustion](../../architectures/v3/failure-modes-v3.md#f21--context-window-exhaustion--silent-degradation) and [F61 context fragmentation](../../architectures/v3/failure-modes-v3.md#f61--context-fragmentation-across-agents) — forcing failure modes
- [BF-L Codebase Model (P-26)](../../architectures/v3/primitives/P-26-codebase-model.md) — composes P-22 as structural view
- [U-C distance estimator (P-32)](../../architectures/v3/primitives/P-32-distance-estimator.md) — reads P-22 fact-store for graph-distance
- [Primitives index](../../architectures/v3/primitives/index.md) — registry: High
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.1a parallel-fanout ADR pattern
