# P-26 — Codebase Model (6 views, integrated)

**Dispatch tier.** per-primitive, **research-grade-uncertainty** per [primitives/index.md](index.md) — "the most ambitious primitive in the catalog"; named by all three Round-2 adversarial reviewers for dedicated attention.
**Claimed by.** [BF-L](../tracks/brownfield-legacy-ingestion-first.md) (load-bearing — the entire track is three loops over this artifact).
**Composes.** [P-22](index.md), [P-23](index.md), [P-24](index.md), [P-07](cluster-C2.md).

## Contract restatement

P-26 is a **durable, versioned, queryable artifact** integrating six views (per [BF-L §1](../tracks/brownfield-legacy-ingestion-first.md)): (a) **structural** — modules, dependencies, call graphs, schemas; (b) **conventional** — idiom register, lint conventions, layering rules, test patterns; (c) **historical** — commit cadence, churn hotspots, fine-grained attribution; (d) **runtime** — production traces, error fingerprints, hot paths; (e) **invariant** — extracted from tests, types, assertions, schemas, docs; (f) **debt** — TODOs, deprecation markers, known-bad regions, dependency staleness, churn-vs-coverage clusters. *Built* by ingestion (Loop 1), *queried* per-cycle (Loop 2), *refreshed* by maintenance (Loop 3). Versioned so per-cycle queries pin to the snapshot at dispatch; queryable via a typed surface; durable in substrate storage (the F21 context-exhaustion defence). What makes it ONE model rather than six is the integration discipline below: common ID space, join API, snapshot consistency at version boundaries, unified `query(view, key, version) -> typed-result`. Without it BF-L collapses to BF-S and the load-bearing claim that *one artifact* parameterises methodology, regime classification, and scenario derivation is forfeit.

## Construction path per view

**Structural — composes P-22 + P-23.** **Tree-sitter** parsers + **SCIP** records ingest into **Meta Glean**'s typed-fact database; P-23's blast-radius is a Datalog query over Glean's `xref` predicate joined with module-membership facts. *Integration:* the substrate exposes `model.structural.symbol(qname, version)` and `impact(symbol, depth, version)` backed by Glean — the prior art most directly shaped to "polyglot queryable code-knowledge artifact at scale."

**Conventional — RG-uncertain (see flag).** **LLM-driven inference with structured output** (Pydantic-typed `Convention { name, pattern, scope, evidence-symbols, confidence }`) over a stratified sample (recency × churn), calibrated against a **golden corpus** of human-labelled conventions per language family; plus mechanical analyzers for naming (regex over Tree-sitter symbol tables), layering (import-graph), test patterns. *Integration:* ingestion dispatches sampled files to a cross-family judge ensemble (routed through P-14); responses are deduplicated, voted, and emitted as `Convention` facts into Glean keyed by scope. **Honest gap:** no SCIP-equivalent standard exists for convention extraction; SonarQube/ESLint/ArchUnit cover only a narrow slice.

**Historical — composes P-24.** **git log** / **git blame**; **Hercules** for churn analytics; **Sigstore (cosign)** for P-24's signed-append discipline. *Integration:* per-symbol attribution intersects Tree-sitter symbol ranges with `git blame -p` output per revision, persisting `{symbol, revision, author, timestamp, signed-by, commit-pointer}` to an append-only log (LMDB / SQLite WAL) cosigned for tamper-evidence — the trust precondition for the regime classifier's "high churn → operator mental model stale → degrade to L4" rule.

**Runtime — composes P-07.** **OpenTelemetry Collector** + Tempo/Prometheus/Loki backends + **OPA** for per-role read-filter policy. *Integration:* P-07 tags every span with the source symbol (line-number → Tree-sitter range → qname against the structural view at ingest), then P-26 exposes `model.runtime.hotpath / error-fingerprint / coverage` as OPA-mediated queries respecting the builder / V&V / comprehension role partition — the F28 holdout enforcement that makes the scenarios-derived-from-codebase claim defensible.

**Invariant — RG-uncertain (see flag).** **Daikon** for runtime invariant inference from execution traces; **CodeQL** for declared-invariant queries; **LLM-extracted invariants** from docs/comments via structured output; optional **Z3** / **CBMC** for symbolic validation. *Integration:* Daikon ingests P-07 trace dumps (joined with structural symbol ranges) and emits `{symbol, predicate-AST, support, refuted}`; CodeQL emits assertion/type/schema invariants; the LLM ensemble emits narrative invariants; all three streams write to a Glean `Invariant` predicate with `source` provenance. **Honest gap:** Daikon is mature academically but lacks production-grade integration with modern observability stacks and polyglot symbol indexes.

**Debt — composes industry tooling.** **CodeScene** (Adam Tornhill — canonical churn-vs-quality prior art) for hotspot analysis; **SonarQube** for static-analysis debt; **Dependabot** / **Renovate** for staleness; grep-based TODO/FIXME extraction. *Integration:* CodeScene's hotspot output (high churn ∩ low quality) emits `DebtCluster { region, severity, churn-vs-coverage-score, contributing-symbols }` facts; the union writes to a Glean `Debt` predicate queried by the regime classifier ([BF-L §2.1(d)](../tracks/brownfield-legacy-ingestion-first.md)) to route debt-touching cycles to elevated regime.

## Integration discipline — what makes it ONE model

**Common ID space.** All six views key on a substrate-canonical symbol ID derived from `{language, qname, source-revision}` plus stable hash. The structural view defines the space; every other view foreign-keys to it. A symbol that does not exist structurally cannot carry facts in other views — this mechanically enforces "one model" rather than "six co-located stores."

**Join API.** `model.join(symbol, version, [views]) -> { structural, conventional, historical, runtime, invariant, debt }` is the call shape the eligibility function and scenario-derivation primitive ([BF-L §1.5, §2.1](../tracks/brownfield-legacy-ingestion-first.md)) use — not the per-view APIs. Integration is the *call shape*, not only storage layout.

**Consistency.** **Snapshot consistency at version boundaries**: a `version` token (git commit + ingestion-pass ID) resolves a coherent view across all six; within a version, queries are repeatable. Within an ingestion pass, views are **eventually consistent** — structural lands first (defines the symbol space); the rest reach consistency before the version is sealed. Closer to a content-addressed snapshot store than OLTP.

**Versioning.** Each ingestion pass is immutable; the maintenance loop (P-13) produces incremental delta-versions sharing unchanged facts via Merkle-DAG structural sharing (IPFS-shaped). Per-cycle queries pin a version at dispatch — the cycle does not see mid-cycle changes (F34 defence at the model level).

## Construction effort

Registry says **6-12 engineer-months.** Realistic *only* if structural/historical/runtime/debt accept industry-standard tooling and conventional/invariant accept research-grade compromises (best-effort, confidence-scored). **Failure modes of partial completion:** (1) structural-only collapses to P-22+P-23 and forfeits the BF-L claim; (2) five-of-six without integration discipline is BF-S — cross-view joins for regime classification become impossible; (3) all-six without versioning breaks snapshot consistency and so breaks maintenance-loop drift detection (F34); (4) conventional/invariant shipped as commodity LLM dumps without golden-corpus calibration poisons every downstream eligibility decision — worse than not having the views (F1/F46 self-reference). Honest range: **9-18 engineer-months for a credible v1.**

## Research-grade-uncertainty flag

**Two views carry RG explicitly:** (a) **conventional** — no industry-standard tool extracts the full convention surface; LLM-structured-output is plausible but unwitnessed at the precision/recall the regime classifier needs; (b) **invariant** — Daikon-class inference is academically mature but has no production-grade integration with modern observability stacks or polyglot symbol indexes at scale. **Soft RG on integration scale:** six-view composition at 1M+LOC with 10+ years of history is unmeasured — Glean / SCIP have published scale numbers for structural alone.

## Per-candidate notes (no same-vs-distinct verdicts)

Only [BF-L](../tracks/brownfield-legacy-ingestion-first.md) claims P-26 directly. Others name sub-primitives the model would compose: **[BF-S](../tracks/brownfield-substrate-first.md)** names S-1=P-22, S-2=P-23, S-3=P-07, S-4=P-24 separately; **[BF-M](../tracks/brownfield-methodology-first.md)** uses code-traversal=P-22 + telemetry=P-07; **[U-C](../tracks/unified-C.md)** uses P-22+P-23 via P-32. **Per the [Round-2 constraints](../decisions/auto-001-phase-3.5-dispatch-shape.md#amendments-to-the-dispatch-brief-that-will-be-sent-to-subagents), this sketch does NOT opine on whether BF-L's integrated P-26 "should be" the same as BF-S's separate primitives** — Phase-4.2 work.

## Corpus-why citation

Load-bearing motivations from BF-L's brownfield-critical F-mode cluster ([BF-L §2](../tracks/brownfield-legacy-ingestion-first.md)): **[F20](../failure-modes-v3.md)** maintenance-vs-greenfield asymmetry — the model *is* the answer to "what do you actually know about the existing system"; **[F21](../failure-modes-v3.md)** context-window exhaustion — persisted versioned artifact defeats re-load; **[F34](../failure-modes-v3.md)** cross-layer drift — maintenance loop reconciles fast against slow; **[F54](../failure-modes-v3.md)** RSI goal subversion — invariant + debt views tag Caremark-exposed regions; **[F58](../failure-modes-v3.md)** runtime/design-time compliance split — runtime view + audited query log is the compliance evidence stream.

**Prior-art citations.** **Meta Glean** (open-source typed-fact code-knowledge store) — closest prior art for the multi-view integrated queryable artifact at scale; **Sourcegraph SCIP + zoekt** for structural-view backend; **CodeQL** for declared-invariant query infrastructure; **CodeScene** (Adam Tornhill) — canonical churn-vs-quality debt-cluster prior art; **Daikon** for runtime invariant inference; **OpenHands V1** event-sourcing ([report 11 §6](../../../research/11-openhands-substrate-audit.md)) for versioning. BF-L itself cites **[report 38 §3](../../../research/38-gas-systems-substrate.md) Beads' `discovered-from` edge** as "the corpus' strongest candidate compounding-of-knowledge primitive at the engine level" ([BF-L §3](../tracks/brownfield-legacy-ingestion-first.md)).

## Buildability verdict — decomposed per view

| View | Verdict | Rationale |
|---|---|---|
| Structural | `designed-system` | P-22+P-23 composition; Glean / SCIP prior art is direct. |
| Conventional | `research-grade-uncertainty` | LLM-with-structured-output + golden corpus plausible but unwitnessed at the precision/recall needed. |
| Historical | `designed-system` | P-24 composition; git plumbing + cosign signing is engineering on mature components. |
| Runtime | `designed-system` | P-07 composition; OpenTelemetry + OPA prior art is direct. |
| Invariant | `research-grade-uncertainty` | Daikon + CodeQL + LLM-extracted at integrated production scale is unwitnessed. |
| Debt | `designed-system` | CodeScene + SonarQube + Dependabot composition; well-trodden. |
| **Integration discipline** | `designed-system` with **soft RG on scale** | Six-view composition at 1M+LOC is unmeasured. |

**Overall: `research-grade-uncertainty`.** Gated by the weakest two views (conventional, invariant). Four views and the integration discipline are `designed-system`; scoping that ships the four solid views with "best-effort, low-confidence" conventional/invariant *could* degrade overall to `designed-system` — but BF-L's methodology (regime classifier, scenario derivation, eligibility function) then operates on degraded inputs on exactly the views it weighs heaviest, a worse failure mode than honest RG-uncertainty.

**Lead-agent recommendation flag for Phase-3.5.5.** BF-L's load-bearing primitive lands as `research-grade-uncertainty` honestly. This is admissible per the [refined two-part rule](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive), provided the flag is carried into Phase-4 candidate-comparison. The shrinkage question is whether BF-L survives *with* this RG flag on its central primitive, or whether the flag is fatal versus BF-S (which decomposes the same surface into separately-buildable primitives at the cost of the integration claim) and BF-M (which uses a thinner per-cycle code-traversal). That comparison is methodology-level — Phase 4, not here.
