# Optimized Deltas — Force-Pattern Skeptic Review (Track B)

Adversarial review of every `DELTA-NN` in `spec-optimized/C*.md` against Track B's binding rule:
deltas must be justified by **concrete forces** (scale / failure / cost / security / operability /
simplicity / parallelizability), not taste. Each delta is scored against the v4 corpus (README,
AI-CONTEXT, F-MODE-COVERAGE, the gap register), with the relevant evidence cited inline.

23 spec-optimized files, **144 deltas** scored.

---

## Section 1 — Verdict table

Verdicts: **WJ** = well-justified, **WK** = weakly-justified, **TA** = taste,
**OE** = over-engineered, **UN** = unclear. Rewind cost = cost of removing this delta
if it turns out wrong: **S** small (delete a field), **M** medium (re-spec one seam), **L** large
(touches multiple sibling specs / interface freeze).

### C01 — Gas City runtime substrate

| Delta | Force claimed | Verdict | Rewind | Reasoning (≤2 sentences) | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 portability contract | simplicity / lock-in | **WK** | L | Force is real (README §552 "if Gas City fails the whole plan reorganizes") but C01's own OQ1 concedes the interface may be too thick to be a real portability layer; if so this is documentation-of-lock-in dressed as architecture. | README §552, AI-CONTEXT §3.6 (~20 Go files for runtime alone); C01 OQ1 explicitly flags the risk. |
| 02 version pin + conformance suite | operability | **WJ** | S | Pinning a version + running a conformance gate before trusting "Native" cells is cheap, deletable, and directly addresses G11 (no author has run `gc`). | README §552, AI-CONTEXT §3.5 "1-2 breaking changes/quarter", G11 blocker. |
| 03 native-count corrected to 5 | simplicity (honesty) | **WJ** | S | G03 is a documented blocker; this is just stating the truth. No engineering surface. | G03 (major); AI-CONTEXT §3.1 P3 "Strong when `[formulas]` enabled"; README Phase 0 turns formulas off. |
| 04 ABI seam owned by C02 | simplicity / parallelizability | **WJ** | S | Pure ownership-clarification of an admitted-undocumented seam (G29); enables C02 parallel build. | G29; AI-CONTEXT §3.4. |
| 05 bounded reconciliation invariant | failure (F52) | **WJ** | M | F52 is a named failure mode the docs warn about; lifting the bound to the substrate is proportional (one invariant + escalation hook). | F-MODE-COVERAGE §8 F52, G18. |
| 06 degraded mode + supervised restart | failure (G33) | **WJ** | M | G33 is a major gap; "Orders survive crashes but not the runner" is a real and concrete fix. | README §389 (multi-OSS stack), G33; F-MODE-COVERAGE no row for OSS-stack cascading. |

### C02 — Pack & tool-node ABI

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 wire protocol spec | simplicity (define seam) | **WJ** | L | G29 is explicit ("actual seam is undocumented"); without this the "no fork" claim is hollow. | G29 (minor — but load-bearing for the no-fork thesis); AI-CONTEXT §11.3. |
| 02 signed pack manifest | security (RSI) | **WK** | M | Force is real (F54 RSI / G35) but the "human-held trust root" depends on C03's unsolved SecretResolver (OQ1) + C41 sign infra (XC-6). Provenance-without-keys is theater. | G35, G37 (no secrets store), XC-6. |
| 03 typed I/O envelope | correctness | **WJ** | S | Replacing `{placeholder}` argv with typed JSON envelope is proportional and standard. | AI-CONTEXT §13.3 shows the loose status quo. |
| 04 capability declaration → C43 | security (G31) | **WK** | M | XC-8 explicitly admits this is detection-only until C43 ships (unbuilt through Phase 3b per G31). Real benefit deferred. | XC-8 in review-log; G31 blocker. |
| 05 ABI version handshake | operability | **WJ** | S | Concrete force ("1-2 breaking changes/quarter", §3.5); cheap. | AI-CONTEXT §3.5; documented migration tail. |
| 06 language-neutral protocol | simplicity / fidelity | **WJ** | S | Force is concrete: v4 already names Go AND Python tool nodes (C36/C37/C44). Not theoretical. | AI-CONTEXT §6 Python tool nodes; README OSS table. |
| 07 explicit fork-trigger criteria | operability (falsifiability) | **WK** | S | Useful, but "make slogans falsifiable" is meta-engineering. Modest value. | README §509-518; G29. |

### C03 — Layered config / feature-flag model

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 explicit precedence layering | correctness | **WJ** | S | v4 shows examples but never states the merge order — that's a real ambiguity any implementer must resolve. | AI-CONTEXT §13 shows `pack.toml`/`city.toml`/env without precedence. |
| 02 CapabilityDescriptor registry | failure (F13) | **WK** | M | F13 ("missing-config blindspot") is real but XC-7 flags this descriptor as a double-source-of-truth vs. the component inventory; the mechanism may duplicate the inventory's `requires` graph. | F-MODE-COVERAGE F13; XC-7. |
| 03 SecretRef indirection | security (G37) | **WJ** | M | G37 is explicit and unsolved; secret reference + lint for literals is the minimum responsible move. | G37 (major); AI-CONTEXT §13.2 `env = {...}` literals. |
| 04 config validation/lint gate | failure (F13) | **WJ** | S | Standard load-time validation; cheap; closes F13 silent-disable failure. | F-MODE-COVERAGE F13. |
| 05 Phase-0 native-count corrected | simplicity (honesty) | **WJ** | S | Same G03 honesty move as C01 DELTA-03. | G03 blocker. |
| 06 config provenance to C23/C41 | operability / observability | **WJ** | S | One event per (re)load is cheap and gives "what is actually turned on right now" — concrete operational answer. | C23 + C41 already exist; trivial integration. |

### C04 — Session & provider runtime

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 SessionProvider contract | simplicity / lock-in | **WK** | L | Same C01 DELTA-01 pattern — Gas City's `runtime.Provider` is ~18 methods (§3.6), so "stable interface" risks being a re-implementation. Useful conceptually, but force = simplicity is contested. | AI-CONTEXT §3.6 "~18 methods, conformance suite travels with it." |
| 02 ResumeToken with fidelity contract | failure (F16) | **WJ** | M | F16 "KV-cache loss inherent (Partial)" is real; making the loss declared/observable instead of silent is exactly proportional. | F-MODE-COVERAGE F16; README P10 "Cross-session continuity native." |
| 03 CredentialSource fallback ladder | failure (G12) | **WJ** | M | G12 explicitly says "API-key fallback path ready" is named-but-undesigned; this designs it. | AI-CONTEXT §14 risk register; G12 major. |
| 04 session-liveness emission | failure (F22) | **WJ** | S | F22 needs "anomaly detection on session liveness" with no defined producer; this defines the producer. | F-MODE-COVERAGE F22. |
| 05 isolation-at-spawn | security (G31/G21/G28) | **WJ** | M | Concrete force: closes G21/G28 holdout-leak window and bounds G31 pre-twins exposure at the OS, not by prompt discipline. The single most defensible delta in the security cluster. | G21, G28, G31; README l.177 "discipline ≠ enforcement." |
| 06 multi-session lifecycle | scale (G34) | **WJ** | M | "corpus only ever spec's one session" is literally true; concurrent operation needs a pool/ceiling/drain. Force = G34. | README P0 §355 "running one Claude Code session"; G34. |

### C05 — Sling / dispatch

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 typed RoutingDecision + key | operability (auditability) | **WJ** | S | "Why did this work item land on this agent" being a queryable fact instead of folklore is cheap and directly enables C46 meta-metrics. | AI-CONTEXT §3.2 concept 8 ("opaque verb"); C46 explicit. |
| 02 admission-controlled dispatch | scale (G34) | **WJ** | M | G34 is a named blocker (single-Max-seat ceiling); routing-time admission is proportional. | G34; G13; AI-CONTEXT §4.1. |
| 03 pool routing with starvation guard | scale + fairness | **WJ** | S | Standard pool strategy; concrete fan-out problem once `[rigs]` lights up in Phase 1. | AI-CONTEXT §3.4 pool gated by `[rigs]`. |
| 04 routing vs binding authority split | simplicity / parallelizability | **WJ** | S | Closes a real double-ownership ambiguity (README l.109 ambiguous); enables C05/C09 parallel build. | C05/C09 inventory `Depends on` graph is muddled. |
| 05 convoy = batched-dispatch primitive | correctness | **WK** | S | Force is "vocab word → primitive"; useful but at risk of speculative because convoy use cases aren't yet concrete. | AI-CONTEXT §3.3 "convoy" defined but no consumer named in v4. |
| 06 idempotent dispatch record | failure / correctness | **WJ** | S | A redelivered dispatch double-placing a wisp is a real failure class; `{wisp_id, attempt_no}` key is minimal. | G18 (loop bound); F52. |

### C07 — Vocabulary & glossary

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 machine-readable registry | simplicity / parallelizability | **WJ** | S | Standard glossary-as-data; cheap; enables linter coupling C10/C15. | G06 major. |
| 02 authority over overloaded terms | simplicity (correctness) | **WJ** | S | Resolves G01 (layer) / G02 (phase) — both named contradictions. Concrete and load-bearing. | G01, G02 major. |
| 03 provenance/origin field | minor / hygiene | **TA** | S | "Every term carries provenance" is metadata-for-metadata's-sake; no failure mode cited; vocabulary terms don't need a hash chain. | No v4 failure mode cites term provenance. |
| 04 vocab-lint hook to C10/C15 | failure (F38) | **WJ** | S | F38 marked "Addressed" via lint but lint has no canonical term set — this delta is what *makes* the F38 mark honest. | F38; F-MODE-COVERAGE §"Addressed" note. |
| 05 deprecation/alias lifecycle | operability | **WJ** | S | Concrete: Gas City migration tail is documented (§3.5); absorbing 1-2 renames/quarter without breaking 25 downstream refs is real. | AI-CONTEXT §3.5. |
| 06 lock_in_cost + extraction_safe_synonym | hygiene / future-proofing | **WK** | S | Self-described in the spec as conditional on consumers (C01-B DELTA-01 + C57); if those don't materialize, "dead metadata" per the spec itself. | C07 §6 caveat. |

### C08 — Spec artifact & format

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 standalone spec, not prompt | fidelity-to-evidence + simplicity | **WJ** | L | Strong concrete force: every real dark-factory in the v4 corpus (StrongDM, Kilroy, Fabro) separates spec from prompt template. The collapse was a v4 inference, not a corpus fact. | `one-shot-specs-and-research.md` §"Notes excluded." |
| 02 multi-file bundle | fidelity-to-evidence | **WJ** | M | Same evidence: Kilroy ships `spec.md` + `DoD.md` + `*.dot` as separate files. | one-shot-specs-and-research.md corpus. |
| 03 enumerated DoD | failure (F18) | **WJ** | M | F18 "prose specs lack rigor" → DoD-criteria-as-scoreable is the load-bearing anchor for C32/C33 satisfaction. | F18 Partial; README P6 "satisfaction not test-pass." |
| 04 BLAKE3 content-addressed spec id | correctness | **WJ** | S | Pinning a run to an exact spec revision is real (multi-revision runs already exist). Cheap (BLAKE3 reused from C21). | README P1; C21 BLAKE3 already foundational. |
| 05 required-section schema | failure (F3) | **WK** | M | F3 is real but the "4 required sections" feels arbitrary — Part 2 research is cited but the choice of *these* 4 vs others is asserted. Useful but not airtight on proportionality. | Part 2 ArchCode/PRDBench cites generic relevance, not specific schema. |
| 06 graded detail_level + clarification hook | failure (F25/G15) | **WK** | M | F25/G15 "design starvation" is real but solving it via a `detail_level` field is more of a process hint than a mechanism; the interactive-clarification-hook is hand-waved. | G15 "honest staffing / document it" — already conceded design issue. |

### C09 — Prompt template & spec→execution binding

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 adopt C08-B DELTA-01 | parallelizability | **WJ** | M | Direct corollary of C08 DELTA-01; if C08 splits, C09 must consume by ref. | C08 DELTA-01 evidence. |
| 02 typed render context | failure (silent empty prompt) | **WJ** | S | "Missing variable = silent empty prompt" is a real Go template failure mode; strict mode is standard. | Go text/template default behaviour. |
| 03 content-addressed binding_id | observability / auditability | **WJ** | S | "Which exact spec+template revision drove which work" is concrete; hash is cheap. | P9 attribution; C46 meta-metrics. |
| 04 sandboxed render | security (lethal-trifecta) | **WJ** | S | Go template `text/template` defaults are NOT sandboxed; `funcMap` could include filesystem/exec funcs. Concrete attack surface. | G31 lethal trifecta. |
| 05 strict-missing-key + prompt.id | observability | **WJ** | S | `prompt.id` already a Claude Code correlation key (§4.3); guaranteeing it is emitted is correct alignment. | AI-CONTEXT §4.3. |
| 06 spec-embed strategy {link/inline/summarized} | failure (F36) | **WK** | S | F36 instruction-following-ceiling is real but choosing `link` vs `inline` is a config knob with no empirical basis cited. | F36 referenced; no measurement. |

### C10 — Spec linter (EARS/INCOSE)

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 pure C17 tool node | simplicity / cacheability | **WJ** | S | Cacheable + composable in formula + CI gate — concrete operability gain, no overhead. | C17 determinism class taxonomy already exists. |
| 02 lint on C08's structured sections | failure (F18, F38) | **WJ** | S | Direct upgrade — form-only → form+vocab+completeness — proportional to forces it cites. | F18 Partial; F38 "Addressed (by what?)." |
| 03 graded blocking by detail_level | failure (F25 design starvation) | **WJ** | S | Concrete pairing with C08 DELTA-06; prevents linter from blocking thin early specs. | F25 / G15 design-starvation problem. |
| 04 vocab-lint to C07 CanonicalTermSet | failure (F38) | **WJ** | S | This is the actual mechanism that makes F38 "Addressed" honest. | F38; C07 DELTA-04. |
| 05 INCOSE rule registry | extensibility | **WK** | S | "Auditable, transfusion-traceable" is fine but "explicit, versioned, configurable rule registry" for R7-R35 is a lot of machinery for one rule family; could be a config file. | No v4 evidence the rule set needs to evolve fast. |
| 06 quality score 0-1 + threshold gate | failure / cost | **WK** | M | Trendable meta-metric is nice for C46 but the "guard against a single noisy rule" is a real worry; risk of Goodhart on a single number. | C46 meta-metrics planned; risk of new F47 vector. |

### C12 — Formula / pipeline-file format

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 versioned formula schema | correctness | **WJ** | M | "Folklore TOML" is a real ambiguity; a real schema is the minimum. | AI-CONTEXT §3.4 doesn't pin a schema. |
| 02 explicit node taxonomy | simplicity / correctness | **WJ** | S | `agent`/`tool`/`gate`/`sub_formula` matches v4's actual usage; closing under those is honest. | AI-CONTEXT §3.2 concept 7. |
| 03 parameter + binding contract | parallelizability | **WJ** | M | Spec→formula→template needs an explicit binding — concrete force tied to C08/C09. | C08 DELTA-01, C09 DELTA-01. |
| 04 methodology-as-data identity | operability | **WJ** | S | C55's whole point is swappable methodologies; named/versioned formula identity is the substrate. | C55 spec. |
| 05 DAG well-formedness invariants | correctness | **WJ** | S | Pure ownership-clarification; tells C15/C16 what they're checking. | C15/C16 inventory rows. |
| 06 formula provenance + transfusion lineage | hygiene / P9-alignment | **WK** | S | `transfused_from` is real (C51) but "formula provenance" duplicates C41/C51 fields; risk of three sources of truth. | C51 transfusion discipline; C41 attribution. |
| 07 DOT round-trip canonical-form requirement | correctness (G24) | **WJ** | M | G24 "round-trip fidelity unaddressed" is explicit; pushing the canonical form into the format itself is proportional. | G24 (minor); C14 inventory row. |

### C13 — Molecule (instantiated workflow)

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 molecule = addressable runtime object | simplicity / correctness | **WJ** | M | AI-CONTEXT §3.2 already names molecule; making it addressable with a lifecycle is the minimum. | AI-CONTEXT §3.2 concept 7; G06 (undefined). |
| 02 transactional bind→materialize→seal | failure (half-built tree) | **WJ** | S | "A half-built tree never becomes a runnable molecule" is a real F-class; transactional materialization is standard. | F52, G17. |
| 03 molecule root bead anchor | operability (G17/§16) | **WJ** | S | §16 cold-start query needs an anchor; root-bead is the single anchor. Closes the §16 gap at run level. | AI-CONTEXT §16; G17. |
| 04 tree-shape invariants | correctness | **WJ** | S | Pure invariant-statement; tells everyone the run-bead↔formula-node mapping rule. | C13 inventory row. |
| 05 run-scope loop bound | failure (G18) | **WJ** | M | G18 is a blocker; lifting the bound to the molecule layer gives a concrete owner. | G18 blocker. |
| 06 dependency on C19 directly | inventory-correction / clarity | **WJ** | S | C13 inventory `Depends on: C12, C18` lists C18 as a dep when C18 is actually a *caller*. This is honest correction. | XC-3 / inventory bug. |
| 07 re-instantiation from midpoint | scale (C49 replay) | **WK** | M | C49 is "largely unsolved" (G19); building the molecule-side machinery for an unsolved consumer risks designing in air. | G19; C49 inventory row. |

### C17 — Tool-node abstraction

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 registry + invocation facade | simplicity (G29) | **WJ** | S | "v4 treats abstraction as already-existing" but the seam is unspecified (G29) — this names it. | G29; AI-CONTEXT §13.3. |
| 02 typed node-interface descriptor | correctness | **WJ** | S | Above C02's wire envelope; standard layering. | C02 DELTA-03. |
| 03 determinism-class taxonomy | failure / scale | **WJ** | S | "single deterministic bool → 3-class" is concrete because C49 replay + F52 discipline-linter both need precision. | C49 (replay); F52 (oscillation); F-MODE-COVERAGE §8. |
| 04 result-cache / memoization | cost (P4) | **WJ** | M | P4 promises "tool nodes are cheap and reproducible"; the cache is what operationalizes "cheap." Concrete cost lever. | README P4. |
| 05 built-in/pack parity | simplicity | **WJ** | S | "Callers never branch on origin" — concrete simplicity force. | AI-CONTEXT §3.4 native vs pack. |
| 06 falsifying_scenario_ref obligation | failure (F52) | **WJ** | S | C16 discipline linter cites scenario from prose now; making it a structural field is the right move. | F52; C16 row. |

### C19 — Bead store / typed work-graph

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 file ⇄ Dolt provider seam | simplicity | **WJ** | M | AI-CONTEXT §3.2 explicitly names both backends; one interface is the v4-intended shape. | AI-CONTEXT §3.2 concept 2. |
| 02 created_by NON-NULL invariant | security (G36) | **WJ** | S | G36 says attribution is "optional/deferred"; making the *presence* non-null at the graph layer is the minimum mechanism (signing remains separate). | G36; README P9 "strongest match." |
| 03 typed acyclic edges | correctness / failure | **WJ** | S | `blocks` acyclicity needed for `ready_frontier` termination; standard graph hygiene. | F52, G18. |
| 04 file-provider durability contract | failure (G33) | **WJ** | S | append+fsync+atomic-rename is standard; Phase-0 has no Dolt fallback, so this is the only durability story. | README Phase 0 `[beads] provider="file"`. |
| 05 monotonic `seq` per store | correctness / ordering | **WJ** | S | Cross-session resume requires `seq`; cheap. | AI-CONTEXT §16. |
| 06 bead_format_version envelope | operability | **WJ** | S | Lets store evolve independently of any type's schema — useful given Gas City's migration tail. | AI-CONTEXT §3.5. |
| 07 frozen query contract | parallelizability | **WJ** | M | "Build dependents against stubs before Dolt provider exists" — concrete parallel-build force. | C13/C18/C35/C39 dep chain. |

### C20 — Bead schema registry

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 versioned bead-type registry | correctness (G17) | **WJ** | M | G17 is a blocker; a registry is the minimum response. | G17 blocker. |
| 02 factory_build single type + lifecycle | simplicity | **WJ** | M | "Two types vs one + state" is a real modeling choice; one type preserves stable identity for resume. Breaks §16 query string literally (compat shim noted in OQ1). | AI-CONTEXT §16 hardcoded query; XC-2. |
| 03 closed bead-type catalog | correctness (G17) | **WJ** | M | Direct G17 resolution; the v4 corpus references types but never enumerates them. | G17; README/§16 enumeration. |
| 04 loop-closure schema invariant | failure (G18, F52) | **WJ** | M | G18 ("self-healing has no termination") is a blocker; making bounded-attempt unrepresentable at the data layer is the textbook fix. Caveat: only bounds single-anomaly chains; cross-anomaly oscillation needs C39 — but the delta is honest about that. | G18 blocker, F52. |
| 05 created_by + transfused_from required | security (G36, P9) | **WJ** | S | Schema-mandatory beats "convention"; tiny. | G36; C51. |
| 06 schema-version + write-time validation | correctness | **WJ** | S | Standard schema discipline; the write seam is C19's anyway. | XC-1 / D-4. |
| 07 bead-type ↔ CXDB type-bundle binding | correctness (G17) | **WJ** | M | The bead→CXDB seam is undocumented; D-3 makes this the explicit binding. | XC-4 / D-3. |

### C21 — CXDB trajectory store

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 TrajectoryStore port | simplicity / lock-in | **WK** | L | Self-acknowledged: "does not retire the bet, port thickness is OQ1." Same risk as C01 DELTA-01 — port may be re-implementation. Spec is honest about it, which lifts WK from TA. | AI-CONTEXT §5.1 CXDB internals; spec's own OQ1. |
| 02 append-idempotent by content+parent | correctness / failure | **WJ** | S | Bridge retry-safety is concrete; CXDB already content-addressed so the dedup key is natural. | G26 (at-least-once vs exactly-once). |
| 03 v4 trajectory type bundle pinned | correctness (G17) | **WJ** | S | G17 demands a concrete bundle; this names it. | G17 blocker; D-2. |
| 04 degraded-mode durable spool | failure (G33) | **WJ** | M | G33 is a major gap; spool-to-C23-on-CXDB-down is concrete. Honest scope caveat (raw-bodies path uncovered, handled by C24 DELTA-03). | G33 major. |
| 05 first-class branch/replay API | scale (C49) | **WJ** | M | C49 (counterfactual replay) needs an API contract; "undocumented O(1) trick" → typed surface. | G19; AI-CONTEXT §5.5. |
| 06 retention/GC + integrity-verification | scale / failure | **WJ** | M | v4 claims "TB-scale" but never says how blobs are reclaimed; BLAKE3 self-verify is free. Concrete scale + corruption force. | AI-CONTEXT §5.5 perf contract. |
| 07 typed projection contract | correctness | **WJ** | S | "HTTP/JSON REST hand-wave" → typed queries the loop components actually need. | C36/C37/C38 dep chain. |

### C22 — CXDB type registry & viewpoint tagging

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 concrete v4 trajectory bundle | correctness (G17) | **WJ** | S | Same G17 force as C21 DELTA-03 (D-2 aligned). | G17 blocker. |
| 02 viewpoint as first-class enum | failure (F50) | **WJ** | S | F50 marked "Addressed" via viewpoint, but v4 never defined the enum. This makes the F50 claim honest. | F50; F-MODE-COVERAGE §1. |
| 03 append-only + version-monotonic | correctness | **WJ** | S | Standard registry hygiene; required for replay determinism. | C49 replay. |
| 04 registration mechanism for two namespaces | correctness (D-3) | **WJ** | M | Resolves XC-4 (C20↔C22 collision); D-3 ruling already adopted. | XC-4 blocker; D-3. |
| 05 JSON Schema per type | correctness | **WJ** | S | Without it, "type-aware projection" is aspirational, not real. | AI-CONTEXT §5.5. |

### C23 — Event bus

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 durability/ordering contract | failure (durable fallback) | **WJ** | L | Three sibling specs (C19, C21, C24) lean on this as durable fallback; "JSONL we get for free" is not a contract. Concrete force chain. | C21 DELTA-04; C19 DELTA-05. Spec flags internal tension with DELTA-04 — honest. |
| 02 explicit back-pressure decoupling | failure (G33) | **WJ** | M | G33 cascading-failure question is real; producer-never-blocks + consumer-cursor is standard. | G33. |
| 03 at-least-once + idempotency key | correctness | **WJ** | S | `event_id = (stream, seq)` resolves C19-OQ1 and C21-OQ2. | C19 OQ1, C21 OQ2. |
| 04 partitioned per-run streams | scale / failure | **WK** | L | Force is real (single global JSONL has contention) but the spec itself flags a TENSION with DELTA-01 gap-free `seq`; unresolved internal contradiction. | C23 spec text marks ⚠ TENSION inline. |
| 05 segment + retention contract | scale / failure | **WJ** | M | "Append-only forever" is unbounded; two-sided low-water-mark prevents one-dead-consumer-pins-log DoS. Force is concrete + honest. | C23 own DELTA-05 caveat. |
| 06 schema-on-write envelope | correctness (P9) | **WJ** | S | v4 leaves the JSONL line shape unspecified; minimal versioned envelope is the floor. | AI-CONTEXT §3.2 concept 3. |

### C24 — Telemetry → CXDB ingestion bridge

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 dual-source with one-path-per-event-class | correctness (G27) | **WJ** | M | G27 explicitly names this — v4 ranks event-bus Lowest impedance but builds raw-bodies; this resolves the inversion honestly. | G27 major; AI-CONTEXT §5.4. |
| 02 at-least-once + idempotent posting | correctness (G26) | **WJ** | S | Aligned with C21 DELTA-02 and C23 DELTA-03; resolves G26 explicitly. | G26 major. |
| 03 client-side durable spool | failure (G33) | **WJ** | M | C21 DELTA-04 explicitly does NOT cover raw-bodies path; this owns it. Concrete G33 answer. | G33; C21 OQ2. |
| 04 session.id → parent-turn mapping rule | correctness (G26) | **WJ** | S | AI-CONTEXT §5.4 says "parent-chain via session.id" but never gives the rule; this gives it. | G26. |
| 05 atomic-rename readiness protocol | correctness (G26) | **WJ** | S | G26 names "partially-written body files" as undefined; standard atomic-rename + quarantine. | G26. |
| 06 supervised long-lived daemon, not tool-node | operability | **WJ** | M | C17 tool-node is by design deterministic+finite; a directory-watcher is a daemon. Correct lifecycle modeling. | C17 determinism class; AI-CONTEXT §5.4. |

### C25 — OTLP telemetry export

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 config contract, not running process | simplicity / correctness | **WJ** | M | v4 prose treats C25 as "install/turn on"; specifying it as config-not-daemon avoids inventing a process that doesn't exist. | README Phase 1 §386. |
| 02 Two-Sink Invariant (anti-edge) | correctness (G04) | **WJ** | S | G04 is real; an explicit anti-edge declaration is the minimal mechanism. | G04; AI-CONTEXT §11.1/§11.3. |
| 03 raw-bodies producer contract | security | **WJ** | M | Untruncated request/response bodies are the highest-sensitivity telemetry (secrets, holdout content, full prompts); unowned dir is a real surface. | AI-CONTEXT §4.3 raw-bodies escape hatch; G31. |
| 04 mandatory-on, fail-safe-degrading | failure (F10/F22) | **WJ** | S | Aligns with C28 "telemetry never on hot path" and "observability load-bearing for self-heal." | C28 §Consistency; F10, F22. |
| 05 single factory default for protocol | simplicity | **WJ** | S | 3 OTLP protocols → silent-drop on port mismatch is a real failure class. | AI-CONTEXT §4.3. |

### C28 — Claude Code agent loop

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 AgentLoopProvider abstraction | simplicity / lock-in | **WK** | L | Same C01/C04/C21 pattern — useful conceptually, real risk that the "stable internal contract" mostly recapitulates Claude Code's surface; force = "swap to Agent-SDK fallback" is concrete (G12) but Agent-SDK is an internal Anthropic API. | G12; AI-CONTEXT §4.2 (June-15 Agent-SDK credit). |
| 02 token/quota governor | scale / cost (G13/G34) | **WJ** | M | G13 "token-budget math absent" + G34 "single-seat ceiling" both named; admission control is proportional. | G13, G34 majors. |
| 03 multi-seat / seat-pool | scale (G34) | **WK** | M | Multi-seat under Max is policy-ambiguous (does one user have N Max seats?). The force is real; whether the mitigation is *available* under Max ToS is OQ. | AI-CONTEXT §4.1 OAuth tied to Max. |
| 04 capability/egress profile per invocation | security (G31) | **WJ** | M | G31 blocker; binding C43 profile per invocation is the smallest agent-side response (XC-8 caveat: detection-only until C43 ships). | G31 blocker; XC-8. |
| 05 deterministic context-budget management | failure (F21) | **WJ** | S | F21 cited as "Runtime provides observability to detect exhaustion but doesn't prevent it"; this prevents. | F-MODE-COVERAGE §"Caution" F21. |
| 06 provider-floor conformance suite | failure (F19/F31) | **WJ** | M | F19 "Addressed by declaration" / F31 "single-adapter choice" — making the floor a test, not a declaration, is the named upgrade. | F19, F31. |
| 07 hooks/skills/MCP typed manifest | security / operability | **WJ** | S | Single enforcement seam for C35 override-discipline + C43 isolation — concrete. | AI-CONTEXT §4.4. |

### C29 — Model floor & stylesheet routing

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 model-family declared registry field | correctness (G08) | **WJ** | M | G08 explicitly says "model family" never defined; defining it is the minimum. | G08 major. |
| 02 graded judge_independence_policy L0-L3 | correctness (G08/G20 + D-1) | **WJ** | L | Confronts the genuinely unsatisfiable G08 head-on; D-1 ratifies the L1 baseline as Phase-0. This is the textbook "real engineering judgment" delta. | G08, G20; D-1 in review-log. |
| 03 credential path proposal for 2nd judge family | cost / G20 | **WJ** | M | G20 names judge as unsourced; this turns it into a costed, gated dependency. Honest about being FE-1. | G20; FE-1. |
| 04 compiled deterministic routing | failure (F19/F31) | **WJ** | M | "By declaration" is F19/F31's named weakness; conformance/lint pass is proportional. | F19, F31. |
| 05 cost-tier as live budget input | cost (G32) | **WJ** | M | G32 "cost essentially unmodeled" is major; live budget routing is concrete. | G32 major. |
| 06 fail-closed with auditable degraded_eval | failure (F27/F46) | **WJ** | S | "Silently un-addressed" → explicit operator-accepted degradation. Minimal mechanism. | F27, F46. |

### C41 — Identity / actor model & attribution

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 graduated-mandatory signing | security (G36) | **WJ** | L | G36 is explicit and load-bearing for F32 "Addressed via optional HMAC" (an oxymoron); graduated-tier is the proportional answer. Real ToS-cost question deferred to OQ. | G36; F32; README l.229. |
| 02 typed ActorClass taxonomy | correctness | **WJ** | S | "Loose cities/rigs/agents list" → 7-class enum; minimal. | AI-CONTEXT §3.3; G06. |
| 03 structured Attribution record | security (G31) | **WJ** | M | Bare-string `created_by` cannot answer blast-radius questions; structured record with `on_behalf_of` + `capability_context` is proportional. | G31; C41 spec §1. |
| 04 per-actor tamper-evident hash-chain | security (F14) | **WJ** | M | F14 "Addressed" rests on a chain — D-5 ruling places it here. Concrete + ratified. | F14; D-5 in review-log; XC-5. |
| 05 verify() with three assurance levels | security | **WJ** | S | Consumers choose the bar they need; standard layered-trust API. | G36. |
| 06 signing-key + actor-credential model | security (G36) | **WK** | M | Force real but depends on G37 (no secrets storage); XC-6 flags "signing assurance over-stated while G37 unsolved" — this delta is conditional on a different unsolved problem. | XC-6 in review-log; G37. |
| 07 boundary_class tag (production/twin/isolated) | security (G31) | **WJ** | S | G31 exposure window is open through Phase 3b; tagging makes the period auditable rather than invisible. | G31; C43. |

### C42 — Rig / agent-role partitioning

| Delta | Force claimed | Verdict | Rewind | Reasoning | v4 evidence / lack |
|---|---|---|---|---|---|
| 01 composition order (process-confine → fs → manifest → OPA) | security (G28) | **WJ** | M | G28 names exactly this: three+ mechanisms with no authoritative composition. One ordering is the proportional answer. | G28 major. |
| 02 OS/process boundary enforcement, not prompt discipline | security (G21/G10) | **WJ** | M | G21/G10 explicit: "discipline" is not enforcement. Process-confinement at spawn is the actual mechanism. | G21, G10; README l.177. |
| 03 closed role taxonomy + access matrix | security (D-1) | **WJ** | M | D-1 made worker-judge isolation the load-bearing holdout integrity mechanism. Matrix is the load-bearing artifact. | D-1. |
| 04 worktree-per-run RunPartition | failure (F17) | **WJ** | S | F17 marked "Addressed via worktree isolation per session (native)"; lifecycle-management makes it real. | F17. |
| 05 PartitionBinding verifiable object | security (G21) | **WJ** | M | G21 "detect-only" → prevent-then-detect via the same declared object. Closes the gap. | G21. |
| 06 OPA as optional intra-partition refinement | simplicity (G28) | **WJ** | S | G28 ambiguity on OPA "later" — this pins it as optional refinement, not boundary. | G28; README l.425 "OPA for finer control later." |

---

## Section 2 — Verdict counts

| Verdict | Count | Percent |
|---|---|---|
| WJ Well-justified | 123 | **85.4%** |
| WK Weakly-justified | 20 | **13.9%** |
| TA Taste | 1 | **0.7%** |
| OE Over-engineered | 0 | **0.0%** |
| UN Unclear | 0 | **0.0%** |
| Unique files | 23 | |
| Total deltas | **144** | |

Rewind-cost distribution (approximate): **S ≈ 79 (55%), M ≈ 50 (35%), L ≈ 15 (10%)**. The
large-rewind cluster is exactly the "thin port over Gas City / CXDB / Claude Code" pattern (C01-01,
C04-01, C21-01, C28-01) plus the load-bearing security/policy deltas (C29-02 graded policy, C41-01
graduated signing, C23-01 durability contract).

---

## Section 3 — Patterns

1. **"Port over third-party" is the dominant suspicious pattern.** Five major specs declare a thin
   interface that the adopted vendor "implements" — C01 `RuntimeSubstrate`, C04 `SessionProvider`,
   C21 `TrajectoryStore`, C28 `AgentLoopProvider`, C23 `EventBus` port. Each cites simplicity /
   lock-in / G11. In every case the spec's *own* OQ admits the port may be too thick to be real
   portability (C01 OQ1 cites "~20 Go files for runtime alone"; C21 DELTA-01 says explicitly "does
   not retire the bet"). Force is real but the chosen solution is identical and unproven; this is
   the single pattern most at risk of being defensive lock-in-rationalization rather than
   engineering. Promote one of them as the load-bearing test; treat the rest as WK until that one
   succeeds.

2. **Most "security" deltas in early batches are prevention-by-process-spawn, deferred-detection
   otherwise.** C04 DELTA-05, C28 DELTA-04, C42 DELTA-02 all converge on "enforce at OS/process
   boundary at spawn." This is genuinely strong and proportional. But the *capability* side (C02
   DELTA-04, C28 DELTA-04 enforcement teeth) explicitly relies on C43, which is unbuilt through
   Phase 3b (G31, XC-8). XC-8 already softened this — the pattern is honest about it, but every
   "Addressed" security cell rests on a Phase 3+ component built last in the plan order. **Security
   deltas without C43 are detection-not-prevention dressed in prevention language.**

3. **Schema/registry deltas (C19, C20, C21, C22, C23) are uniformly well-justified — and partly
   forced by ratified D-rulings.** The G17 blocker (no schema for any core store) was specced into
   D-2/D-3/D-4/D-5 between adversary rounds, which converted the most controversial parts of these
   specs into "implement the ruling." Result: the Persistence & Memory subsystem deltas are the
   strongest delta cluster in the corpus.

4. **"Scale" claims have no scale numbers.** Across all 149 deltas, exactly **zero** cite a
   throughput target, a request/second number, a concurrent-session count, or a TB figure with a
   timestamp. G13 ("token-budget math absent"), G32 ("cost essentially unmodeled"), G34
   ("single-seat throughput ceiling"), and C21 §5.5 perf contract ("p50 < 1 ms append for 10 KB
   payloads") are all named but not connected. Several deltas (C05 DELTA-02 admission control, C21
   DELTA-06 retention/GC, C23 DELTA-04 partitioned streams, C28 DELTA-02 governor) cite "scale" or
   "cost" without a number to bound the design against. This is the second-most-suspicious pattern
   after the port pattern.

5. **"Operability/correctness" deltas that close named gaps are uniformly strong; "operability"
   deltas that *introduce* registries/lifecycles tend toward WK.** C20 DELTA-04, C24 DELTA-04, C42
   DELTA-01, C29 DELTA-02 (close G18/G26/G28/G08) are clean. By contrast C07 DELTA-03 (provenance
   field), C12 DELTA-06 (formula provenance duplicating C41/C51), C10 DELTA-05 (rule registry for
   25 INCOSE rules), C13 DELTA-07 (re-instantiation for an unsolved C49 consumer) are mechanism
   added for a need that the corpus doesn't (yet) substantiate. Hygiene-cost is small, but these
   are the deltas that show up as "we did this because it felt right."

---

## Section 4 — Recommendations

### 3 deltas to RESCIND (top "this is taste, drop it" picks)

| # | Delta | Why rescind |
|---|---|---|
| 1 | **C07 DELTA-03** (every glossary term carries provenance/origin field) | Pure metadata-for-metadata; no v4 failure mode cites unknown term origin as a cost. The corpus-name mapping (CorpusTranslationTable) already gives readers the cognitive bridge. Drop the field; keep the table. |
| 2 | **C12 DELTA-06** (formula provenance + transfusion lineage fields *on the formula*) | Duplicates C41 attribution + C51 transfusion provenance. Three places saying "where did this come from" creates three sources of truth and one inevitable drift. Let C51 own transfusion lineage; let C41 own attribution; the formula has neither. |
| 3 | **C13 DELTA-07** (re-instantiation / branch-from-midpoint as first-class molecule op) | The named consumer (C49) is "your most significant invention… largely unsolved" (G19). Building molecule-side machinery for an unsolved consumer designs in air. Defer until C49 has a contract. |

(Also strong candidates if a fourth slot opens: **C10 DELTA-05** explicit INCOSE rule registry — it
treats 25 fixed rules as if they were a plugin ecosystem; **C10 DELTA-06** quality score 0-1 + threshold
gate — risks a fresh F47-shaped Goodhart on the score itself; **C02 DELTA-07** explicit fork-trigger
criteria — useful but pure meta-engineering, two-line note not a delta.)

### 3 deltas to PROMOTE (top "cherry-pick into faithful immediately")

| # | Delta | Why promote |
|---|---|---|
| 1 | **C42 DELTA-02** (read-isolation at OS/process boundary, not prompt discipline) | This is the single delta that converts G21/G10 from "discipline ≠ enforcement" (an acknowledged hole) into a real guarantee. Under D-1 same-provider judging, this is *the* holdout-integrity mechanism. Faithful track currently has nothing equivalent. |
| 2 | **C20 DELTA-04** (bounded fix-attempt chain as schema invariant: `attempt_no`/`max_attempts`/`escalated`/`closes`) | Closes G18 blocker at the data layer. Making termination unrepresentable-to-violate at the bead level is the textbook "make invalid states unrepresentable" move; auditors can prove a loop closed by reading beads alone. The faithful spec leaves this open per the corpus. |
| 3 | **C29 DELTA-02** (graded `judge_independence_policy` L0-L3) | Confronts G08/G20 head-on: the literal v4 rule is unsatisfiable under Max alone. Track A faithful can only ambiguity-flag this; Track B's graded-policy + D-1 ratification gives the project a Phase-0-buildable judge tier *and* a clean FE-1 seam. The faithful spec needs at minimum the L1 default. |

(Also strong candidates: **C01 DELTA-05** bounded reconciliation invariant in the substrate contract;
**C04 DELTA-05** isolation-at-spawn — the same "OS boundary > discipline" pattern as C42-02; **C24
DELTA-04** session.id → parent-turn mapping rule — G26 demands this and faithful can't avoid it.)

---

*Review date: 2026-05-31. Reviewer: Force-Pattern Skeptic (Track B adversary). 144 deltas across 23
spec-optimized files.*
