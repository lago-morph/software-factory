# P-23 — Dependency-and-impact graph

**Dispatch tier.** per-primitive (designed-system).
**Claimed by.** [BF-S/S-2](../tracks/brownfield-substrate-first.md), component-of [BF-L Codebase Model](../tracks/brownfield-legacy-ingestion-first.md), used by [U-C distance estimator](../tracks/unified-C.md).

## Contract restatement

A substrate primitive maintaining a per-symbol / per-module directed graph of reference / call / type / import / data-flow edges, queryable as **per-symbol blast-radius** (`forward_closure(s) → set<Symbol>`, `reverse_closure(s) → set<Symbol>` with edge-type filters) and **per-change impact** (`impact(diff) → ranked set<Symbol × edge-path>`). The graph is **cross-language** — references crossing language boundaries (Python → Rust extension; TypeScript → Go backend via OpenAPI; JVM JNI) resolve into the same symbol namespace. Incrementally maintained on every commit; transitive-closure query API with bounded latency at typical brownfield scale. Per BF-S §1.S-2, partition is role-keyed: builders see the same edges but only role-visible symbols.

## Construction path

**Primary: Glean (Meta open-source) as Datalog-backed graph store, with Stack Graphs (GitHub) as cross-language reference resolver feeding Glean's symbol predicates.** Glean stores typed facts and exposes Angle (Datalog-like) queries; the substrate defines `predicate forward_call_closure(s: Symbol, c: Symbol)` and `reverse_call_closure(...)` as transitive-closure rules over per-language `Reference` / `Call` predicates Glean's indexers populate. Stack Graphs emits name-binding facts composable across languages via a shared scope-graph algebra; bindings are written into Glean as `CrossLangBinding` facts. **Integration sentence:** Glean's Angle query `forward_call_closure(S, C) where Function.name == "charge"` returns the transitive forward call graph well under a second on multi-million-LOC repos (Meta's www monorepo is documented scale); cross-language fidelity comes from `CrossLangBinding` facts joining per-language `Reference` predicates inside the same Datalog evaluation.

**Alternative: CodeQL (GitHub) semantic-query substrate.** CodeQL extracts per-language databases and exposes QL over typed predicates including `Call`, `DataFlow::Node`. **Integration sentence:** `Call.getATransitiveCallee()` realises per-language transitive closure directly; the design content is a cross-language federation step over a shared symbol-URI scheme (typically an OpenAPI/Protobuf/gRPC schema registry as the inter-language reference fabric).

**Fallback: tree-sitter + custom graph on Neo4j (recursive Cypher `MATCH (s)-[:CALLS*]->(t)`) or Postgres recursive CTEs** — for languages outside Glean / CodeQL coverage, and also the BF-L Codebase Model composition path (same graph layer carries structural / historical / conventional edges alongside dependency edges). **Prior art.** Glean at multi-million-LOC scale; Stack Graphs behind GitHub code navigation; CodeQL behind GitHub Advanced Security.

## Partition-leakage risk (B7 ROBUST claim, engaged honestly)

BF-S §1.S-2 asserts substrate-enforced role-partition; the [brownfield red-team §2 Attack 1](../bias-guards/phase-3/brownfield/red-team.md) shows **the codebase is a connected graph; the partition leaks via dependency edges**. A builder fixing `payments/charge.py` queries `forward_closure("charge")` and the closure reaches `test_charge.py::test_replay_2024_11_incident` — a held-out scenario. The substrate must either (a) return the edge and leak the held-out test's existence + approximate purpose, or (b) hide the edge and break F34 cross-layer-drift detection. **Assessment: structural, partially mitigable but not eliminable.** Glean / CodeQL / Neo4j all permit filtering closure by role-visible symbol set (Glean: an Angle `visible_to(s, r)` predicate joined into the closure rule), reducing the leak to a **count-and-aggregate side channel** ("N hidden-impacted symbols; escalate to V&V"). The count is itself a side channel; rate-limiting it is a designed-system answer, not a clean fix. The structural fact that any non-trivial transitive closure carries information about hidden nodes does not go away.

## Cross-language fidelity

Stack Graphs resolves a curated set of language pairs (Python ↔ TypeScript ↔ Java ↔ Ruby ↔ C#); pairs outside it degrade to text-match. Schema-mediated references (OpenAPI / gRPC / Protobuf / GraphQL) are tractable because the schema is a first-class graph artifact; ad-hoc bindings (FFI, JNI, ctypes, shell-out, RPC-by-convention) are not. **Fidelity ceiling: high for schema-mediated polyglot; medium for stack-graph-supported pairs; low for ad-hoc FFI.** BF-S §4 OQ-T2 concedes polyglot S-2 fidelity is uneven.

## Per-candidate notes (no same-vs-distinct verdicts)

- **BF-S / S-2.** One of five substrate stores; the V&V step compares the proposed diff against S-2's predicted blast radius and escalates discrepancies ([brownfield-substrate-first §1.3 step 6](../tracks/brownfield-substrate-first.md)). Role-partition asserted by track; red-team contests.
- **BF-L (component of Codebase Model).** The structural view composes S-2 with P-22 and P-24; maintenance loop refreshes incrementally on every push. BF-L's partition lives at the model-query interface — different design point from BF-S's substrate-level assertion.
- **U-C (distance-estimator component).** The estimator's `blast-radius` component is `|forward_closure(diff.touched_symbols)| × test_coverage_gap` per [unified-C](../tracks/unified-C.md); P-23 is one of three typed substrate inputs. U-C is robust to fidelity gaps (low-fidelity blast-radius makes the estimator conservative) but *not* robust to substrate-level leakage — U-C presumes honest closure queries.

## Corpus-why citation

Load-bearing: **[F34 — Cross-layer drift](../failure-modes-v3.md#3-f34-f35--round-3-promotions)** (brownfield-critical) and **[F35 — Federation-as-Family drift](../failure-modes-v3.md#3-f34-f35--round-3-promotions)** (brownfield-high). BF-S §1.S-2 makes the explicit corpus claim that F34 / F35 are unaddressable without substrate-level blast-radius compute. Secondary: **F37 silent contradictory-prompt collapse**, where the contradiction is between a proposed diff and a latent invariant elsewhere in the call graph, is detectable via blast-radius traversal at diff time.

## Research-grade-uncertainty flag

Two axes flagged; the primitive itself remains `designed-system`.

1. **Partition-leakage is structural.** The transitive closure of a connected graph reveals hidden-node information by count, edge-type, and path-length. No tool fixes this; best substrate-side answer is a rate-limited side channel. Whether that suffices for D-4 holdout discipline is a methodology-layer question BF-S defers and the red-team contests.
2. **Cross-language fidelity for ad-hoc FFI bindings.** No construction-path tool reliably resolves ad-hoc cross-language references outside schema-mediated paths.

Both are risk markers, not buildability blockers — the primitive *can* be constructed; what it *guarantees* is partial.

## Buildability verdict

**`designed-system`.** Glean + Stack Graphs (or CodeQL, or tree-sitter+Neo4j) realise the contract at known prior-art scale. Designed-system content: the Datalog rule set, cross-language symbol-URI scheme, role-visibility predicates in closure rules, rate-limiting side-channel defense. Two uncertainty flags carry forward to Phase 4.2 where the BF-S role-partition claim is re-examined.
