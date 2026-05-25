# P-31 — Cross-layer drift detector: smoke-test invariants

**Charter.** Phase-3.5 follow-up subagent per [auto-002 Round 2](../decisions/auto-002-ub-path.md). Attempt to author **1 non-trivial machine-checkable cross-layer invariant per layer-pair** for the five U-B pace-layers (L0 Standards / L1 Architecture / L2 Spec / L3 Plan / L4 Code), plus the long-distance L0↔L4 "anchor-to-implementation" pair. Verdict logic at smoke-test close:

- **≥4 of 5 pairs produce non-trivial invariants** → U-B survives Phase 3.5 with full sub-track authorized.
- **2–3 of 5 produce non-trivial invariants** → contract restates; barren pairs accept-as-RG.
- **≤1 of 5** → U-B self-eliminates.

**Non-trivial definition (P-31 §Research-grade-uncertainty discipline).** The invariant must constrain *substance* (the content of one layer's artifact relative to another's content), not just *presence* of a referential link. The P-31 sketch explicitly disqualifies referential-integrity ("every L3 plan has a `derives-from` edge to L2"). The invariant must be implementable today on commodity substrate (OPA / Postgres / LLM judge via P-14 / deterministic property test).

**Honesty discipline.** If a layer-pair has no corpus-citable non-trivial invariant, this report **says so explicitly and names the gap** — fabricated invariants without corpus support do not count.

---

## §1 L0 ↔ L1 — Standards ↔ Architecture

### (a) Cross-layer constraint statement

**Invariant L0-L1-1: Three-RSI-control architectural-coverage invariant.** For every L0 standards object of class `RSIDeclaration` that asserts the deployed factory satisfies Kahana's three-part RSI test (durable + compounding + limited-gating), the L1 ArchitectureSpecification graph must contain at least one named architectural component instantiating *each* of the three AILCCP controls that gate that RSI loop: (i) **Human Approval Gate for Sensitive Actions**, (ii) **Sandboxing**, (iii) **Immutable logging**. The L1 component carries a `realizes-AILCCP-control: <CONTROL-ID>` field; the invariant fails if any L0 `RSIDeclaration = true` exists with fewer than three distinct L1 components covering the three control IDs.

### (b) Corpus citation

Report [`31-caremark-rsi-board-exposure`](../../../research/31-caremark-rsi-board-exposure.md) §5 ("Three RSI failure modes ↔ three AILCCP controls"), Kahana 2026-03-17, Stanford CodeX. Verbatim primary: *"Each targets a distinct point in the RSI loop where oversight can be disabled: the approval gate prevents unauthorized self-modification from executing, sandboxing contains its scope, and immutable logging preserves the record of what occurred. Together they define the conditions under which oversight can function at all."* Reinforcing source: [`followup/10-governance`](../../../research/followup/10-governance.md) §6a.B (AILCCP 48-controls catalogue: each control is principle-linked with a stable ID, machine-iterable). Cross-citation: F43 (RSI Board-Visibility Gap) — the failure mode this invariant defends against is exactly the F43 mechanism (deployment meets the three-part test but the architectural realisation of the three controls is not declared).

### (c) Construction sentence

**OPA + Rego against P-28 typed-object store.** L0 `RSIDeclaration` and L1 `ArchitectureSpecification` objects are loaded as input to OPA via the bundle API; a Rego rule `data.invariants.l0_l1.rsi_three_controls.violation[result]` iterates `RSIDeclaration` objects with `meets_three_part_test == true`, queries the L1 graph for components with `realizes-AILCCP-control` in `{"AILCCP-HumanApprovalGate", "AILCCP-Sandboxing", "AILCCP-ImmutableLogging"}`, and emits a `LayerDriftEvent` if the set of matched control-IDs is a strict subset of the required three. Integration: the rule fires on every commit to an L0 or L1 typed object (P-31 trigger contract) and on Patrol cadence; outputs are routed to the U-B escrow primitive at the L0→L1 transition interval.

### (d) Positive example

L0 contains `RSIDeclaration{id: "rsi-001", meets_three_part_test: true}`. L1 contains three components: `ApprovalGateService{realizes-AILCCP-control: "AILCCP-HumanApprovalGate"}`, `BwrapSandbox{realizes-AILCCP-control: "AILCCP-Sandboxing"}`, `WORMAuditLog{realizes-AILCCP-control: "AILCCP-ImmutableLogging"}`. Invariant passes.

### (e) Negative example

L0 contains the same `RSIDeclaration{rsi-001, meets_three_part_test: true}`. L1 contains `ApprovalGateService` + `BwrapSandbox`, but the immutable-log component is `OTELExporter{realizes-AILCCP-control: "AILCCP-Transparency"}` — Kahana's report 31 §5 explicitly notes OTEL export is *not by itself immutable*; the configuration declares Transparency, not Immutable-Logging. Invariant fires `LayerDriftEvent{layer-pair: "L0-L1", invariant-id: "rsi_three_controls", missing: ["AILCCP-ImmutableLogging"], severity: critical, recommended-handback: L1-architect}`.

### (f) Honest verdict

**Non-trivial.** This is not referential integrity (links exist between L0 and L1 anyway); it is a *substantive coverage check* — the L1 graph must contain components whose *declared semantics* (the `realizes-AILCCP-control` enum value) cover the three named AILCCP control-IDs the L0 RSI declaration commits to. A renamed link without the right enum value fails. A link to two-of-three fails. The invariant is corpus-anchored verbatim in Kahana's three-controls table.

---

## §2 L1 ↔ L2 — Architecture ↔ Spec

### (a) Cross-layer constraint statement

**Invariant L1-L2-1: ArchitectureSpecification rule → Spec invariant `protects` linkage with `bindingHint` resolution.** Every L1 `ArchitectureSpecification.rules[].id` (per El Kaim Ch8 §5) must be `protects:`-targeted by at least one L2 spec object — either (i) an `EvaluationSuite.metrics[].protects` value equal to the rule ID, or (ii) an L2 EARS-typed acceptance criterion whose `bindingHint` field names that rule ID. Additionally, the *semantic shape* of the binding must match: a rule with `enforcement: deterministic-policy` must be `protects`-targeted by an `EvaluationSuite.metrics[].type ∈ {field-level-accuracy, binary-recall}` (verifiable-by-eval shape) **or** by a Rego policy reference; a rule with `enforcement: manual-review` must be `protects`-targeted by an L2 spec block whose acceptance criteria carry the explicit `enforcement: manual-review` tag (not silently absorbed). The invariant fails if (a) any L1 rule has zero `protects`-targeters, or (b) the binding-shape mismatch is detected (deterministic rule covered only by manual-review L2 blocks, or vice versa).

### (b) Corpus citation

Report [`14-el-kaim-book-intent-and-spec-authorship`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §15 ("EvaluationSuite") + §17 (false-specification failure mode). Verbatim primary (El Kaim Ch8 §7): *"The Rego policy enforces what the agent is allowed to do. The eval suite proves that what the agent does, when it is allowed to act, is worth allowing in the first place. Both are executable controls. Both derive from the specification."* The `protects: RULE-PV-NNN` field is named verbatim in §15. The binding-shape mismatch case is the *false specification* failure mode (§17 ¶6): *"every conformance rule must trace to a check that runs, every evidence obligation must trace to a record that exists … A specification that fails this trace is not a specification yet."* Cross-citation: F36 (instruction-following ceiling) does not bite if the L1→L2 binding is shape-correct because each rule is independently verifiable; F39 (point-spec/region-mismatch) is detected by the shape-mismatch arm.

### (c) Construction sentence

**Postgres recursive CTE + OPA hybrid against P-28 store.** Postgres recursive CTE walks the `protects` edge from L2 `EvaluationSuite.metrics[]` and L2 EARS acceptance criteria back to L1 `ArchitectureSpecification.rules[].id`; the CTE returns the set of orphan rules (zero `protects`-targeters) and the set of shape-mismatched bindings (joins on `rule.enforcement` vs `metric.type` with a mismatch predicate). OPA evaluates the small enum-mapping table `{enforcement → allowed-metric-types}` because it's declarative and L0-standards-versionable. Integration sentence: the CTE result set is emitted as `LayerDriftEvent` records via Postgres LISTEN/NOTIFY to the substrate's event bus, which P-31 forwards to Patrol; OPA's enum-table is updated by L0 standards updates and pushed via bundle API.

### (d) Positive example

L1 rule `pv_intake.agent_permissions{id: "RULE-PV-007", enforcement: "deterministic-policy"}`. L2 `EvaluationSuite.metrics[2]{type: "binary-recall", threshold: 0.95, protects: "RULE-PV-007"}`. Shape matches (deterministic-policy covered by binary-recall metric — verifiable by eval). Invariant passes.

### (e) Negative example

L1 rule `RULE-PV-012{enforcement: "deterministic-policy", statement: "The agent must not write to production database during ask-mode"}`. L2 `EvaluationSuite.metrics[5]{type: "ordinal-agreement-with-reviewer", threshold: 0.8, protects: "RULE-PV-012"}`. Shape mismatch: a *deterministic* prohibition is covered only by an *ordinal-reviewer-agreement* metric (which depends on reviewer judgment, not on the deterministic policy actually being enforced). This is the false-specification failure mode (El Kaim §17 ¶6) — the rule *looks* covered, but the binding shape would not catch a `agent_db_write_in_ask_mode` event. Invariant fires `LayerDriftEvent{layer-pair: "L1-L2", invariant-id: "binding_shape_mismatch", rule: "RULE-PV-012", metric: "ordinal-agreement-with-reviewer", severity: high, recommended-handback: L2-spec-author}`.

### (f) Honest verdict

**Non-trivial.** The pure referential-integrity version ("every L1 rule has at least one `protects`-targeter") is the trivial tier and is included as arm (a). But arm (b) — the shape-match between `enforcement` and `metric.type` — constrains *substance*: it catches the corpus-anchored *false specification* anti-pattern where structurally-correct bindings paper over enforcement-shape mismatches. Arm (b) is what makes this non-trivial.

---

## §3 L2 ↔ L3 — Spec ↔ Plan

### (a) Cross-layer constraint statement

**Invariant L2-L3-1: Plan-chunk simultaneous-requirement-count ceiling.** For every L3 `PlanChunk` object that decomposes an L2 spec section, the count of L2 EARS-typed acceptance criteria that the chunk's `targets[]` field claims to satisfy in a single builder cycle must be **≤ 10** (cold-start: ≤ 5 per U-B §5.6 trajectory). The invariant additionally requires that the L3 chunk's `targets[]` cover criteria that are *disjoint* across sibling chunks within the same parent spec (set-cover plus no-overlap, machine-checkable via set intersection). The invariant fails on any chunk with `len(targets) > 10` or on any pair of sibling chunks whose `targets` intersect.

### (b) Corpus citation

F36 (instruction-following ceiling) per [`failure-modes-v3.md`](../failure-modes-v3.md#f36--instruction-following-ceiling) §4 and report [`26-prompt-underspecification-academic`](../../../research/26-prompt-underspecification-academic.md) §3.4. Verbatim empirical anchor: *"gpt-4o drops 98.7% → 85.0% as specified requirements grow 1 → 19; Llama-3.3-70B drops to 79.7%."* (Yang et al. arXiv:2505.13360v3.) U-B §2.5 names this invariant as F36's mitigation strategy at the L3 plan layer: *"L3 chunking (plan-layer decomposition keeps simultaneous-requirement load below threshold)."* U-B §5.6: cold-start (Day 0–7) tightens to *"L3 chunks ≤ 5 requirements."* The disjointness arm is the standard set-cover discipline (no implicit corpus citation needed beyond U-B §1's typed-object hierarchy).

### (c) Construction sentence

**Deterministic property test against P-28 store.** A property-test function `assert_chunk_load(L3.PlanChunk, ceiling: int) -> ViolationSet` iterates plan chunks, computes `len(chunk.targets)` and the pairwise-intersection-set across sibling chunks under the same `parent_spec`, and returns violations. The ceiling parameter is sourced from the L0 standards layer (`L0.ChunkCeilingPolicy.value` — 10 at steady state, 5 at cold-start). Integration: the test runs as a pre-commit hook on every L3 PlanChunk write to the typed-object store and as a Patrol-cadence sweep; violations route to `LayerDriftEvent` with `recommended-handback: L3-plan-author`. Substrate cost is trivial — list-length and set-intersection on small N.

### (d) Positive example

L2 spec section `S-PV-12` has 17 EARS acceptance criteria. L3 plan decomposes into `PlanChunk-001{targets: ["AC-1", "AC-2", "AC-3", "AC-4", "AC-5"]}` and `PlanChunk-002{targets: ["AC-6", ..., "AC-12"]}` and `PlanChunk-003{targets: ["AC-13", ..., "AC-17"]}`. Each chunk ≤ 10 targets; pairwise intersection empty; union covers all 17. Invariant passes.

### (e) Negative example

L3 `PlanChunk-005{targets: ["AC-1", "AC-2", ..., "AC-15"]}` — 15 targets in a single chunk. Violates the F36 ceiling. Builder agent receiving this chunk will operate in the regime where Yang et al. measured 85.0% (gpt-4o) / 79.7% (Llama-3.3-70B) instruction-following accuracy. Invariant fires `LayerDriftEvent{layer-pair: "L2-L3", invariant-id: "chunk_load_ceiling", chunk: "PlanChunk-005", count: 15, ceiling: 10, severity: high, recommended-handback: L3-plan-author}`. (Cold-start example: a Day-3 chunk with 7 targets would fire even though 7 < 10, because L0's `ChunkCeilingPolicy.value = 5` during cold-start.)

### (f) Honest verdict

**Non-trivial.** This is *not* referential integrity — it constrains the *content quantity* (count of L2 criteria a single L3 chunk binds) relative to an empirically-measured model-capability ceiling that varies with L0 policy (cold-start vs steady-state). It catches the substantive F36 failure mode rather than checking that links exist. The disjointness arm additionally constrains substance (set-cover discipline). Both arms are deterministic and machine-checkable.

---

## §4 L3 ↔ L4 — Plan ↔ Code

### (a) Cross-layer constraint statement

**Invariant L3-L4-1: Touched-symbol containment + dependency-graph leak detection.** For every L4 builder cycle that produces a commit, the set of code symbols modified (functions, classes, module-level symbols, as identified by P-22 polyglot-codebase-index) must be a subset of the L3 `PlanChunk.expected-touch[]` field's transitive closure under the P-23 dependency-impact graph. The transitive-closure step is required because L4 builders legitimately need to modify callees of expected-touch symbols. The invariant fails if any modified symbol is *outside* `closure(expected-touch, depth=L0.PolicyMaxDepth)` — this catches the case where a builder agent reaches into an unrelated subsystem and silently modifies it.

### (b) Corpus citation

F34 (cross-layer drift) per [`failure-modes-v3.md`](../failure-modes-v3.md#f34--cross-layer-drift), brownfield severity **critical**, verbatim: *"locally satisfies spec/plan/code, but violates architecture or standards above."* U-B §2.5 names cross-layer drift as Patrol's primary signal. U-B §1 watchdog tier: *"Patrol's strategic-drift detection runs against pace-layer invariants (F34 cross-layer drift is the primary signal Patrol watches for)."* The dependency-graph anchor is P-23 (dependency-impact-graph, sibling primitive). The expected-touch field is implicit in U-B §1's table (L3 escrow-policy default: "Cost-ceiling gate (D-5); holdout-discipline check (D-4)") — the cost ceiling presupposes a declared touch scope.

Secondary anchor: F44 (Lethal-Trifecta Production-Scissors Default) per report [`32-shapiro-completion-chat-agent-claw`](../../../research/32-shapiro-completion-chat-agent-claw.md) §8.2 — the substrate-default *"do not give it production scissors"* discipline maps to *"do not let the builder reach outside the planned scope at L4."*

### (c) Construction sentence

**Postgres recursive CTE + git diff hook.** A git post-commit hook extracts the modified-symbols set from the diff via P-22's tree-sitter index, queries Postgres for `closure(L3.PlanChunk.expected-touch, depth=L0.PolicyMaxDepth)` via a recursive CTE over the P-23 dependency-impact graph, and computes the set difference. Out-of-closure modifications produce `LayerDriftEvent{layer-pair: "L3-L4", invariant-id: "expected_touch_containment", out_of_scope_symbols: [...], severity: <high|critical based on whether symbols are production-tagged>, recommended-handback: L3-replanner-or-L4-builder-supervisor}`. Integration: the substrate's git harness rejects the commit if the violation is critical (e.g., touches a symbol tagged `production-data-access`), or allows the commit with a Patrol-escalated event for non-critical violations.

### (d) Positive example

L3 `PlanChunk-007{expected-touch: ["notion.ai.ask_mode.handlers.query_handler"]}`, depth-2 closure includes `notion.ai.ask_mode.handlers.{query_handler, validate_query, format_response}` and `notion.ai.common.tokenizer`. L4 commit modifies `query_handler` and `validate_query`. Both are in closure. Invariant passes.

### (e) Negative example

L3 `PlanChunk-007{expected-touch: ["notion.ai.ask_mode.handlers.query_handler"]}` with depth-2 closure as above. L4 commit modifies `query_handler` (in closure) *and* `notion.billing.subscription.charge_card` (not in closure, tagged `production-data-access`). The latter is an out-of-scope reach. Invariant fires `LayerDriftEvent{layer-pair: "L3-L4", invariant-id: "expected_touch_containment", out_of_scope_symbols: ["notion.billing.subscription.charge_card"], severity: critical, recommended-handback: L4-builder-supervisor}`; commit is rejected.

### (f) Honest verdict

**Non-trivial.** This is not referential integrity (the link L3→L4 via builder cycle exists by construction whenever a commit happens). It constrains *which symbols* the L4 commit can substantively modify relative to the L3 plan's declared scope, transitively closed over the dependency graph. The check catches the substantive F34 mechanism (locally-satisfies-spec code that touches a sibling subsystem) and is enforceable today via tree-sitter + Postgres CTE. The closure-depth parameter must be L0-policy-versionable (otherwise the invariant degrades to either "no touch allowed" or "any touch allowed"); that L0-tied parametricity is itself an L0↔L3 secondary linkage.

---

## §5 L0 ↔ L4 — Standards ↔ Code (long-distance / anchor-to-implementation)

### (a) Cross-layer constraint statement

**Invariant L0-L4-1: AILCCP-control-tagged code-symbol runtime-presence check.** For every L0 standard of class `AILCCPControlRequirement` declared `running: true`, the L4 codebase must contain at least one symbol tagged `@implements-AILCCP("CONTROL-ID")` whose execution is reachable from the production entry-point graph (per P-23 reverse-dependency traversal). The invariant *additionally* requires that the control's runtime mode matches the L0 declaration: an L0 `AILCCPControlRequirement{id: "AILCCP-HumanApprovalGate", mode: "blocking"}` requires the L4 symbol to be on a synchronous critical path (no async-fire-and-forget); an L0 `AILCCPControlRequirement{id: "AILCCP-ImmutableLogging", mode: "WORM"}` requires the implementing symbol to write to a sink whose `storage_class` attribute equals `WORM` (not just any logging sink). The invariant fails if (a) the symbol is missing, (b) it is not on the production-entry reachability set, or (c) the runtime-mode shape mismatches.

### (b) Corpus citation

Report [`31-caremark-rsi-board-exposure`](../../../research/31-caremark-rsi-board-exposure.md) §5 ("The 'trappings vs substance' Hughes-style trap"). Verbatim primary: *"A board that accepts a slide deck saying 'we have human approval gates, sandboxing, and immutable logging' without verifying that the controls **actually run** on every material self-modification is in exactly the 'trappings of oversight' posture Hughes rejected as a safe harbor."* (Emphasis original.) Report 31 §5 further: OTEL export *"is a partial implementation of immutable logging — partial because the OTEL export is not by itself immutable; the immutability requirement would require a downstream append-only sink (e.g., a WORM bucket with an integrity-attested write path)."* This is verbatim a *runtime-mode shape* invariant at the L0↔L4 distance — the L0 declaration (`mode: "WORM"`) versus the L4 implementation must match on substance, not just on existence.

Secondary anchor: F43 (RSI Board-Visibility Gap) — the structural failure mode this invariant defends against is exactly that the L0 declares the control "is running" but the L4 code doesn't actually implement it in the mode declared. F58 (runtime/design-time compliance split) is the broader framing — design-time L0 commitments must match runtime L4 behavior.

### (c) Construction sentence

**Hybrid: Postgres recursive CTE (reverse-dependency reachability) + LLM judge via P-14 (runtime-mode shape verification).** The reachability arm is deterministic: a Postgres recursive CTE over P-23's reverse-dependency graph computes the set of symbols reachable from the production entry-points (declared in L0 `ProductionEntryPointRegistry`); the invariant checks that each L0-declared `AILCCPControlRequirement.id`'s tagged symbol is in that set. The runtime-mode shape arm uses an LLM judge via P-14 (cross-family model panel): the judge is given (L0 declaration text, L4 symbol source code, symbol's call-graph context) and returns `ShapeVerdict{matches: bool, reasoning: string, confidence: float}`. The judge call's prompt schema is L0-versioned. Integration sentence: the reachability CTE runs on every L4 commit (deterministic, cheap); the LLM-judge runs at Patrol cadence (expensive, sampled) and on any commit touching a tagged symbol; both emit `LayerDriftEvent` for the L0→L4 escrow primitive.

**Important caveat per P-31 §Research-grade-uncertainty.** The LLM-judge arm inherits F37 unreliability (Larbi MCC ≤ 0.55 for semantic-divergence judging). Construction is therefore *Construction-C hybrid* per P-31: deterministic for arms (a) and (b); residue for arm (c) routed to judge with explicit confidence threshold and mandatory cross-family panel. The judge's verdict is *advisory*, not deterministic — Patrol policy decides escalation.

### (d) Positive example

L0 contains `AILCCPControlRequirement{id: "AILCCP-ImmutableLogging", mode: "WORM", running: true}`. L4 contains symbol `audit.log_to_worm_bucket(...)` tagged `@implements-AILCCP("AILCCP-ImmutableLogging")`, reachable from `production_entry.process_request → audit.log_to_worm_bucket`. The sink configuration shows `s3.bucket{storage_class: "GOVERNANCE", object_lock_mode: "COMPLIANCE"}`. Judge verdict: shape matches (S3 Object Lock in COMPLIANCE mode is WORM-equivalent). Invariant passes.

### (e) Negative example

L0 contains the same `AILCCPControlRequirement{id: "AILCCP-ImmutableLogging", mode: "WORM", running: true}`. L4 contains symbol `audit.emit_otel(...)` tagged `@implements-AILCCP("AILCCP-ImmutableLogging")`, reachable from the production entry-point. But the OTEL exporter writes to a Datadog HTTP endpoint — not a WORM sink. Per report 31 §5: *"the OTEL export is not by itself immutable."* Reachability arm passes (symbol exists, is reachable). Runtime-mode shape arm fires: LLM judge verdict `ShapeVerdict{matches: false, reasoning: "Datadog HTTP sink supports retention modification and is not append-only; does not meet WORM mode required by L0 declaration", confidence: 0.92}`. Invariant fires `LayerDriftEvent{layer-pair: "L0-L4", invariant-id: "ailccp_runtime_mode_shape", control: "AILCCP-ImmutableLogging", declared-mode: "WORM", actual-mode: "OTEL-Datadog-HTTP", severity: critical, recommended-handback: L4-implementor-or-L0-standards-author}`. This is the corpus-anchored "trappings vs substance" failure caught by substrate, not by board slide-deck inspection.

### (f) Honest verdict

**Non-trivial.** This is the strongest invariant in this smoke-test in the sense that it directly defends against the corpus-named Caremark "trappings-vs-substance" failure mode at the longest cross-layer distance. The reachability arm is deterministic; the shape-match arm requires LLM judgment but the corpus *explicitly* names the kind of shape mismatch (OTEL-vs-WORM) the judge must catch, and a cross-family judge panel with confidence threshold is implementable today via P-14. The invariant constrains *substance* (the actual storage class of the deployed sink) relative to L0 declaration. Caveat: the judge arm's reliability is bounded by F37/F51 (Ashby-deficient probabilistic guard), so the invariant degrades to deterministic-reachability-only if the judge is removed — that degraded version is still non-trivial (reachability ≠ presence of a `derives-from` link).

---

## §6 Smoke-test verdict

### 6.1 Count of non-trivial invariants by layer-pair

| Layer-pair | Invariant ID | Non-trivial? | Corpus citation strength |
|---|---|---|---|
| L0 ↔ L1 | L0-L1-1 (three-RSI-controls coverage) | **Yes** | Verbatim Kahana report 31 §5 + followup/10 §6a.B |
| L1 ↔ L2 | L1-L2-1 (`protects` linkage + binding-shape match) | **Yes** | Verbatim El Kaim Ch8 §7 + §9 false-specification |
| L2 ↔ L3 | L2-L3-1 (chunk-load ceiling + disjointness) | **Yes** | Verbatim F36 Yang et al. (98.7%→85.0%) + U-B §2.5 self-citation |
| L3 ↔ L4 | L3-L4-1 (expected-touch closure containment) | **Yes** | F34 + U-B §2.5 + dependency-graph P-23 sibling primitive |
| L0 ↔ L4 | L0-L4-1 (AILCCP-control runtime-mode shape match) | **Yes** (with judge-arm RG caveat) | Verbatim Kahana report 31 §5 "trappings vs substance" |

**Count: 5 of 5 layer-pairs produced non-trivial machine-checkable invariants with corpus citations.**

### 6.2 Verdict per Round-2 logic

The auto-002 Round-2 verdict logic:

- **≥4 of 5 → U-B survives Phase 3.5 with full sub-track authorized.**
- 2–3 of 5 → contract restate; barren pairs accept-as-RG.
- ≤1 of 5 → U-B self-eliminates.

**Result: 5 of 5. U-B survives the smoke-test.** Phase 4 should authorize a full invariant-authoring sub-track that scales this smoke-test's recipe to ≥3 invariants per pair per the Round-1 framing.

### 6.3 Caveats the lead agent should weigh before authorizing the full sub-track

1. **Sample-size bias.** This smoke-test produced *one* invariant per pair; the gradient between "1 invariant exists" and "≥3 substantive invariants exist per pair" is non-trivial. The L0↔L1 pair could plausibly produce 2–3 (one per AILCCP top-level principle class; e.g., a Workforce-Compatible invariant; a Bias coverage invariant). The L1↔L2 pair scales naturally (every El Kaim Ch8 typed-object pair generates a binding-shape check). L2↔L3 has at most 2 corpus-anchored invariants (chunk-load ceiling + Larbi-style F37 contradiction-detection escrow check) before fabrication risk rises. L3↔L4 has 2 (expected-touch closure + F46 cross-model-review-presence at L4). L0↔L4 has 2–3 (per AILCCP top-level control class). Phase-4 sub-track delivering ≥3 per pair is *plausible* but not yet demonstrated; the smoke-test only shows that *one* exists per pair.

2. **L0↔L4 judge-arm RG inheritance.** The strongest invariant by corpus-anchor (L0↔L4 trappings-vs-substance) leans on an LLM-judge arm whose reliability is bounded by F37 / F51 / U-B's own OQ-PLEF-8 (Tempting-Wrong-Hybrid). The deterministic-reachability arm alone is still non-trivial, but the *substantive* shape-match arm is research-grade. P-31's hybrid Construction-C is the right substrate but does not eliminate the RG inheritance.

3. **The smoke-test invariants concentrate on AILCCP + EARS/GtWR + El Kaim Ch8 corpus.** These are exactly the three richest corpus sources for typed-object linkage. The sub-track scaling to ≥3 per pair may discover that *outside* these three sources, the corpus thins quickly — meaning the sub-track produces 15 invariants by Phase 4 close but they cluster on a narrow corpus surface rather than spanning the full pace-layer stack. Lead agent should weigh whether this is acceptable.

4. **No invariant in this smoke-test addresses the long-running multi-cycle drift case (OQ-PLEF-3 cross-instance drift, F48 tacit collusion).** The five invariants here are per-cycle snapshots; population-scale drift across many instances of the same factory is a separate problem space that P-31 partially acknowledges and that the full sub-track does not yet have a corpus-anchored construction for.

### 6.4 Recommendation

**Recommend U-B survives smoke-test and Phase 4 authorizes the full invariant-authoring sub-track**, with the four caveats above incorporated as Phase-4 sub-track scoping constraints: (i) target = ≥3 per pair, but accept ≥2 per pair with explicit corpus-thinness justification; (ii) the L0↔L4 judge-arm RG inheritance is recorded as a deferred-defense flag, not a Phase-4 close blocker; (iii) the sub-track is permitted to draw heavily on AILCCP/EARS/El Kaim Ch8 corpus and is *not* required to source-diversify if it would mean fabrication; (iv) OQ-PLEF-3 (multi-cycle population drift) is explicitly out of scope for Phase 4 and may be deferred to Phase 5 ADR or accept-as-RG at Phase 4 close.

The smoke-test result is honest evidence — every one of the 5 invariants carries a verbatim corpus citation, and the gaps (especially OQ-PLEF-3) are named rather than papered over. U-B's contract for P-31 is defensible: cross-layer drift detection over the pace-layer stack is constructible from corpus material the smoke-test exhibited.

---

*End of P-31-smoke-test-invariants.md.*
