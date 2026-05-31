# Track B Optimized — Complete DELTA Enumeration

**Cartographer:** Delta Cartographer persona, session 2026-05-31.
**Scope:** All `> [DELTA-NN]` markers across 23 spec-optimized C*.md + 23 plan-optimized C*.md files in `architectures/v4/`. Every row is sourced from the spec header `> Deltas:` block or an inline `> [DELTA-NN]` callout. Plan files confirm implementation task coverage; no additional DELTAs were introduced in plan files.
**Integration Pass 1 resolutions:** D-1 (judge independence Phase-0 baseline), D-2 (bundle-id namespace), D-3 (bead-schema ownership), D-4 (C19↔C20 dependency direction), D-5 (C41 owns hash-chain over C23 event_ids), FE-1 (cross-family judge deferred).

---

## Section 1 — Full DELTA Table (sorted by C-ID, then delta_id)

| component | delta_id | delta_title | v4_or_faithful_says | optimized_says | force_cited | references_other_deltas | references_other_components | resolved_per_integration_pass_1 |
|---|---|---|---|---|---|---|---|---|
| C01 | DELTA-01 | RuntimeSubstrate portability interface | Gas City hardcoded substrate, no abstraction | Thin `RuntimeSubstrate` interface wrapping Gas City; all dependents code against the interface, not Gas City internals | operability, simplicity | — | C02 (tool-node seam) | no |
| C01 | DELTA-02 | Version pin + conformance suite | Gas City version uncontrolled; conformance unspecified | Pin `gc` version; author machine-checked conformance test set gating "Native" claims | operability, failure | DELTA-01 | C02 | no |
| C01 | DELTA-03 | Phase-0 native-count honesty (5 native) | Native capability count unspecified / aspirational | Exactly 5 native capabilities at Phase-0; P3 `[formulas]`-gated; machine-checked assertion not prose | operability, simplicity | DELTA-02 | — | no |
| C01 | DELTA-04 | Tool-node seam typed ABI | Tool-node subprocess invocation implicit / untyped | Tool-node seam is a typed ABI co-specified with C02; C01 owns "the seam exists + is conformance-tested" | simplicity, operability | DELTA-02 | C02 | no |
| C01 | DELTA-05 | Reconciler bounded-iteration invariant | Reconciler loop behavior undefined / unbounded | Per-node iteration cap; escalation to `stuck`/`needs_human` on bound violation | failure, operability | — | C18 | no |
| C01 | DELTA-06 | Degraded-mode / supervised-restart contract | No explicit degraded mode or restart behavior defined | Quiesce store-dependent capabilities on downstream outage; park molecules; replay-on-restart from event bus | failure, operability | DELTA-05 | C23 | no |
| C02 | DELTA-01 | Wire protocol spec | Pack extension protocol implicit / informal | Explicit JSON stdin/stdout wire protocol with content-address-by-reference rule, stderr-for-diagnostics | simplicity, operability | — | C01 | no |
| C02 | DELTA-02 | Signed versioned PackManifest | Pack manifest informal or absent | Signed, versioned `PackManifest` + `ToolNodeManifest` with `abi_version` range, imports, provides, `declared_capabilities`, `transfused_from` | security, operability | — | C43 | no |
| C02 | DELTA-03 | Typed I/O envelope + exit-code taxonomy | Exit codes and I/O shapes ad hoc | Typed `ToolNodeRequest`/`ToolNodeResponse` envelope; closed exit-code taxonomy distinguishing lint-fail from engine-error | simplicity, failure | DELTA-01 | — | no |
| C02 | DELTA-04 | Capability declaration → C43 grant | Capability access uncontrolled | Declared capabilities ∩ (C03/C43 policy) = effective grant; over-grant = load failure; breach = kill + attributed event | security, failure | DELTA-02 | C03, C43 | no |
| C02 | DELTA-05 | ABI version handshake + compat policy | ABI compatibility unspecified | Additive-within-major versioning; range negotiation; typed `AbiIncompatible` failure on mismatch | operability, failure | DELTA-01 | — | no |
| C02 | DELTA-06 | Language-neutral protocol (Go + Python parity) | Protocol implicitly Go-native | Language-neutral wire protocol; Go and Python reference skeletons proving parity | simplicity, parallelizability | DELTA-01 | — | no |
| C02 | DELTA-07 | Fork-trigger criteria explicit | Fork decision undocumented | Named fork-trigger criteria + escape-valve decision template; C24/C33/C36 expressible as zero-Go-import packs | operability, simplicity | — | C24, C33, C36 | no |
| C03 | DELTA-01 | Explicit layer precedence | Layer merge order undefined | Ordered layer stack `core-defaults → pack → city → agent.env → runtime-override`; explicit merge semantics | simplicity, operability | — | C01 | no |
| C03 | DELTA-02 | Capability descriptor registry | Capabilities implicit / undeclared | `CapabilityDescriptor` schema with `{capability_id, gating_section, requires, conflicts_with, schema_ref, default_state}`; formal registration | operability, simplicity | — | C43 | no |
| C03 | DELTA-03 | Secret-reference indirection | Secrets potentially inline in config | `SecretRef` syntax (`secret://`, `${ENV:NAME}`, `file://`) with `SecretResolver` interface; no plaintext-secret lint rejects literals | security, operability | — | C28, C25 | no |
| C03 | DELTA-04 | Load-time validation gate | Config loaded without structural validation | Schema-per-section, transitive `requires`/`conflicts_with` enforcement, unknown-section = error; `ConfigValidationReport` | failure, operability | DELTA-02 | — | no |
| C03 | DELTA-05 | Phase-0 native count 5 / formulas-gated | P3 capabilities ungated / aspirational | Phase-0 profiles as named, validated overlays; P3 gated off at Phase 0 and flips on `[formulas]`; G03 honesty assertion | simplicity, operability | DELTA-01 | — | no |
| C03 | DELTA-06 | Config provenance + attribution | Config load unattributed | Per-(re)load `ConfigProvenance` attributed event to C23 with effective hash + contributing layers | security, operability | — | C23, C41 | no |
| C04 | DELTA-01 | SessionProvider contract (not tmux hardcoded) | tmux hardcoded as the session mechanism | `SessionProvider` contract abstraction; Claude Code / tmux = default adapter; swap-safe | operability, simplicity | — | — | no |
| C04 | DELTA-02 | ResumeToken with fidelity contract | Resume behavior unspecified | `ResumeToken` minting/consumption with explicit fidelity contract; `session.id`↔`gas_city_session_ref` binding | failure, operability | — | C21 | no |
| C04 | DELTA-03 | CredentialSource fallback ladder | Credential selection unspecified | Max-OAuth default adapter + Agent-SDK-credit + metered-API rungs; downgrade-event emission on ladder descent | security, failure | — | C28, C29 | no |
| C04 | DELTA-04 | Heartbeat/liveness as substrate-owned emitted resource | Zombie detection informal | Heartbeat + last-progress emission; `zombie` transition; F22 signal to event bus | failure, operability | — | C23 | no |
| C04 | DELTA-05 | Session as isolation-at-spawn seam | Isolation applied informally or post-spawn | C43 capability profile + C42 work-partition applied at `Create`, before the first command | security, failure | — | C42, C43 | no |
| C04 | DELTA-06 | Multi-session lifecycle (pool / ceiling / drain / restart) | Single-session model; pool behavior unspecified | Session pool with ceiling, ordered drain, supervised restart | scale, operability | DELTA-04 | C28 | no |
| C05 | DELTA-01 | Typed RoutingDecision over RoutingKey | Routing key and decision type informal | `RoutingKey = {agent_role, rig/pool target, model_family, capability_profile_ref}`; `RoutingDecision = {executor, rig_member, model_selection, admission_lease}` | simplicity, operability | — | C09, C12 | no |
| C05 | DELTA-02 | Admission-controlled back-pressure dispatch | No back-pressure mechanism; dispatch unbounded | On governor `back_pressure`, enqueue wisp with aging timestamp; `back_pressured` surfaced to caller; re-attempt on next drive | scale, failure | DELTA-01 | C28 | no |
| C05 | DELTA-03 | Pool routing with fairness + anti-starvation | Pool routing behavior unspecified | `least_loaded | round_robin | affinity` strategy over declared pool; per-rig concurrency caps; anti-starvation aging rule | scale, failure | DELTA-01 | C03, C42 | no |
| C05 | DELTA-04 | Routing-key authority split from binding authority | Authority over routing and binding conflated | C05 owns route/place; C09 owns resolve/bind; opaque binding is a pass-through field, never re-derived by C05 | simplicity, operability | DELTA-01 | C09, C18 | no |
| C05 | DELTA-05 | Convoy = explicit batched dispatch with atomicity policy | Batched dispatch ad hoc / unspecified | `dispatch_convoy(wisps[], atomicity) → ConvoyOutcome`; `all_or_nothing` (rollback partial) vs `best_effort` (per-wisp report); one attribution envelope | failure, operability | DELTA-01 | — | no |
| C05 | DELTA-06 | Idempotent attributable replayable dispatch record | Dispatch record absent; replay unspecified | `DispatchRecord` schema; `dispatch_id = hash({wisp_id, attempt_no})`; dedup on redelivery; new `attempt_no` mints new record | failure, operability | DELTA-01 | C19, C20, C23, C41 | no |
| C07 | DELTA-01 | Machine-readable glossary registry | Glossary prose-only | `GlossaryEntry` schema with `{term, canonical_definition, owning_components, corpus_equivalent, provenance, aliases, deprecated_by, lock_in_cost, extraction_safe_synonym}` | simplicity, operability | — | — | no |
| C07 | DELTA-02 | Authority to pin canonical readings of overloaded terms | Overloaded terms ("layer," "phase") undefined | `CanonicalReading` schema; disambiguation rule; rejected senses; seeds G01 ("layer") and G02 ("phase") | simplicity, operability | DELTA-01 | C10, C15 | no |
| C07 | DELTA-03 | Provenance/origin field + corpus-name mapping | Term origin untraceable | Per-term `provenance` + corpus-equivalent mapping; Gas City / Gas Town term family seeded | operability, simplicity | DELTA-01 | — | no |
| C07 | DELTA-04 | Vocabulary-lint hook → C10 / C15 | No machine-checkable vocabulary enforcement | `CanonicalTermSet` export (content-hashed + versioned) consumed by C10 spec-linter and C15 workflow-linter | operability, simplicity | DELTA-02 | C10, C15 | no |
| C07 | DELTA-05 | Deprecation/alias lifecycle | Deprecation informal | `DeprecateTerm` with `deprecated_by` + named removal version; downstream refs keep resolving | operability, simplicity | DELTA-01 | — | no |
| C07 | DELTA-06 | Per-term lock-in cost + extraction-safe synonym | Lock-in cost unmodeled | `lock_in_cost` field + `extraction_safe_synonym` making Gas City vocabulary replaceable without conceptual loss | simplicity, operability | DELTA-01 | — | no |
| C08 | DELTA-01 | Spec = standalone Markdown bundle (not prompt template) | Spec embedded in or conflated with prompt.template | Spec is a self-contained, independently resolvable Markdown bundle; C09 renders *around* the spec, never *as* it | simplicity, operability | — | C09 | no |
| C08 | DELTA-02 | Multi-file bundle with manifest | Spec = single flat file | Bundle = directory (`spec.md`, `DoD.md`, `spec.toml`); manifest with `spec_id`, `name`, `detail_level`, `references`, `schema_version` | operability, simplicity | DELTA-01 | — | no |
| C08 | DELTA-03 | Enumerated per-criterion-scoreable DoD | DoD prose / unscoreable | `DoD.md` = enumerated criterion list with stable per-criterion IDs; scoring contract for C32/C33; criterion taxonomy (deterministic / scenario-backed / judge-only) | operability, failure | DELTA-01 | C32, C33 | no |
| C08 | DELTA-04 | BLAKE3 content-addressed spec identity | Spec identity informal / mutable | `spec_id = BLAKE3(canonicalized bundle)`; reuses C21 addressing primitive; byte-identical bundles hash identically | security, operability | — | C21 | no |
| C08 | DELTA-05 | Required-section schema (Goal / Constraints / DoD / Out-of-scope) | Spec structure ad hoc | Four required sections with a deterministic validator; C10 lints against this surface | simplicity, operability | DELTA-02 | C10 | no |
| C08 | DELTA-06 | Graded detail + clarification hook | Detail level unspecified | `detail_level` field; `vague` spec triggers clarification hook in C09/C11 before build-token spend | operability, simplicity | DELTA-05 | C09, C11 | no |
| C09 | DELTA-01 | Renders around referenced spec by spec_id | Template renders without explicit spec reference | Prompt template binds to a C08 spec by `spec_id`; resolves to immutable bundle; fail-loud on zero/multiple/unresolvable | simplicity, failure | DELTA-02 | C08 | no |
| C09 | DELTA-02 | Typed render context with closed versioned namespace | Render context untyped / open | Typed `RenderContext` with four roots (`spec`, `bead`, `run`, `actor`) + `context_schema_version`; closed namespace | simplicity, operability | DELTA-01 | C12, C28 | no |
| C09 | DELTA-03 | Content-addressed binding_id record | Binding unrecorded | `binding_id = hash({spec_id, template_id, formula_node_id, agent_role, context_schema_version})`; persisted append-only with `created_by` | security, operability | DELTA-01, DELTA-02 | C19, C23, C41 | no |
| C09 | DELTA-04 | Sandboxed side-effect-free render | Render may call arbitrary functions | Restricted Go `text/template` FuncMap; pure helpers only; no fs/exec/net/env; pack-build-time rejection of non-allowlisted funcs | security, failure | — | — | no |
| C09 | DELTA-05 | Strict-missing-key + prompt.id emission | Missing template keys produce empty string | `missingkey=error` strict mode; `prompt.id` minted and attached; verified on trajectory join via C28→C21 | failure, operability | DELTA-01 | C28, C21 | no |
| C09 | DELTA-06 | Spec-embed strategy (link / inline / summarized) | Embed strategy unspecified | `link`/`inline`/`summarized` selected from `spec.detail_level` + size budget; `summarized` = Goal/Constraints/DoD inlined | operability, cost | DELTA-01 | C29 | no |
| C10 | DELTA-01 | Pure C17 tool node with typed report + stable rule-id taxonomy | Linter untyped / informal | C10 = `pure` C17 tool-node; `LintReport` schema with `Finding`; rule-id families `ears:*`, `incose:Rn`, `vocab:*`, `bundle:*`; score 0–1 | simplicity, operability | — | C17 | no |
| C10 | DELTA-02 | Lint over C08 structured 4-section bundle | Linting freeform text | Lint operates over C08's required 4-section bundle; structural validators tied to C08 DELTA-05 surface | simplicity, operability | DELTA-01 | C08 | no |
| C10 | DELTA-03 | Severity + advisory/blocking disposition graded by detail_level | No graded gate | `gate_result ∈ {pass, advisory, block}` mapped from `(detail_level, score, severity, C03 threshold)`; `advisory` default for vague/moderate specs | operability, simplicity | DELTA-01, DELTA-06 | C03, C18 | no |
| C10 | DELTA-04 | Vocabulary-lint wired to C07 CanonicalTermSet | No vocabulary enforcement | Load C07 `CanonicalTermSet` by content hash; flag undefined / off-canon / deprecated-alias usages | operability, simplicity | DELTA-03 | C07, C15 | no |
| C10 | DELTA-05 | Versioned configurable rule registry R7–R35 | Rules hardcoded / ad hoc | Versioned, content-hashed data file with `{rule_id, family, predicate-ref, default_severity, enabled_default, provenance, rationale}`; config-as-data | operability, simplicity | DELTA-01 | — | no |
| C10 | DELTA-06 | Structural score 0–1 + threshold gate | No quantitative score | Aggregate findings → score; CI-gated threshold (not any-error-blocks) | operability, simplicity | DELTA-03 | — | no |
| C12 | DELTA-01 | Versioned formula schema | Formula schema informal | Versioned TOML grammar with identity / parameters / nodes / edges / gates blocks and `schema_version` doc | simplicity, operability | — | — | no |
| C12 | DELTA-02 | Node taxonomy (agent / tool / gate / sub_formula) | Node types ad hoc | Closed `{agent, tool, gate, sub_formula}` set; per-kind `ref` namespace mapping to C09/C17/C18/C12 | simplicity, operability | DELTA-01 | C09, C17, C18 | no |
| C12 | DELTA-03 | Parameter + binding contract | Parameter binding informal | `FormulaParameters` declaration + resolution to C08 `spec_ref` and C09 `template_ref`; parameter totality fail-closed rule | failure, operability | DELTA-02 | C08, C09 | no |
| C12 | DELTA-04 | Methodology-as-data with FormulaIdentity | Formula methodology implicit | `{name, version, methodology_id, transfused_from}` identity hash; formulas are data, not embedded logic | simplicity, operability | DELTA-01 | C51 | no |
| C12 | DELTA-05 | DAG well-formedness invariants | Graph correctness unverified | Acyclicity, reachability, no-dangling-ref, sub_formula acyclicity; typed diagnostics (`FormulaCycle`, etc.) | failure, operability | DELTA-02 | — | no |
| C12 | DELTA-06 | Formula provenance + transfusion lineage | Provenance untracked | Authoring/promotion emits attributed event (C41); `transfused_from` lineage for C51 | security, operability | DELTA-04 | C41, C51 | no |
| C12 | DELTA-07 | DOT round-trip canonical-form requirement | DOT representation informal / non-round-tripping | Deterministic node/edge/key ordering for `CanonicalForm`; intersection-based DOT vocabulary; out-of-vocabulary rejection | simplicity, operability | DELTA-04 | C14 | no |
| C13 | DELTA-01 | Named addressable runtime object with lifecycle state machine | Molecule = implicit runtime artifact | Molecule = named addressable object with formal lifecycle FSM; root bead as anchor | operability, failure | — | C19 | no |
| C13 | DELTA-02 | Typed transactional bind→materialize→seal | Instantiation non-atomic | `instantiate` = bind→materialize→seal; transactional; mid-instantiation crash yields `instantiation_failed`, never runnable torn molecule | failure, operability | DELTA-01 | C19 | no |
| C13 | DELTA-03 | Molecule root bead as resume/query anchor | Resume behavior unspecified | Root bead is the anchor for gc-converge, resume, and query; `MoleculeState` query contract frozen | failure, operability | DELTA-01, DELTA-02 | C05, C18, C33 | no |
| C13 | DELTA-04 | Tree-shape invariants owned here | Structural invariants distributed / absent | `child_of` tree shape, `blocks` acyclicity, reachability — all owned by C13; structural checks at instantiate | failure, simplicity | DELTA-02 | C19 | no |
| C13 | DELTA-05 | Run-scope loop bound | Loop bounds undefined | Per-node run-scope iteration cap with bounded `fix-attempt` chain; bound violation → escalation | failure, operability | DELTA-04 | C18, C39 | no |
| C13 | DELTA-06 | Dependency on C19 directly (not C18) | C13 believed to depend on C18 at build time | C18 (reconciler) is a runtime collaborator, not a build-time dep; C13 depends on C19; builds and tests with C18 absent | simplicity, operability | — | C18, C19 | no |
| C13 | DELTA-07 | Re-instantiation / branch-from-midpoint as first-class | Branch operation unspecified | `branch(molecule_id, from_node, overrides)` producing shared-history + diverging sibling with `branched_from` lineage; C49/C55 hook | operability, parallelizability | DELTA-02, DELTA-03 | C49, C55 | no |
| C17 | DELTA-01 | Runtime catalog/registry + invocation facade | Tool node invocation ad hoc / unregistered | `ToolNodeRegistry` with `register`/`resolve`/`list`/`is_enabled`; `invoke` facade delegating to C02 wire; global `node_id` uniqueness | simplicity, operability | — | C02 | no |
| C17 | DELTA-02 | Typed NodeInterface descriptor | Node interface implicit | `NodeInterface` = `{node_id, version, input/output schema refs, determinism_class, capability_needs, origin, falsifying_scenario_ref, abi_version}` | simplicity, operability | DELTA-01 | — | no |
| C17 | DELTA-03 | Determinism-class taxonomy (pure / capability-scoped / nondeterministic) | Determinism class unspecified | Closed taxonomy; cacheability + replay + guard implications per class | simplicity, operability | DELTA-02 | — | no |
| C17 | DELTA-04 | Result-cache / memoization for pure + capability-scoped nodes | Caching absent | Cache keyed on `(node_id, node_version, input_hash, granted_caps_hash, abi_version)`; bypass for `nondeterministic` | cost, operability | DELTA-03 | C03, C49 | no |
| C17 | DELTA-05 | Built-in vs pack node parity | Pack nodes second-class | Native and pack nodes both registered and invoked through the same `invoke` facade; parity invariant enforced | simplicity, operability | DELTA-01 | — | no |
| C17 | DELTA-06 | F52 discipline hook as first-class registry obligation | Falsifying scenario reference absent from tooling | `falsifying_scenario_ref` is a queryable registry field; C16 reads it from `list`, not from prose | operability, simplicity | DELTA-02 | C16 | no |
| C19 | DELTA-01 | Single provider-abstraction seam (file ⇄ Dolt) | Single file-based implementation, no abstraction | `BeadStore` port with file provider (default) and Dolt provider (optional); provider-parity contract test suite | operability, simplicity | — | — | no |
| C19 | DELTA-02 | created_by NON-NULL graph invariant | `created_by` optional or missing | Any `create`/`update` with null/unknown `created_by` is rejected; non-null enforced at write seam | security, failure | — | C41 | no |
| C19 | DELTA-03 | Typed + acyclic-by-construction dependency edges with named taxonomy | Edge types informal; acyclicity unverified | `{blocks, child_of, caused_by, closes}` taxonomy; `blocks`-acyclicity invariant at `add_edge`; reject-or-commit | failure, simplicity | — | — | no |
| C19 | DELTA-04 | File-provider durability (append + fsync + atomic-rename) | Durability unspecified / unsafe | Append log + rebuildable indexes; append→fsync→atomic-rename; crash-replay recovery; `seq` = log ordinal | failure, operability | DELTA-01 | — | no |
| C19 | DELTA-05 | Monotonic per-store seq | Ordering undefined | `seq` strictly increases across restart; `seq`-ordered replay reconstructs identical graph | failure, operability | DELTA-04 | C23 | no |
| C19 | DELTA-06 | Schema enforcement via C20 at write seam; C19 owns bead_format_version | Schema validation absent | `create`/`update` calls C20 `validate(bead)` fail-closed; C19 owns `bead_format_version` field | failure, operability | — | C20 | no |
| C19 | DELTA-07 | Graph query contract frozen as stable interface | Query contract informal / unstable | `find(predicate)`, `walk`, `ready_frontier` — frozen, stable signatures; `gc bd find` CLI surface | simplicity, operability | — | — | no |
| C20 | DELTA-01 | Versioned bead-type registry as first-class artifact | Bead types informal / undeclared | Machine-readable registry of all v4 bead types with versioned schemas; the G17 resolution surface | operability, simplicity | — | — | no |
| C20 | DELTA-02 | factory_build / factory_build_in_progress = one type + lifecycle state | Separate types for in-progress and done | Single `factory_build` type with `lifecycle_state` field; `factory_build_in_progress` is a state, not a type | simplicity, operability | DELTA-01 | — | no |
| C20 | DELTA-03 | Closed bead-type catalog resolving G17 | Bead type set open / unspecified | Closed catalog: `override`, `fix_task`, `factory_build`; G17 ("what types exist") resolved | simplicity, operability | DELTA-01, DELTA-02 | — | no |
| C20 | DELTA-04 | Loop-closure contract (bounded fix-attempt chain) | Fix-attempt loop bounds absent | `fix_task` bounded-attempt machine with `attempt_no`/`escalated`/`closes` fields | failure, operability | DELTA-03 | C35, C39 | no |
| C20 | DELTA-05 | created_by + transfused_from as schema-required | Attribution fields optional | Both fields schema-required on all bead types; structural enforcement at write | security, operability | DELTA-01 | C41, C51 | no |
| C20 | DELTA-06 | Schema-version migration + validation gate | Schema changes informal; migration absent | `schema_version` pinning; `migrate()` function; `SchemaChangeEvent` → C23 on version bump | operability, failure | DELTA-01 | C23 | no |
| C20 | DELTA-07 | Bead-type ↔ CXDB type-bundle binding | Binding between bead types and CXDB bundles undefined | C20 authors bead schemas in `softwarefactory.v4.beads` bundle; registers via C22 seam | operability, simplicity | — | C21, C22 | yes (D-2, D-3) |
| C21 | DELTA-01 | TrajectoryStore port wrapping CXDB | CXDB directly accessed by dependents | `TrajectoryStore` port with `AppendTurn`/`PutBlob`/`GetTurn`/`GetBlob`/`WalkTrajectory`/`EnumerateBranches`/`Branch`/`Query` | operability, simplicity | — | — | no |
| C21 | DELTA-02 | Append-idempotent by content + parent | Duplicate turn appends possible | Deterministic `TurnRef` from `(parent, blob_hash, type_triple, attribution)`; dedup-on-append | failure, operability | DELTA-01 | C24 | no |
| C21 | DELTA-03 | v4 trajectory bundle named / versioned / CI-pinned | Bundle namespace informal | `softwarefactory.v4.trajectory` bundle; named, versioned, CI-pinned | operability, simplicity | DELTA-01 | C22 | yes (D-2) |
| C21 | DELTA-04 | Degraded-mode + durable spool; raw-API-bodies durability owned by C24 | No degraded mode; raw-bodies path unspecified | Back-pressure response; non-blocking ingest; drain-from-C23 on recovery; raw-bodies durability explicitly delegated to C24 | failure, operability | DELTA-01, DELTA-02 | C23, C24 | no |
| C21 | DELTA-05 | Branch / replay as first-class API | Branch and replay informal | `Branch` + `BranchRef` + provenance turn + `EnumerateBranches`; O(1) branch isolation; source immutability | operability, parallelizability | DELTA-01 | — | no |
| C21 | DELTA-06 | Retention / GC + BLAKE3 integrity-verification contract | Retention and integrity unspecified | Self-verifying reads; mark-and-sweep compaction; retention policy hooks | security, operability | DELTA-01 | — | no |
| C21 | DELTA-07 | Typed projection contract for read / query | Query contract informal | `Query(typed_filter)`, typed `WalkTrajectory` stream for C36/C37/C38 | simplicity, operability | DELTA-01 | C22, C36, C37, C38 | no |
| C22 | DELTA-01 | Concrete v4 trajectory bundle (softwarefactory.v4.trajectory) | Bundle identifier informal | Concrete bundle id `softwarefactory.v4.trajectory` hardened into the registry | operability, simplicity | — | C21 | yes (D-2) |
| C22 | DELTA-02 | Viewpoint as closed enum (first-class registry-enforced field; F50 mechanism) | Viewpoint informal / unenforced | `viewpoint ∈ {architecture, spec, trajectory, telemetry, control}`; `CheckViewpoint` guard for F50; mismatch on wrong-viewpoint use | failure, simplicity | DELTA-01 | — | no |
| C22 | DELTA-03 | Append-only + version-monotonic registry | Registry mutable / unversioned | New `{bundle_id,type,version}` triple with changed schema rejected; requires `version+1`; old version remains resolvable | failure, operability | DELTA-01 | — | no |
| C22 | DELTA-04 | Registration mechanism for two namespaces | Registration mechanism unspecified | C20 authors bead schemas in `softwarefactory.v4.beads`; C21 authors trajectory types in `softwarefactory.v4.trajectory`; C22 owns only registration | operability, simplicity | DELTA-01 | C20, C21 | yes (D-3) |
| C22 | DELTA-05 | Every type carries machine-checkable JSON Schema | Schema presence unenforced | Every registered type must include a non-empty JSON Schema; `Validate` compiles schemas at load for hot-path cost | operability, failure | DELTA-03 | — | no |
| C23 | DELTA-01 | Named durability/ordering contract (append-atomic, fsync-durable, monotonic gap-free seq) | Event bus ordering and durability unspecified | Per-stream appender; fsync barrier; head-`seq` recovery; torn-trailing-line truncation on restart | failure, operability | — | — | no |
| C23 | DELTA-02 | Back-pressure bounded + explicit; producer never blocks on consumer | Producer can block on consumer | `min(committed_seq)` low-water-mark; bounded back-pressure; `consumer-lag` health signal to C01; producer/consumer decoupled | scale, failure | DELTA-01 | C01 | no |
| C23 | DELTA-03 | Delivery frozen as at-least-once + event_id idempotency key | Delivery semantics unspecified | `Read(from_seq)` + `Tail`; per-consumer `Commit`; resume-from-committed on restart; `event_id = (stream, seq)` idempotency key | failure, operability | DELTA-01 | C24 | no |
| C23 | DELTA-04 | Partitioned streams per run_id / actor | Single monolithic stream | Per-`run_id`/actor streams; size/time-rolled segment files `<stream>/<from_seq>.jsonl`; single-writer-per-segment | scale, operability | DELTA-01 | — | no |
| C23 | DELTA-05 | Segment + retention contract with two-sided prune bound | Retention unspecified | Prune whole segments below low-water-mark by age/reachability; durability floor protects un-ingested data; max-age escalation hook | operability, cost | DELTA-04 | — | no |
| C23 | DELTA-06 | Schema-on-write envelope with created_by NON-NULL | Envelope informal; `created_by` optional | `{event_id=(stream,seq), seq, ts, stream, type, actor, payload}` JSONL schema; non-null `created_by` enforced at emit seam | security, failure | DELTA-01 | C41 | no |
| C24 | DELTA-01 | Dual-source bridge with one canonical-path-per-event-class rule | Bridge logic informal; path per class unspecified | Two adapters (BodyWatcher + BusTailer) with static `kind → {bundle_id,type,version}` map; each event class has exactly one canonical path; rejects misrouted records; resolves G27 | simplicity, operability | — | C21, C23 | no |
| C24 | DELTA-02 | At-least-once + idempotent posting aligned with C21 DELTA-02 + C23 DELTA-03 | Posting semantics unspecified | Idempotent post client over C21 `AppendTurn`; honor `BUSY`/`UNAVAILABLE`; retry+backoff | failure, operability | C21 DELTA-02, C23 DELTA-03 | C21, C23 | no |
| C24 | DELTA-03 | Client-side durable spool + watermark cursor | No durable spool; failure on C21 unavailability | On-disk `inbox/archive/quarantine/cursor` state machine; ack-before-release; crash-safe reload; resolves G33 for raw-bodies class | failure, operability | DELTA-02 | C21 | no |
| C24 | DELTA-04 | Explicit session.id → parent-turn mapping rule | Parent-turn linkage unspecified | `session.id → head TurnRef` durable table; genesis-on-new-session; advance-on-ack; re-root-on-resume; export-order ordinal ordering; resolves G26 | failure, operability | DELTA-03 | C21 | no |
| C24 | DELTA-05 | Partial / torn body-file handling via atomic-rename readiness protocol | Torn file handling absent | Watch `OTEL_LOG_RAW_API_BODIES` dir; readiness via atomic-rename / `.done` / size-stable; quarantine on parse failure | failure, operability | DELTA-03 | C25 | no |
| C24 | DELTA-06 | Bridge as supervised long-lived service; type mapping to softwarefactory.v4.trajectory per D-2 | Bridge lifecycle unspecified | `Health()`, `Start/Stop/Drain` under C01 supervision; `bridge-lag` alarm + retention ceiling; type mapping pinned to D-2 namespace | operability, failure | — | C01, C22 | yes (D-2) |
| C25 | DELTA-01 | C25 = telemetry configuration + enablement contract (not a daemon) | C25 treated as a telemetry process | C25 is a configuration component; its "build" = freezing seams and verifying emitter behavior; no daemon | simplicity, operability | — | C26, C27, C28 | no |
| C25 | DELTA-02 | Two-Sink Invariant (OTLP→Collector→LangFuse AND raw-bodies→C24→CXDB; anti-edge declared) | Data flow between sinks unspecified | Anti-edges declared: "OTLP wire ↛ CXDB; raw-bodies ↛ LangFuse"; testable architectural constraint; resolves G04 | security, simplicity | — | C24, C26 | no |
| C25 | DELTA-03 | Raw-bodies escape hatch as first-class security-bounded output | Raw-bodies handling informal | Inbox dir on C01 isolated mount; write=agent / read=C24 identity; C43 boundary enforced; file-readiness mechanism pinned to C24 DELTA-05 | security, operability | C24 DELTA-05 | C01, C24, C43 | no |
| C25 | DELTA-04 | Telemetry mandatory-on + fail-safe-degrading | Telemetry optional / ungated | Export is async/buffered/bounded-drop; never an agent gate; telemetry-off is a flagged exception | failure, operability | — | C28 | no |
| C25 | DELTA-05 | Per-signal protocol/endpoint pinned to single factory default gRPC :4317 | Endpoint configuration informal | One endpoint/protocol (gRPC :4317); protocol as deployment knob; mTLS required+specified for non-localhost C26 | operability, security | — | C26 | no |
| C28 | DELTA-01 | Provider-abstracted AgentLoopProvider role contract | Claude Code hardcoded as agent loop | `AgentLoopProvider` interface; Claude Code = default floor adapter; swap-safe against the contract | operability, simplicity | — | C04, C29, C43 | no |
| C28 | DELTA-02 | Explicit token/quota governor + admission control | Token/quota management absent | `acquire()` admission control; measured token/cost accounting; seat-pool ledger; back-pressure to C05 | scale, cost | DELTA-01 | C05 | no |
| C28 | DELTA-03 | Multi-seat / seat-pool abstraction | Single-seat model | N Max + Agent-SDK-credit + metered-API seats behind one scheduler; per-seat rate-limit state | scale, cost | DELTA-02 | — | no |
| C28 | DELTA-04 | Capability/egress profile as declared enforced input | Capability enforcement absent | C43 profile bound per invocation; default-deny Bash/network/fs; deny → `tool-denied` | security, failure | — | C43 | no |
| C28 | DELTA-05 | Deterministic context-budget management (max turns/tokens/wall-clock/stuck-detector) | Budget management ad hoc | `max_turns`/token/wall-clock budgets; compaction policy; no-progress detector; breaches map to `AgentOutcome.status` | failure, operability | DELTA-02 | — | no |
| C28 | DELTA-06 | Provider-floor conformance suite | Conformance gate absent | Capability-floor test battery (multi-turn tool use, subagent fan-out, structured-edit fidelity, hook honoring) gating any adapter via C03 | operability, failure | DELTA-01 | C03, C29 | no |
| C28 | DELTA-07 | Hooks/skills/subagents/MCP surface as typed version-pinned config | Hook surface informal | PreToolUse/PostToolUse/SessionStart/Stop chain; MCP mount; subagent registration; typed version-pinned config in C02 pack | simplicity, operability | DELTA-01 | C02 | no |
| C29 | DELTA-01 | model-family is a first-class declared registry field with an explicit independence axis | "model-family" undefined word (G08) | `family = shared-weights lineage`; orthogonal `independence_class` axis (`same-family / cross-family-same-provider / cross-provider`); G08 resolved | simplicity, operability | — | — | no |
| C29 | DELTA-02 | Cross-family rule generalised to configurable judge_independence_policy with graded L0–L3 levels | Binary "different model family" rule (L3); unsatisfiable under Max | Graded enforcement L0 (off) through L3 (cross-provider); L1 (`prompt-independent`) is Phase-0 default — strongest satisfiable under Max | failure, operability | DELTA-01 | C32, C34 | yes (D-1, FE-1) |
| C29 | DELTA-03 | Explicit credential-path proposal for second judge family (metered-API "judge seat") | G20: judge model unsourced, no credential path | Metered-API judge seat; C29 owns the gate; judge-seat credential isolated from Max OAuth; G20 → named costed gated dependency | cost, security | DELTA-02 | — | yes (FE-1 — Phase-0 not mandatory) |
| C29 | DELTA-04 | Routing is a compiled deterministic decision function with conformance/lint pass | CSS text policy interpreted ad hoc | Compiled deterministic function; CSS-cascade by specificity; lint rejects unregistered-model references; closes F19/F31 "by declaration" loophole | simplicity, operability | DELTA-01 | C28 | no |
| C29 | DELTA-05 | Cost-tier becomes live budget-aware input | Static cost-tier label | Routing reads C46/C28 live remaining-budget; downshifts within allowed band under pressure; G32 addressed at routing time | cost, scale | DELTA-04 | C28, C46 | no |
| C29 | DELTA-06 | Fail-closed by default with auditable degraded_eval escape valve | No enforcement when compliance unmet | Refuse dispatch when independence unmet; operator-signed `degraded_eval` acceptance routes at highest satisfiable level, tags scores `independence_degraded`; logged | security, failure | DELTA-02 | C23, C41 | no |
| C41 | DELTA-01 | Signed provenance is graduated-mandatory (not optional/deferred) | Verification "optional, deferred"; F32 "optional HMAC signing" | Config-tiered policy default-on for cross-boundary/security-relevant actions from Phase 0; closes G36 integrity half | security, failure | — | C03, C06 | no |
| C41 | DELTA-02 | Canonical Actor identity model with typed ActorClass taxonomy | Loose "cities, rigs, agents" list | `ActorClass ∈ {human, agent, rig, city, pack, tool_node, external}`; one canonical registry; one identity envelope | simplicity, operability | DELTA-01 | C42 | no |
| C41 | DELTA-03 | created_by is a structured Attribution record with delegation chain | `created_by` = bare string | `Attribution = {actor_ref, on_behalf_of chain, capability_context, boundary_class, assurance, signature, prev_provenance_hash}`; G31 blast-radius answerable | security, operability | DELTA-02 | C19, C23, C42 | no |
| C41 | DELTA-04 | Attribution is append-only and tamper-evident (C41 owns per-actor hash-chain over C23 event_ids) | Audit trail = event bus + bead history; no integrity guarantee | Per-actor provenance hash chain over C23-provided ordered gap-free `event_id`s; C41 owns chain; C23 owns ordered ids; `verify_chain` detects breaks; F14 detectable | security, failure | DELTA-03 | C23 | yes (D-5) |
| C41 | DELTA-05 | Identity verification is first-class service verify(attribution)→Verdict with three assurance levels | Verification absent / self-asserted | `verify(attribution, expected_level?) → {level_met: asserted/signed/attested, ok, reason}`; consumers choose bar | security, operability | DELTA-01 | C06, C34 | no |
| C41 | DELTA-06 | Signing-key / actor-credential model specified | Signature source unspecified (G36) | Per-actor keypair minted at registration; `key_history`; `rotate_key`/`revoke_actor`; trust-rooted at human operator | security, operability | DELTA-05 | C03, C43 | no |
| C41 | DELTA-07 | Attribution carries boundary_class tag (production/twin/isolated) | Boundary labelling absent | Every attribution stamped with `boundary_class` from Phase 0; exposure window auditable before C43/C44 isolation exists; G31 exposure auditable | security, operability | DELTA-03 | C43, C44 | no |
| C42 | DELTA-01 | Partition model + enforcement contract with single authoritative composition order | Three mechanisms named with no composition order (G28) | Ordered stack: process-confinement (mandatory floor) → filesystem perms → declared partition manifest → OPA (optional); resolves G28 | simplicity, failure | — | C04 | no |
| C42 | DELTA-02 | Read-isolation enforced at OS/process boundary (not agent-prompt discipline) | Holdout via "agent-prompt discipline" (G21, G10) | Worker session spawned inside a partition physically unable to open scenario bytes; discipline demoted to defense-in-depth | security, failure | DELTA-01 | C04 | no |
| C42 | DELTA-03 | Roles are closed typed taxonomy worker/scenario-author/judge with declared partition-access matrix | Rig = one loose role | `{worker, scenario-author, judge}` taxonomy; default-deny access matrix; load-bearing cell: worker cannot read scenarios | security, simplicity | DELTA-01, DELTA-02 | C30, C32, C34 | no |
| C42 | DELTA-04 | Worktree-per-run as lifecycle-managed isolation unit (RunPartition) | "Native worktree" mentioned informally | `RunPartition` with explicit create/confine/reap and no-shared-writable invariant; parallel runs cannot clobber or read across each other | failure, operability | DELTA-01 | C28 | no |
| C42 | DELTA-05 | C42 emits verifiable PartitionBinding that C04 enforces and C34 audits | Holdout detect-only; no unified binding object | `PartitionBinding = {run_id, role, actor_ref, readable_roots, writable_roots, run_partition_worktree, composition}`; binding ≡ enforcement ≡ audit; G21 "detect-only" closed | security, failure | DELTA-02, DELTA-03, DELTA-04 | C04, C34, C41 | no |
| C42 | DELTA-06 | OPA positioned precisely as optional intra-partition refinement layer | OPA implied as a primary boundary mechanism | OPA only refines within an already-confined partition; coarse worker/scenario boundary never depends on OPA | simplicity, operability | DELTA-01 | — | no |

---

## Section 2 — Per-Component Summary

| component | name | delta_count | delta_ids |
|---|---|---|---|
| C01 | Gas City Substrate | 6 | DELTA-01 through DELTA-06 |
| C02 | Pack Extension ABI | 7 | DELTA-01 through DELTA-07 |
| C03 | Config / Feature Flags | 6 | DELTA-01 through DELTA-06 |
| C04 | Session Provider | 6 | DELTA-01 through DELTA-06 |
| C05 | Sling Dispatch | 6 | DELTA-01 through DELTA-06 |
| C07 | Vocabulary / Glossary | 6 | DELTA-01 through DELTA-06 |
| C08 | Spec Artifact | 6 | DELTA-01 through DELTA-06 |
| C09 | Prompt Template Binding | 6 | DELTA-01 through DELTA-06 |
| C10 | Spec Linter (EARS) | 6 | DELTA-01 through DELTA-06 |
| C12 | Formula Pipeline File | 7 | DELTA-01 through DELTA-07 |
| C13 | Molecule Runtime State | 7 | DELTA-01 through DELTA-07 |
| C17 | Tool Node Abstraction | 6 | DELTA-01 through DELTA-06 |
| C19 | Bead Work Graph | 7 | DELTA-01 through DELTA-07 |
| C20 | Bead Schema | 7 | DELTA-01 through DELTA-07 |
| C21 | CXDB Trajectory Store | 7 | DELTA-01 through DELTA-07 |
| C22 | CXDB Type Registry | 5 | DELTA-01 through DELTA-05 |
| C23 | Event Bus | 6 | DELTA-01 through DELTA-06 |
| C24 | Telemetry-CXDB Bridge | 6 | DELTA-01 through DELTA-06 |
| C25 | OTLP Telemetry Export | 5 | DELTA-01 through DELTA-05 |
| C28 | Claude Code Agent Loop | 7 | DELTA-01 through DELTA-07 |
| C29 | Model Floor / Stylesheet | 6 | DELTA-01 through DELTA-06 |
| C41 | Identity / Attribution | 7 | DELTA-01 through DELTA-07 |
| C42 | Rig / Agent-Role Partitioning | 6 | DELTA-01 through DELTA-06 |
| **TOTAL** | | **148** | |

---

## Section 3 — Per-Force Histogram

Forces are cited in the spec header delta lists. Many DELTAs cite two forces; each primary force is counted once. Where two forces are co-equal the primary is the one listed first in the spec header text.

| force | delta_count | representative_deltas |
|---|---|---|
| **operability** | 60 | C01-DELTA-01 (substrate contract), C01-DELTA-06 (degraded-mode), C03-DELTA-06 (config provenance), C04-DELTA-01 (SessionProvider), C07-DELTA-04 (vocab-lint), C08-DELTA-02 (bundle manifest), C09-DELTA-02 (typed render context), C10-DELTA-03 (graded gate), C21-DELTA-01 (TrajectoryStore port), C24-DELTA-02 (idempotent posting) — plus 50 more across all 23 components |
| **failure** | 38 | C01-DELTA-05 (reconciler bounded-tick), C04-DELTA-04 (heartbeat/zombie), C09-DELTA-01 (fail-loud on missing spec), C13-DELTA-02 (transactional seal), C19-DELTA-04 (fsync durability), C23-DELTA-01 (fsync-durable seq), C24-DELTA-03 (durable spool), C42-DELTA-02 (OS-enforced isolation), C42-DELTA-05 (PartitionBinding prevent-then-detect) |
| **security** | 22 | C02-DELTA-02 (signed manifest), C02-DELTA-04 (capability grant gate), C03-DELTA-03 (secret-reference), C04-DELTA-05 (isolation-at-spawn), C23-DELTA-06 (created_by NON-NULL), C25-DELTA-02 (Two-Sink Invariant), C25-DELTA-03 (raw-bodies bounded output), C29-DELTA-06 (fail-closed independence), C41-DELTA-01 (graduated-mandatory signing), C41-DELTA-04 (tamper-evident chain), C41-DELTA-06 (signing-key model), C42-DELTA-02/03/05 |
| **simplicity** | 18 | C01-DELTA-03 (native-count honesty), C02-DELTA-01 (wire protocol), C07-DELTA-01 (machine-readable glossary), C08-DELTA-01 (spec ≠ template), C12-DELTA-01 (versioned schema), C17-DELTA-03 (determinism taxonomy), C19-DELTA-07 (frozen query contract), C22-DELTA-02 (viewpoint enum), C29-DELTA-01 (family defined), C42-DELTA-03 (closed role taxonomy) |
| **scale** | 7 | C04-DELTA-06 (multi-session pool), C05-DELTA-02 (admission-controlled dispatch), C05-DELTA-03 (pool routing + anti-starvation), C23-DELTA-02 (back-pressure bounded), C23-DELTA-04 (partitioned streams), C28-DELTA-02 (quota governor), C28-DELTA-03 (seat-pool abstraction) |
| **cost** | 5 | C09-DELTA-06 (embed strategy), C17-DELTA-04 (result cache), C23-DELTA-05 (segment retention), C29-DELTA-03 (metered judge seat), C29-DELTA-05 (live budget-aware routing) |
| **parallelizability** | 3 | C02-DELTA-06 (language-neutral protocol), C13-DELTA-07 (branch-from-midpoint), C21-DELTA-05 (branch/replay first-class) |

**Notes:** operability is dominant at ~41% of all DELTAs. Security-themed DELTAs cluster almost entirely in the Security & Governance subsystem (C41, C42) plus the cross-cutting attribution enforcement (C19-DELTA-02, C23-DELTA-06, C03-DELTA-03). Cost and parallelizability are the least-cited forces, consistent with Track B's stated Phase-0 scope.

---

## Section 4 — Cross-Component Reference Web

The table below shows which components a given component's DELTAs explicitly reference. A reference is counted when the delta title, inline callout, or `references_other_components` field names another C-ID as a co-owner, enforcement target, or consumer of the delta's contract.

| source_component | references_in_deltas | key_dependency_narrative |
|---|---|---|
| C01 | C02, C18, C23 | C01 DELTA-04 co-specifies tool-node seam with C02. DELTA-05 ties to C18 reconciler. DELTA-06 ties to C23 event bus for replay-on-restart. |
| C02 | C01, C03, C24, C33, C36, C43 | C02 DELTA-04 chains capability declaration into C03/C43 policy. DELTA-07 cites C24/C33/C36 as pack candidates. |
| C03 | C23, C25, C28, C41, C43 | C03 DELTA-06 emits provenance to C23/C41. DELTA-03 serves C28/C25 credential seams. |
| C04 | C21, C23, C28, C29, C42, C43 | C04 DELTA-05 enforces C42/C43 binding at spawn. DELTA-03 credential ladder mirrors C28/C29. |
| C05 | C09, C12, C18, C19, C20, C23, C28, C41, C42 | C05 DELTA-06 dispatch record lands on C19/C23 with C41 attribution. DELTA-02 back-pressure signal from C28. DELTA-03 rig set from C42. |
| C07 | C10, C15 | C07 DELTA-04 wires `CanonicalTermSet` to C10 and C15 vocabulary-lint hooks. |
| C08 | C09, C10, C11, C21, C32, C33 | C08 DELTA-01 redraws C08↔C09 line. DELTA-04 reuses C21 BLAKE3 primitive. DELTA-03 feeds C32/C33 DoD evaluation. |
| C09 | C08, C12, C19, C21, C23, C28, C29, C41 | C09 DELTA-01 binds by `spec_id` from C08. DELTA-03 persists to C19/C23 with C41 attribution. DELTA-05 correlates via C28→C21. |
| C10 | C03, C07, C08, C15, C17, C18 | C10 DELTA-01 packages as C17 tool-node. DELTA-04 loads from C07. Gate threshold from C03. |
| C12 | C08, C09, C14, C17, C18, C41, C51 | C12 DELTA-02 maps node kinds to C09/C17/C18/C12. DELTA-06 attribution to C41. DELTA-07 DOT vocabulary co-spec with C14. |
| C13 | C05, C18, C19, C33, C39, C49, C55 | C13 DELTA-06 clarifies C18 is a caller not build-dep. DELTA-07 branch hook for C49/C55. DELTA-03 query contract consumed by C05/C18/C33. |
| C17 | C02, C03, C16, C49 | C17 DELTA-01 delegates to C02 wire. DELTA-06 `falsifying_scenario_ref` consumed by C16. DELTA-04 cache seam with C49. |
| C19 | C20, C23, C41 | C19 DELTA-06 calls C20 validate. DELTA-05 seq mirrors C23. DELTA-02 co-owns `created_by` invariant with C41. |
| C20 | C21, C22, C23, C35, C39, C41, C51 | C20 DELTA-07 binds bead types to C21/C22. DELTA-04 loop-closure bounds touch C35/C39. DELTA-05 attribution via C41/C51. |
| C21 | C22, C23, C24, C36, C37, C38 | C21 DELTA-03 namespace in C22. DELTA-04 degraded-mode uses C23 spool. DELTA-07 typed queries for C36/C37/C38. |
| C22 | C20, C21 | C22 DELTA-04 registration mechanism serves C20 and C21 bundle namespaces. |
| C23 | C01, C41 | C23 DELTA-02 back-pressure health signal to C01. DELTA-06 `created_by` enforcement links to C41 actor model. |
| C24 | C01, C21, C22, C23, C25 | C24 DELTA-06 supervised by C01. DELTA-01 routes to C21 with type map from C22. DELTA-02 aligns with C21 DELTA-02 + C23 DELTA-03. DELTA-05 readiness protocol from C25. |
| C25 | C01, C24, C26, C27, C28, C43 | C25 DELTA-02 Two-Sink Invariant contracts with C24/C26. DELTA-03 raw-bodies seam with C24/C43. |
| C28 | C02, C03, C04, C05, C29, C43 | C28 DELTA-01 consumes C04 session. DELTA-02 back-pressure to C05. DELTA-04 enforces C43 profile. DELTA-06 conformance gates C29. |
| C29 | C23, C28, C32, C34, C41, C46 | C29 DELTA-02 graded policy consumed by C32/C34. DELTA-05 live budget from C46/C28. DELTA-06 resolution records to C23/C41. |
| C41 | C03, C06, C19, C23, C42, C43, C44 | C41 DELTA-04 hash-chain over C23 event_ids (D-5). DELTA-03 attribution embedded in C19/C23. DELTA-07 boundary_class co-consumed with C43/C44. |
| C42 | C04, C28, C30, C32, C34, C41 | C42 DELTA-05 `PartitionBinding` enforced by C04, audited by C34. DELTA-03 role taxonomy governs C30/C32. Attribution via C41. |

**Densest cross-referencing nodes:**
- **C41** is referenced by 15 of the other 22 components (C03, C05, C06, C09, C12, C19, C20, C23, C24, C28, C29, C35, C42, C51, plus C34 audit) — it is the horizontal cross-cutting load-bearer.
- **C23** is referenced by 13 components (C01, C03, C04, C05, C09, C19, C20, C21, C23-self, C24, C29, C41) — the integration bus for all attribution and spool paths.
- **C19** is referenced by 8 components as the bead work-graph write seam.
- **C04** is the enforcement seam for C42/C43 and referenced by C28/C29 credential ladders.

**DELTAs referencing 2 or more other components (cross-component reach ≥ 2 unique C-IDs):**

| delta | components_referenced | count |
|---|---|---|
| C02-DELTA-04 | C03, C43 | 2 |
| C03-DELTA-06 | C23, C41 | 2 |
| C04-DELTA-05 | C42, C43 | 2 |
| C05-DELTA-06 | C19, C20, C23, C41 | 4 |
| C08-DELTA-03 | C32, C33 | 2 |
| C09-DELTA-03 | C19, C23, C41 | 3 |
| C09-DELTA-05 | C28, C21 | 2 |
| C12-DELTA-03 | C08, C09 | 2 |
| C12-DELTA-06 | C41, C51 | 2 |
| C13-DELTA-03 | C05, C18, C33 | 3 |
| C20-DELTA-07 | C21, C22 | 2 |
| C21-DELTA-04 | C23, C24 | 2 |
| C21-DELTA-07 | C22, C36, C37, C38 | 4 |
| C24-DELTA-01 | C21, C23 | 2 |
| C24-DELTA-02 | C21, C23 | 2 |
| C25-DELTA-03 | C01, C24, C43 | 3 |
| C28-DELTA-01 | C04, C29, C43 | 3 |
| C29-DELTA-06 | C23, C41 | 2 |
| C41-DELTA-03 | C19, C23, C42 | 3 |
| C41-DELTA-07 | C43, C44 | 2 |
| C42-DELTA-05 | C04, C34, C41 | 3 |

Total DELTAs referencing 2+ distinct other components: **21**

---

## Appendix — Integration Pass 1 Resolved DELTAs

| delta | ruling | what was resolved |
|---|---|---|
| C20-DELTA-07 | D-2, D-3 | Bead bundle = `softwarefactory.v4.beads`; C20 authors, C22 registers |
| C21-DELTA-03 | D-2 | Trajectory bundle = `softwarefactory.v4.trajectory` |
| C22-DELTA-01 | D-2 | Concrete trajectory bundle named in registry |
| C22-DELTA-04 | D-3 | Registration mechanism — C20 authors, C22 registers only |
| C24-DELTA-06 | D-2 | Type mapping pinned to `softwarefactory.v4.trajectory` |
| C29-DELTA-02 | D-1, FE-1 | L1 same-provider is Phase-0 default; L2/L3 are FE-1 |
| C29-DELTA-03 | FE-1 | Metered judge seat = FE-1, not Phase-0 mandatory |
| C41-DELTA-04 | D-5 | C41 owns hash-chain; C23 owns ordered gap-free event_ids |
