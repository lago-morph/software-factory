# BF-L invariant-view prior-art research notes

**Charter.** Phase-4.4 research dispatch per [auto-003 option A](../decisions/auto-003-bfl-rg-view-choice.md). Catalog prior art and active work on production-grade runtime invariant inference at scale, feeding (i) BF-L Phase-4 invariant-view sub-track design, (ii) Phase-5 BF-L ADRs alternatives-considered, (iii) Phase-8 lean-eval pressure-test design. The target artifact is the integrated `Invariant` predicate of [P-26 Codebase Model](../primitives/P-26-codebase-model.md): `{ symbol, predicate-AST, support, refuted, source }`, fed jointly by trace-based dynamic inference, static checkers, type systems, property-based tests, observability streams, and LLM extraction.

---

## §1 Daikon and successors

**Daikon — canonical prior art.** Ernst, Cockrell, Griswold, Notkin, *"Dynamically discovering likely program invariants to support program evolution"* (ICSE 1999; extended TSE 2001). Daikon instruments a target program, captures variable values at program points (function entry/exit, loop heads, object scopes), and infers candidate invariants by template instantiation: it has a catalog of ~75 invariant templates over scalars, sequences, and pairs (e.g., `x > 0`, `x == y`, `x in [a..b]`, `x = a*y + b`, `len(arr) > 0`, `arr is sorted`, `x % k == c`). For each template, Daikon tracks how many observed traces satisfy it ("support") and discards it on first refutation. Surviving templates are filtered by a confidence test (informally: probability that the invariant holds by chance is below 1%) and by redundancy elimination (implication-closed pruning). Output is the well-known `.inv.gz` file and a human-readable invariants report.

**Languages / runtimes.** Front-ends ship for Java (`chicory`, bytecode rewriting), C/C++ (Kvasir, built on Valgrind), Perl, and via custom trace-dump format (`.dtrace`) any language can be plumbed in. Python and JavaScript front-ends exist as community ports of varying maturity. The trace-dump interface is the durable lingua franca.

**Precision/recall track record.** Empirical studies (Ernst 2000 dissertation; Nimmer & Ernst, *"Automatic generation of program specifications"* ISSTA 2002; Polikarpova et al., *"Comparative study of programmer-written and automatically inferred contracts"* ISSTA 2009) consistently report:
- High recall on simple numeric / sequence / nullness invariants when test coverage is good.
- Substantial false-positive rate: Daikon reports invariants that are coincidentally true on the trace set but are not actual program properties. Polikarpova 2009 found ~56% of Daikon-inferred postconditions matched human-written Eiffel contracts; the rest were either spurious-but-true-on-trace or too weak.
- Heavy dependence on trace diversity. Without exercising edge cases, Daikon "discovers" overfit invariants (e.g., `x < 100` because the test never went higher).

**Production-scale limitations.**
- Instrumentation overhead: Kvasir (Valgrind-based) typically 30-100x slowdown; Chicory 5-50x. Unfit for production traffic; works on test/staging traces or sampled offline replays.
- Trace storage: full variable dumps at every program point are enormous. Daikon's `--ppt-select-pattern` and sampling alleviate but do not solve.
- Template explosion: invariant candidates are O(n^2) over variables in scope; large functions (>50 locals) hit memory walls.
- No incremental / streaming mode: Daikon expects the full trace, then runs to fixpoint.
- No first-class symbol-index integration: outputs are keyed on `ClassName.methodName(args)` strings, not on a polyglot symbol-ID space.

**Direct successors and forks.**
- **DIDUCE** — Hangal & Lam, *"Tracking down software bugs using automatic anomaly detection"* (ICSE 2002). Online relaxation of invariants during execution; flags points where invariants weaken as anomaly candidates. Java only.
- **DySy** — Csallner, Tillmann, Smaragdakis, *"DySy: Dynamic symbolic execution for invariant inference"* (ICSE 2008). Combines concrete execution traces with symbolic path conditions to produce stronger, path-disjunctive invariants than Daikon's template engine.
- **Agitator** (Boshernitsan et al., *"From Daikon to Agitator: Lessons and challenges in building a commercial tool for developer testing"* ISSTA 2006). Agitar Software productized Daikon-style inference for Java unit testing. Notable as the only sustained commercial deployment; defunct after 2010.
- **DIG / NumInv** — ThanhVu Nguyen et al. (2014, 2017), polynomial/nonlinear invariant inference using algebraic-geometry techniques. Goes beyond Daikon's template library at the cost of solver dependence.
- **PIE / IceDust** — Padhi, Sharma, Millstein, *"Data-driven precondition inference with learned features"* (PLDI 2016). Replaces template instantiation with feature-learning over execution data; reports recall improvements on SyGuS benchmarks.
- **JDoctor** (Blasi et al., ISSTA 2018) — extracts invariants/preconditions from Javadoc comments via NLP, an early precursor of LLM-based extraction (see §6).

**Bottom line on Daikon.** Daikon and its successors solved the *inference* problem for narrow domains (numeric, sequence, nullness, simple equality) with honest precision/recall tradeoffs. They did not solve production-scale ingestion, polyglot symbol unification, or integration with modern observability. That gap is exactly the P-26 sketch's RG flag.

## §2 Symbolic execution and abstract interpretation

These tools *check* invariants (or fail to) rather than *infer* them in the Daikon sense, but they are critical complement: a refuted Daikon candidate can become a CodeQL query; a CodeQL-asserted invariant can be validated by symbolic execution.

- **KLEE** — Cadar, Dunbar, Engler, *"KLEE: Unassisted and automatic generation of high-coverage tests for complex systems programs"* (OSDI 2008). Symbolic execution on LLVM bitcode; finds inputs that violate `assert()` and pointer-safety conditions. Output is a counterexample trace, not a positive invariant. For P-26: a refuted candidate from Daikon could be fed to KLEE to produce a witness input that becomes part of the symbol's `refuted` set.
- **Z3** — de Moura & Bjørner, *"Z3: An efficient SMT solver"* (TACAS 2008). The underlying solver for nearly every modern static analyzer. P-26 would use Z3 to discharge implication checks between candidate invariants (e.g., does `x > 0` subsume `x >= 1` in this context?).
- **CBMC** — Clarke, Kroening, Lerda, *"A tool for checking ANSI-C programs"* (TACAS 2004) — bounded model checking. Given an assertion, CBMC searches for a counterexample within `k` loop unrollings. Complementary to Daikon: Daikon proposes, CBMC disposes.
- **Astrée** — Cousot et al., *"The ASTRÉE Analyzer"* (ESOP 2005). Abstract-interpretation-based sound checker for absence of runtime errors in C, deployed on Airbus avionics code. Produces *sound* invariants (over-approximations) — the dual of Daikon's *likely* invariants. P-26-relevant: Astrée's interval and octagon domains could feed range invariants with mathematical-soundness guarantees on supported C/Ada subsets. Commercial (AbsInt), not polyglot.
- **Infer** (Facebook/Meta) — Calcagno et al., *"Moving fast with software verification"* (NFM 2015). Separation-logic-based interprocedural analyzer for null-deref, resource-leak, race conditions. Open-source. Runs at Meta scale on every diff. **Critically: Infer outputs are already Glean-adjacent at Meta** — Meta uses Glean to store SCIP-like cross-references, and Infer's results are stored in databases queryable similarly. This is the closest existing precedent for a P-26-style polyglot-checker → unified-fact-store pipeline. Infer's *invariant* shape is narrow (memory safety, null-safety, thread safety), not Daikon-style data invariants.
- **CodeQL / Semmle** — de Moor et al., *"Keynote address: .QL for source code analysis"* (SCAM 2007). Datalog-style query language over a typed code-fact database. CodeQL ships ~3000+ queries spanning security and correctness; the P-26 sketch names CodeQL specifically as the source for declared-invariant queries (assertions, `requires`/`ensures` annotations, schema annotations parsed from JSON-Schema/protobuf/OpenAPI files). CodeQL's fact-store is conceptually similar to Glean but uses its own database engine (TRAP files → relational). GitHub operates CodeQL at scale across millions of public repos via Code Scanning. **This is the strongest existing precedent for production-scale polyglot invariant *query* infrastructure** — though it does not do dynamic inference.

**Composition with Daikon.** Daikon proposes invariants from traces; CodeQL provides the queryable static-fact substrate that can store declared invariants and refute Daikon candidates via cross-referenced assertions; KLEE/CBMC produce witness inputs for refutations; Z3 normalizes the predicate-AST and discharges redundancy. The P-26 sketch's "all three streams write to a Glean `Invariant` predicate with `source` provenance" composition is technically coherent but has, to my knowledge, no production-scale prior demonstration.

## §3 Type-inference-system invariant extraction

Modern type systems already carry many of the predicates P-26 wants as invariants. Lifting them is a low-cost first quartile of the invariant view.

- **TypeScript strict mode** (`strict: true`, `strictNullChecks`, `noUncheckedIndexedAccess`). Nullness and discriminated-union exhaustiveness become statically checked invariants. SCIP records carry the inferred types; lifting them to predicates of the form `forall x:T, x !== null` is a syntactic transformation.
- **mypy / pyright** for Python — gradual typing with PEP 484/586/593 annotations. `Literal["a","b"]` and `Annotated[int, Ge(0)]` (PEP 593) carry value-range invariants. Pyright (Microsoft) is the production engine for VS Code's Pylance.
- **Checker Framework** for Java — Papi, Ali, Correa, Perkins, Ernst, *"Practical pluggable types for Java"* (ISSTA 2008). Same Ernst lineage as Daikon. Ships @NonNull, @Tainted, @Interned, @Regex, @Format, @Units, @KeyFor and dozens more pluggable type qualifiers. Each qualifier corresponds to a class of invariants; output is queryable through standard javac plumbing.
- **Rust borrow checker** — produces alias-freedom and lifetime invariants that compose into stronger memory-safety guarantees than any of the above. Output is implicit in the type signature; explicit lifting requires parsing rustc's HIR.
- **F\# / Liquid Haskell / refinement types** — Vazou et al., *"Refinement Types for Haskell"* (ICFP 2014). Explicit value-range invariants in the type system, e.g., `{v:Int | v > 0}`. Production deployment is academic/niche; relevance to BF-L is mostly as a precedent for the predicate-AST shape.
- **Dependent-type systems** (Coq, Lean, Idris, Agda). Out of scope for industrial BF-L but inform the predicate-AST upper bound.

**Lift to P-26.** The tractable plan: per language, write a small extractor that walks SCIP/Tree-sitter symbol records and emits an `Invariant` fact for every type-system-derivable predicate (nullness, range from refinement annotations, enum-membership from union types, format strings from `@Format`). Precision is essentially 1.0 (modulo type-system unsoundness gaps like Java's `null`/erasure, TypeScript's `any`-escape hatches). Recall is bounded by what's in the type system. **This is the single most-tractable invariant class to ship first** — see §8.

## §4 Property-based testing inference

PBT tools surface invariants by attempting to refute them; refutations + shrunken counterexamples are the most valuable signal.

- **QuickCheck** — Claessen & Hughes, *"QuickCheck: A lightweight tool for random testing of Haskell programs"* (ICFP 2000). Predicates are stated, generators sample inputs, shrinking minimizes counterexamples. Family includes Hypothesis (Python), fast-check (TypeScript), ScalaCheck, jqwik (Java), proptest (Rust).
- **Hypothesis** — Drysdale et al. — adds *targeted property search* (Löscher & Sagonas, *"Targeted property-based testing"* ISSTA 2017): hill-climb on a fitness function (e.g., trace coverage, maximizing input size). Hypothesis records all failing cases in the `.hypothesis/examples` database — a natural durable source of refuted invariants for P-26's `refuted` set.
- **Fuzzers + sanitizers** — libFuzzer, AFL++, Google's ClusterFuzz. UndefinedBehaviorSanitizer / AddressSanitizer / ThreadSanitizer / MemorySanitizer report violations of memory-safety and undefined-behavior invariants with witness inputs. **Google's OSS-Fuzz** has run continuous fuzzing on ~1000 open-source projects since 2016 — a substantial corpus of invariant-violations-with-symbol-attribution; reports are filed against function-level symbols.

**Composition with P-26.** Every fuzzing campaign / PBT run is implicitly testing thousands of invariants (memory-safety, type-safety, assertion-validity). Aggregating refutations into the `refuted` field with the witness input as evidence is straightforward plumbing. The harder problem — turning PBT *successes* into positive invariants — is unsolved: success only confirms the stated property, not derived ones. (You learn `forall x, P(x)` but not the conjuncts of `P`.)

## §5 Observability-driven invariant detection

The runtime view of P-26 (P-07 traces) is the natural input for invariant inference at production scale.

- **Anomaly detection on metrics.** SLI/SLO frameworks (Google SRE Book ch. 4; OpenSLO standard) treat error-budget violations as refutations of latency/availability invariants. Honeycomb's BubbleUp (Charity Majors et al.) clusters anomalous events by attribute-conditional invariants ("requests with `user_tier=enterprise` AND `region=eu-west` have p99 latency 10x higher than baseline" is an invariant violation).
- **Distributed-trace mining.** Tools like Jaeger, Tempo, OpenTelemetry Collector emit spans tagged with attributes. Academic work — e.g., Zhang et al., *"Sentinel: A robust intrusion detection system for IoT networks using kernel-level system information"* (2020) — and industry tools (Datadog Watchdog, New Relic Applied Intelligence) infer "normal" patterns and flag deviations. These are *implicit* invariants (statistical baselines), not predicate-AST-shaped.
- **Pythia** — Sigelman et al. (Google), *"Dapper, a large-scale distributed systems tracing infrastructure"* (Google TR 2010) — the OG distributed tracing system; downstream Pythia work (Mace et al., SOSP 2018) infers "trace lattice" structural invariants.
- **OpenTelemetry-derived invariant proposals.** No standardized OTel signal for "invariant" currently. OpenTelemetry Logs / Metrics / Traces remain the raw substrate; mapping span attributes to symbol-keyed invariants is custom integration work. The CNCF observability TAG has discussed an `otel-invariants` extension but no spec as of 2025.

**Daikon-on-OTel.** I found no published production-scale integration of Daikon (or successor) with an OpenTelemetry / Tempo trace store. The closest is Hangal & Lam's DIDUCE applied to single-process Java traces. Bridging OTel span attributes → Daikon `.dtrace` format is plumbing (~hundreds of LOC), but bridging *meaningfully* — ensuring that the span tags carry enough variable values to make invariant inference informative — requires source-code instrumentation discipline that most production codebases lack. **This is exactly the unwitnessed-at-scale gap P-26 names.**

## §6 LLM-extracted invariants from docs/comments

Recent (2023-2025) work using LLMs to extract structured invariants from natural-language sources.

- **JDoctor** (Blasi et al., ISSTA 2018) — precursor; rule-based NLP on Javadoc to extract `@param`/`@return`/`@throws` constraints. Reported ~80% precision on hand-curated Javadoc but recall <40%.
- **DocTer** — Xie, Chen, Jung, Choi, *"DocTer: Documentation-guided fuzzing for testing deep learning API functions"* (ISSTA 2022). Extracts input-constraint invariants from PyTorch/TensorFlow API docs via dependency-parse + heuristics; constraints feed a fuzzer.
- **SpecBuddy / LLM-assisted spec inference** — multiple 2023-2024 arXiv preprints (Endres et al., *"Can large language models write good property-based tests?"* arXiv:2307.04346, 2023; Lemieux et al., *"CODAMOSA: Escaping coverage plateaus in test generation"* ICSE 2023 — LLM-augmented test generation that proposes invariants implicitly). [uncertain] — I cannot verify all author lists / venue placements from training.
- **Pynguin + LLM** — Lukasczyk et al. — automated test generation for Python; recent extensions use LLMs to propose oracle conditions. [uncertain] on specific 2024-2025 publications.
- **InvGen / Lemur** — Wu, Wu, Wang, Bastani, *"Lemur: Integrating large language models in automated program verification"* (ICLR 2024) — LLMs propose loop invariants for SV-COMP-style benchmarks; SMT solver discharges them. Reports state-of-the-art on Linux-kernel-driver verification benchmarks. **This is the strongest recent precedent for LLM-proposed invariants with mechanical verification** — the design pattern P-26 should adopt.
- **Pei et al., *"Can large language models reason about program invariants?"* (ICML 2023)** — direct empirical study. Reports GPT-4 achieves ~57% precision on inferring loop invariants from short C functions, with precision dropping sharply on longer functions. Recall not separately reported. [uncertain on exact venue; consult original.]

**Empirical track record summary.** LLM invariant extraction in 2024-2025 ranges from ~50% precision (raw GPT-4 output on loop-invariant tasks) to ~90% precision (LLM-proposed + SMT-verified, accepting only the verified subset). The **propose-and-verify** pattern (Lemur, Endres) is the credible production shape; **raw LLM extraction without mechanical verification is below the precision bar** the P-26 regime classifier needs. The Convention-view sister sub-track's golden-corpus calibration approach is the equivalent compensation.

## §7 Polyglot integration attempts

Has anyone built a production-grade invariant store integrated with a polyglot codebase index?

**Glean (Meta).** Glean ships predicate schemas including `cxx.Function`, `python.Definition`, `hack.MethodDefinition`, etc. — purely *structural*. To my knowledge **Meta has not published a Daikon-integrated `Invariant` predicate in Glean's public schema repository.** Internal Meta uses (PyRe, Hack typechecker, Infer) feed Glean-adjacent stores but as separate views, not as a unified `Invariant` predicate. The P-26 sketch's unification at the *Glean predicate level* would be net-new.

**Sourcegraph / SCIP.** SCIP is a structural code-index format; it does not carry invariant data. Sourcegraph's "Code Insights" feature surfaces aggregated metrics (e.g., "how many TODOs over time") but not predicate-AST invariants. No production polyglot-invariant integration.

**GitHub CodeQL.** As noted in §2, CodeQL's TRAP database carries declared-invariant facts and supports cross-language queries (somewhat — practical cross-language queries are rare). It is the closest existing system to "polyglot invariant store" but: (a) it's static-only (no Daikon-style dynamic inference); (b) the schema is per-language and federation is by query, not by shared predicate; (c) it's GitHub-proprietary infrastructure.

**Has anyone integrated Daikon with OpenTelemetry / Tempo / Prometheus?** I find no published production deployment of this integration. Academic prototypes exist (DIDUCE on single-process JVM traces; Pythia-style trace lattices) but no Daikon-on-OTel-Collector pipeline. **This confirms the P-26 sketch's RG-uncertain flag honestly.**

**Honest assessment of polyglot integration prior art:** The component pieces (Glean for storage, SCIP for symbol-IDs, Daikon for inference, OTel for trace ingestion, CodeQL for static facts, Lemur-shape for LLM proposals) all exist and are individually production-grade. **The composition is unwitnessed.** This is engineering risk, not research risk — but P-26's claim is that the composition *defines* the artifact, so the engineering risk is the load-bearing one for BF-L.

## §8 Honest assessment for the BF-L sub-track

**Realistic precision/recall ceiling for the integrated invariant view, as P-26 sketches it.**

Decomposed by source stream:

| Source | Precision ceiling | Recall ceiling | Notes |
|---|---|---|---|
| **Type-system lift** (TS strict, mypy strict, Checker Framework, Rust) | ~0.99 | Bounded by type-system expressiveness | Lowest-hanging fruit; ship first |
| **Static declared-invariants** (CodeQL queries for assert/contracts/schemas) | ~0.95 | High where contracts exist; low where they don't | The CodeQL precedent is direct |
| **Daikon-class trace inference** (filtered + cross-checked) | ~0.5-0.7 raw; ~0.85 after SMT cross-check | Limited by trace diversity | Polikarpova 2009 baseline |
| **PBT/fuzz refutations** (negative invariants only) | ~1.0 (witness-backed) | High where PBT exists | Adds to `refuted` set, not `support` |
| **OTel-derived statistical invariants** | ~0.3-0.5 (false positive heavy) | Broad but noisy | Daikon-on-OTel is unwitnessed |
| **LLM-extracted (propose + SMT-verify)** | ~0.85-0.9 (verified subset only) | Low (only narrow predicates verifiable) | Lemur-shape; raw LLM is below the bar |

The integrated `Invariant` predicate's *aggregate* precision depends on the source-weighting and dedup discipline. If P-26 weights sources by their per-source precision and emits a confidence score per fact, an aggregate precision of **~0.80-0.85** on the union seems achievable. Aggregate recall is harder to bound because the universe of "true invariants" is undefined.

**Most-tractable invariant class to target first.**

In rank order of tractability for the BF-L sub-track's "≥5 declared machine-checkable invariants per language for top-3 languages" Phase-4-close gate:

1. **Null-safety invariants** on Java (`@NonNull`/`@Nullable` via Checker Framework), TypeScript (`strictNullChecks`), Python (`Optional[T]` via mypy strict). Precision ~1.0, recall bounded by annotation coverage. Shippable as a syntactic lift from existing type-checker output.
2. **Type-tag / enum-exhaustiveness invariants** ("this field is one of {A,B,C}"). Direct from TS discriminated unions, Python `Literal[...]`, Java enum types.
3. **Range invariants on numeric fields** (from `Annotated[int, Ge(0)]` in Python, `@Min/@Max` in Java Bean Validation, refinement types where available). Precision ~1.0 on annotated fields; the harder Daikon-class inference of *un-annotated* range invariants is best deferred.
4. **Schema-conformance invariants on API boundaries.** OpenAPI / JSON-Schema / protobuf declarations carry per-field invariants for free; the lift is parsing schema files and emitting `Invariant` facts per `(endpoint, field, predicate)`. Strong recall on schema-documented systems; zero recall on under-documented systems (which is most legacy code — but that's where the conventional view helps).
5. **Assertion-derived invariants** (`assert x > 0` in Python; `Preconditions.checkArgument(...)` in Java; `assert!()` in Rust). Direct from AST traversal; precision ~1.0.

Items 1-5 cover the Phase-4-close gate without invoking Daikon dynamic inference at all. **Daikon-class inference is the right Phase-5 or Phase-6 stretch goal, not the Phase-4 gate criterion.**

**Biggest open problem the BF-L sub-track will have to solve-or-accept-as-RG.**

The unwitnessed-at-scale gap is **the trace-ingestion pipeline that bridges production OpenTelemetry signals to Daikon-style dynamic invariant inference, keyed on the same polyglot symbol-ID space the structural view defines.**

Specifically:
- OTel spans carry attributes, not full variable snapshots; Daikon needs the snapshots.
- Production instrumentation cost (5-50x slowdown for Chicory-class instrumentation) rules out full-fidelity prod tracing; sampling discipline is required and unsolved at the inference-quality level (sampled-out invariants get refuted as if they're false).
- Symbol-ID unification across the Java/Python/TS/Rust polyglot is a separate engineering problem — each language's trace tagger needs to emit the canonical substrate symbol-ID. SCIP gives the structural-view ID; OTel tagging convention to emit it is custom.
- The Glean `Invariant` predicate schema P-26 sketches has not been written; the unification of `support`/`refuted` semantics across the six source streams is a schema-design problem with no public precedent.

**This problem is, in honest terms, the BF-L invariant-view sub-track's central engineering risk.** The sub-track must either solve it (build the OTel-to-Daikon-to-Glean pipeline on a representative codebase) or accept it as RG (ship only the static and type-lifted sources for Phase-4, defer dynamic inference). The bounded "≥5 invariants per language across top-3 languages = 15 minimum" gate is achievable from items 1-5 above *without* solving the dynamic-inference plumbing — so the gate-passing path is viable; the gate-failing risk is on the dynamic-inference reach.

## Specific recommendations for the sub-track design

1. **Tier the invariant sources by tractability.** Ship Tier-1 (type-lift) for the Phase-4-close gate; Tier-2 (static + assertion + schema) as the "designed-system promotion" bar; Tier-3 (Daikon-class dynamic) as an explicit Phase-5+ stretch goal carried with an RG-flag.

2. **Adopt the Lemur propose-and-verify pattern for LLM-extracted invariants.** Raw LLM extraction is below the precision bar; LLM-proposed + Z3-verified is at the bar. The structural view's symbol-ID space and an SMT discharger are the missing infrastructure pieces.

3. **Treat the Glean `Invariant` predicate schema as the central design artifact.** It must encode `{symbol, predicate-AST, support, refuted, source, confidence, source-version}`. The predicate-AST language needs union types for {range, equality, nullness, enum-membership, regex-match, schema-conformance, custom-Z3-encoded}. This is a 1-2 week schema-design exercise; the sub-track should sequence it before construction.

4. **Use Infer as the existence-proof for production-scale polyglot static invariant infrastructure.** Meta's Infer + Glean integration is the closest existing analog. Reading Infer's published architecture (Calcagno NFM 2015 + follow-up Meta engineering blog posts) is the highest-leverage prior-art consumption for the sub-track.

5. **Defer the OTel-Daikon bridge.** Acknowledge it as the central engineering risk; ship the Phase-4 gate without it; carry it as named work for Phase-5/6 with an explicit RG-flag if not yet built.

6. **Pressure-test in Phase-8 lean-eval against three failure modes specifically:** (a) the `support` count grows linearly with trace volume but precision collapses on edge-case inputs (Daikon overfitting); (b) the LLM-extracted source poisons the predicate set with plausible-but-wrong invariants that aren't refuted by available traces; (c) the symbol-ID unification breaks across an in-place language migration (e.g., Python 2 → 3, Java module renames) and historical invariants become unreachable.

7. **Carry the RG-flag honestly into Phase 5.** Per [auto-003](../decisions/auto-003-bfl-rg-view-choice.md), if the sub-track fails its gate the view falls back to (b) accept-as-RG. The Phase-5 ADR should pre-author the graceful-degradation paragraph: BF-L's regime classifier downweights any `Invariant` fact whose source is `daikon-dynamic` or `llm-extracted` when the source's per-fact confidence is below a threshold; the eligibility function uses only Tier-1 and Tier-2 invariants for binding decisions.

---

**References (cross-repo).** [P-26 Codebase Model](../primitives/P-26-codebase-model.md) §Construction-invariant; [auto-003 BF-L RG-view choice](../decisions/auto-003-bfl-rg-view-choice.md); [auto-002 U-B path](../decisions/auto-002-ub-path.md) for parallel-precedent symmetric treatment; [failure-modes-v3](../failure-modes-v3.md) F20/F21/F34/F54/F58 (the failure modes the invariant view defends against).
