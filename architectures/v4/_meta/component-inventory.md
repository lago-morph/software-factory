# Canonical Component Inventory — Software Factory v4

**System summary.** Software Factory v4 is a principle-bound *runtime substrate* (Gas City + Claude Code, extended only via packs) through which a human-authored **spec** flows into running software, while a parallel held-out **scenario/judge** stream measures satisfaction, an **observability → anomaly → diagnosis → fix** loop self-heals failures, and a **self-optimization** loop tunes the runtime's own meta-performance. Everything is built on a content-addressed trajectory store (CXDB) + a typed work-graph (beads) with universal actor attribution, and the whole thing is delivered by a *recursive bootstrap* in which the factory builds its own next components via gene-transfusion from external exemplars under human design review. The load-bearing transform is "specs in → satisfying software out, with every action attributed and every failure routed back as a new bead."

This inventory fuses the structural lens (A__), the dataflow/lifecycle lens (B__), and the adversarial gap analysis (G__) into one canonical backbone. Each row is a thing we can write a self-contained spec + plan doc for. IDs `C01…` are FINAL and load-bearing — reference them everywhere downstream.

---

## Canonical components

| ID | Name (`slug`) | Subsystem | Kind | One-line description | Maps from | Depends on | Key gaps | Foundational? |
|---|---|---|---|---|---|---|---|---|
| C01 | Gas City runtime substrate (`gas-city-substrate`) | Runtime Substrate | subsystem | Load-bearing third-party runtime: DOT-shaped TOML workflow runner + agent dispatch + persistence; covers ~5–6 principles natively at min install | A07, A01, A03, A19f-host, B19 | C03, C04 | G11, G03 | yes |
| C02 | Pack & tool-node ABI (`pack-extension-abi`) | Runtime Substrate | interface | The sole v4 extension surface: distributable bundle (TOML + tool-node binaries + templates) and the subprocess tool-node input/output protocol; no Go fork | A22, A101, A108, B57, B72 | C01 | G29, G06 | yes |
| C03 | Layered config / feature-flag model (`config-feature-flags`) | Runtime Substrate | data-store | Layered TOML where section presence enables a capability (`[formulas]` on, etc.); drives all feature gating | A26, B70 | C01 | G03, G37 | yes |
| C04 | Session & provider runtime (`session-provider`) | Runtime Substrate | component | Stable provider-backed runtime (tmux/k8s/subprocess) with cross-session continuity and resume | A27, A20b, B73, B85 | C01 | G12 | no |
| C05 | Sling / dispatch (`sling-dispatch`) | Runtime Substrate | component | Routes a bead/wisp to an agent or pool by template/role | A09b, A22h, A22f, A22g, B25 | C01, C18 | — | no |
| C06 | Messaging (Mail + Nudge) (`agent-messaging`) | Runtime Substrate | component | Inter-agent coordination: Mail durable, Nudge ephemeral; optional HMAC signing | A22d, A28k, B71 | C04 | G36 | no |
| C07 | Vocabulary & glossary (`vocabulary-glossary`) | Runtime Substrate | cross-cutting | Canonical glossary for cities/rigs/formulas/molecules/sling/wisp/Order etc.; mitigates lock-in and undefined-term debt | A22j, A22i, A22k, A22l, A103, B-vocab | C01 | G06 | yes |
| C08 | Spec artifact & format (`spec-artifact`) | Spec Intake | artifact | Load-bearing source-of-truth that drives execution (code disposable); version-controlled spec format | A30, A14, A95, B26, B82 | C03 | G16 | yes |
| C09 | Prompt template & spec→execution binding (`prompt-template-binding`) | Spec Intake | interface | Go text/template + Markdown that becomes the agent's instruction; binds which spec drives which work | A28, A32b, B27 | C08, C05 | — | yes |
| C10 | Spec linter (EARS / INCOSE) (`spec-linter-ears`) | Spec Intake | component | Deterministic structural rules over specs (INCOSE R7–R35); addresses prose-rigor / vocab-lint debt | A32, B69 | C08 | — | no |
| C11 | Intent intake (9-field crucible) (`intent-intake`) | Spec Intake | component | Structured 9-field intent capture (GF-C transfusion); addresses under-defined-intent debt | A97, A149 | C08 | G23 | no |
| C12 | Formula / pipeline-file format (`formula-pipeline-file`) | Workflow Engine | artifact | TOML DAG describing the workflow; methodology lives here, not in prompts | A33, A16, A96, B28 | C01, C03 | G06 | yes |
| C13 | Molecule (instantiated workflow) (`molecule-runtime-state`) | Workflow Engine | artifact | A formula instantiated into a live bead-tree for a specific run; the runtime state of an in-flight workflow | A22b, B32 | C12, C18 | — | no |
| C14 | Formula↔DOT translator + visualizer (`formula-dot-translator`) | Workflow Engine | interface | Bidirectional formula/DOT conversion for visualization + DOT-ecosystem linting; round-trip fidelity must be proven | A37, A34, A37b, B29 | C12 | G24 | no |
| C15 | Workflow linter (Mammoth 21-rule) (`workflow-linter`) | Workflow Engine | component | Structural rules over the DAG; flags malformed workflows (Mammoth transfusion) | A34b, B30 | C14 | G30 | no |
| C16 | Discipline linter (LLM-where-tool) (`discipline-linter`) | Workflow Engine | component | Flags LLM nodes used where a deterministic tool suffices; each guard must cite a falsifying scenario | A36b, B31, B75 | C12 | G18 | no |
| C17 | Tool-node abstraction (`tool-node-abstraction`) | Workflow Engine | component | Unified interface for deterministic steps (Gas City tool beads) | A35, A17 | C02 | G29 | yes |
| C18 | Reconciler / Health Patrol loop (`reconciler-convergence`) | Workflow Engine | control-loop | Per-tick desired-state convergence with bounded gates; deterministic-first | A36, A22e, B07, B59 | C01 | G18 | no |
| C19 | Bead store / typed work-graph (`bead-work-graph`) | Persistence & Memory | data-store | Durable typed work-graph (file or Dolt) with dependencies; the memory layer surviving across sessions | A20, A19e, A21b, B44 | C01 | G17 | yes |
| C20 | Bead schema registry (`bead-schema`) | Persistence & Memory | data-store | Canonical schema for all bead types (`override`, `fix_task`, `factory_build_in_progress`, etc.) | A90, A91, A92, A58b, B37-schema | C19 | G17, G18 | yes |
| C21 | CXDB trajectory store (`cxdb-trajectory-store`) | Persistence & Memory | data-store | BLAKE3-addressed turn-DAG store: dedup, O(1) branching, replay; HTTP + binary ingest APIs | A21, A21c, A21d, A21e, A21g, A21h, A21i, B43 | C01 | G17, G33 | yes |
| C22 | CXDB type registry & viewpoint tagging (`cxdb-type-registry`) | Persistence & Memory | data-store | Dynamic `{bundle_id,type,version}` type system; viewpoint tagging resolves architecture/spec confusion | A21f | C21 | G17 | yes |
| C23 | Event bus (`event-bus`) | Persistence & Memory | data-store | Append-only JSONL with monotonic seq; records every action; lowest-impedance CXDB source | A29, B46 | C01 | — | yes |
| C24 | Telemetry → CXDB ingestion bridge (`telemetry-cxdb-bridge`) | Persistence & Memory | interface | Standalone tool-node watching raw-API-bodies dir, posting to CXDB HTTP; defines delivery/ordering/back-pressure at the seam | A29b, A29c, A28c, B45 | C21, C28 | G26, G27, G33 | no |
| C25 | OTLP telemetry export (`otlp-telemetry-export`) | Observability | interface | Claude Code native OTLP (metrics/events/traces) + raw-API-bodies escape hatch | A28b, A28c, A23 | C28 | G04 | no |
| C26 | OpenTelemetry Collector (`otel-collector`) | Observability | component | Receives Claude Code OTLP, fans out to LangFuse | A24, B47 | C25 | G04 | no |
| C27 | LangFuse trace store & browser (`langfuse-traces`) | Observability | data-store | Self-hosted LLM trace browsing + session/prompt versioning | A25, A24b, B48 | C26 | G37 | no |
| C28 | Claude Code agent loop (`claude-code-agent-loop`) | Agent Loop | agent-role | Multi-turn reasoning + tool dispatch + provider abstraction under Max; the implementer worker; hooks/skills/subagents/MCP surface | A04, A04b, A05, A28d, A28e, A28f, A28g, A28h, B20, B21 | C04 | G12, G13, G34 | yes |
| C29 | Model floor & stylesheet routing (`model-floor-stylesheet`) | Agent Loop | component | Declares Claude Code as capability floor; CSS-like cost/family-aware model routing rules | A11b, A106, B84 | C28 | G08, G20, G32 | yes |
| C30 | Scenario authoring & store w/ read-isolation (`scenario-store`) | Evaluation & Judge | data-store | Inspect AI scenario DSL authored in an isolated rig; separate repo + perms + partition keep scenarios unread by implementer | A45, A46, A22i-rig, B22, B40 | C17, C42 | G10, G21, G28 | yes |
| C31 | Scenario runner (`scenario-runner`) | Evaluation & Judge | component | Executes scenarios against the system (Inspect AI runner wrapped as pack); needs session-id adapter | A47, A28i, A28j, B42, B49 | C30, C17 | G25 | no |
| C32 | LLM-as-judge harness (`judge-harness`) | Evaluation & Judge | agent-role | Scores work trajectories against scenarios; must be a different model family than coder | A50, A51, A52, B23 | C30, C29 | G08, G20 | yes |
| C33 | Satisfaction metric aggregator (`satisfaction-metric`) | Evaluation & Judge | component | Computes the satisfaction distribution over the trajectory population from judge outputs | A53, A19, B41 | C32, C19 | G09 | yes |
| C34 | Holdout integrity & isolation enforcement (`holdout-integrity`) | Evaluation & Judge | component | Read-isolation policy (perms + OPA + rig partition) + after-the-fact audit; cross-family + independence enforcement | A48, A48b, A48c, A54, A105, B53, B54 | C30, C32 | G10, G21, G08, G28 | no |
| C35 | Override → pattern → rule loop (`override-why-loop`) | Override Discipline | control-loop | Hooks detect operator overrides, prompt "why", log as beads, surface recurring patterns, convert to new validation rules | A38, A39, A40, A41, A42, B09, B67, B68 | C28, C20, C30 | G43 | no |
| C36 | Anomaly detection (numeric) (`anomaly-detection`) | Self-Healing Loop | component | Detects unusual patterns on telemetry/quality metrics (PyOD/Anomalib); first/simplest P11 piece | A56, B33 | C24, C21 | G33 | no |
| C37 | Trajectory embedding & clustering (`trajectory-clustering`) | Self-Healing Loop | component | Embeds trajectories (sentence-transformers) and clusters similar failures (HDBSCAN) for diagnosis | A56b, A56c, B34, B35 | C21 | G32, G33 | no |
| C38 | Diagnosis agent (Healer) (`diagnosis-agent`) | Self-Healing Loop | agent-role | LLM root-cause analysis over clustered failures (Tracker Diagnose/Audit/Doctor transfusion) | A57, B24 | C37, C21 | G30, G07 | no |
| C39 | Fix-task generation & loop-closure (`fix-task-loop-closure`) | Self-Healing Loop | control-loop | Diagnosis → `fix_task` bead re-entering build flow; bead chain proves the fix worked; needs termination/escalation contract | A58, A58b, B36, B37 | C38, C20, C08 | G18, G35 | no |
| C40 | Durable workflow engine (Orders) (`durable-orders`) | Self-Healing Loop | component | Event-triggered workflows surviving crashes/retries (Gas City Orders; Temporal optional) | A59, A22c, B38, B39 | C23 | G33 | no |
| C41 | Identity / actor model & attribution (`identity-attribution`) | Security & Governance | component | Who/what can act (cities/rigs/agents); `created_by` on every action; audit trail; optional signed provenance | A43, A44, A44b, A44c, A19d, B50, B51, A22i | C01, C19, C23 | G36 | yes |
| C42 | Rig / agent-role partitioning (`rig-partitioning`) | Security & Governance | agent-role | Worker/scenario/judge roles with read/write partitions; worktree isolation per run | A22i, A22k, A22l, B85 | C04 | G21, G28 | no |
| C43 | Isolation & lethal-trifecta boundary (`isolation-boundary`) | Security & Governance | cross-cutting | Deterministic boundary typing + twin isolation to bound blast radius; the security posture for Bash/network/fs access | A100-sec, F44-host, B-sec | C42, C44 | G31, G35, G37 | no |
| C44 | Digital twin (per service) (`digital-twin`) | Digital Twins | component | Behavioral clone of a critical external dependency (record/replay + stateful + OpenAPI mock); LocalStack-shaped | A61, A62, A62b, A64, B65 | C17 | G22, G31 | no |
| C45 | Twin contract & fidelity verification (`twin-fidelity`) | Digital Twins | invariant | Verifies twin usage matches service promises and twin behavior matches the real service; needs a "how close is close enough" bar | A63, A64b, B66 | C44, C30 | G22 | no |
| C46 | Meta-metric stream (`meta-metrics`) | Self-Optimization | data-flow | Records cost-per-satisfaction, time-to-threshold, judge-FP-rate over time; needs a defined cost model | A65, A66, A72b, A72d, B12, B-cost | C33, C24 | G09, G32 | no |
| C47 | Variant identification (`variant-identification`) | Self-Optimization | component | Identifies prompt (DSPy) + hyperparameter (Optuna/Ray Tune) variants to experiment with | A67, A68, B64 | C46 | — | no |
| C48 | A/B routing & statistical comparison (`ab-routing-stats`) | Self-Optimization | component | Routes traffic between variants (Unleash/bandit) and determines whether a variant was actually better (scipy/Evidently) | A69, A71, A72c, B60, B63 | C47, C46 | G32 | no |
| C49 | Counterfactual replay driver (`counterfactual-replay`) | Self-Optimization | component | Re-runs a trajectory from a midpoint via CXDB O(1) branching for variant tests; the "most significant invention", largely unsolved | A70, B62 | C21 | G19 | no |
| C50 | Promotion gate (`promotion-gate`) | Self-Optimization | control-loop | Statistical, multi-metric gate deciding a new variant becomes the default; guards Goodhart | A72, B61, B78 | C48, C12 | G18 | no |
| C51 | Gene-transfusion discipline (`gene-transfusion`) | Bootstrap | cross-cutting | Every factory-built component transfuses ≥1 external exemplar; records `transfused_from`; needs a correctness/completeness predicate + license handling | A86, A93, A107, A180-189, B52, B55 | C08, C20 | G07, G14, G30 | yes |
| C52 | Self-bootstrap recursion & design review (`self-bootstrap`) | Bootstrap | control-loop | Factory authors a spec for its own next component, runs, human-reviews before deploy, extends itself; resume of in-progress builds | A84, A87, A85, B06, B17, B56, B80 | C51, C52-gate, C08 | G14, G23 | no |
| C53 | Bootstrap-validation milestone (`bootstrap-validation`) | Bootstrap | artifact | The go/no-go gate: first factory-built component passes review and deploys; needs a rubric/scenario set, not "looks good" | A85, B17 | C52, C33 | G23 | no |
| C54 | Phase delivery plan (`phase-plan`) | Bootstrap | pipeline-stage | Four-phase ordered delivery (P0 foundation → P1 OSS → P2 Layer2+bootstrap → P3 factory-builds-factory) | A80, A81, A82, A83, A83a-d, B11, B13-16 | C52 | G01, G02, G03, G31 | no |
| C55 | Methodology-as-config experiment loop (`methodology-experiment`) | Bootstrap | control-loop | v3's 10 candidates run as swappable pipeline files; empirical results select methodology per work type | A88, A188, B08, B81 | C12, C30, C33 | G05 | no |
| C56 | Autonomy ladder (L0–L5) (`autonomy-ladder`) | Security & Governance | cross-cutting | Maturity scale manual→intern→pair→HITL→PM-mode→dark; v4 targets L4–L5 (out-of-loop batched review) | A13, B10 | C52 | G15, G35 | no |
| C57 | Failure-mode coverage map & residual-risk register (`failure-mode-coverage`) | Security & Governance | cross-cutting | Canonical 61-mode → mechanism mapping (addressed/partial/gap/caution); owns license hygiene + the honest residual/caution register | A100, A102, A104, A109, A110-A169, B58, B74, B75-79 | C51, C43 | G31, G32, G33, G34, G35, G38, G39, G40, G44 | no |

---

## Subsystem groupings

**Runtime Substrate** — C01 Gas City substrate, C02 Pack/tool-node ABI, C03 Config/feature-flags, C04 Session/provider, C05 Sling/dispatch, C06 Messaging, C07 Vocabulary/glossary.

**Spec Intake** — C08 Spec artifact, C09 Prompt template & binding, C10 Spec linter (EARS), C11 Intent intake.

**Workflow Engine** — C12 Formula format, C13 Molecule, C14 Formula↔DOT translator, C15 Workflow linter, C16 Discipline linter, C17 Tool-node abstraction, C18 Reconciler/Health Patrol.

**Persistence & Memory** — C19 Bead work-graph, C20 Bead schema, C21 CXDB trajectory store, C22 CXDB type registry, C23 Event bus, C24 Telemetry→CXDB bridge.

**Observability** — C25 OTLP export, C26 OTel Collector, C27 LangFuse.

**Agent Loop** — C28 Claude Code agent loop, C29 Model floor & stylesheet.

**Evaluation & Judge** — C30 Scenario store w/ isolation, C31 Scenario runner, C32 Judge harness, C33 Satisfaction metric, C34 Holdout integrity enforcement.

**Override Discipline** — C35 Override→pattern→rule loop.

**Self-Healing Loop** — C36 Anomaly detection, C37 Trajectory clustering, C38 Diagnosis agent, C39 Fix-task & loop-closure, C40 Durable Orders.

**Self-Optimization** — C46 Meta-metrics, C47 Variant identification, C48 A/B + stats, C49 Counterfactual replay, C50 Promotion gate.

**Digital Twins** — C44 Digital twin, C45 Twin fidelity.

**Security & Governance** — C41 Identity/attribution, C42 Rig partitioning, C43 Isolation/lethal-trifecta boundary, C56 Autonomy ladder, C57 Failure-mode coverage & residual-risk register.

**Bootstrap** — C51 Gene-transfusion discipline, C52 Self-bootstrap recursion, C53 Bootstrap-validation milestone, C54 Phase plan, C55 Methodology-experiment loop.

---

## Suggested build/spec batches

Ordered by dependency so a downstream orchestrator can fan out wave by wave. Foundational primitives first; later batches consume earlier ones.

**Batch 1 — Foundational primitives (substrate, schemas, vocabulary).** Author fully in parallel: **C01, C02, C03, C07, C08, C17, C19, C20, C21, C22, C23, C41**. These are the load-bearing schemas/interfaces everything else references (substrate, pack ABI, config, spec artifact, tool-node, bead + bead-schema, CXDB + type-registry + event-bus, identity/attribution). C12 (formula format) and C29 (model floor) can also start here as foundational artifacts once C01/C03 shape is fixed.

**Batch 2 — Core build flow + observability.** Depends on Batch 1. Parallel: **C04, C05, C09, C10, C12, C13, C28, C29, C42**, plus observability ingest **C25, C26, C27, C24**. (Session, sling, prompt-binding, spec-linter, formula, molecule, agent loop, model floor, rig partitioning, OTLP→collector→LangFuse, CXDB bridge.) This yields specs-in→software-out with telemetry landing in the stores.

**Batch 3 — Evaluation, workflow tooling, override discipline.** Depends on Batch 2. Parallel: **C06, C11, C14, C15, C16, C18, C30, C31, C32, C33, C34, C35, C40**. (Messaging, intent intake, DOT translator + linters, reconciler, the full scenario→judge→satisfaction tier with isolation enforcement, override loop, durable Orders.) This delivers Layer 2 (P5/P6) and the P8 loop.

**Batch 4 — Self-healing + bootstrap mechanics.** Depends on Batch 3. Parallel: **C36, C37, C38, C39, C43, C44, C45, C51, C52, C53, C54, C55, C56**. (Anomaly→cluster→diagnose→fix loop-closure, isolation boundary + twins, gene-transfusion discipline, self-bootstrap recursion + validation milestone + phase plan + methodology loop + autonomy ladder.) This is "factory builds factory".

**Batch 5 — Self-optimization (research frontier, built last).** Depends on Batch 4. Parallel: **C46, C47, C48, C49, C50, C57**. (Meta-metrics, variant ID, A/B + stats, counterfactual replay, promotion gate; plus the consolidated failure-mode coverage / residual-risk register that can only be finalized once all mechanisms exist.)

---

## Dependency notes — critical path

The critical path runs through the persistence + evaluation + bootstrap spine; these are the components that gate the largest number of downstream specs:

1. **C21 CXDB trajectory store** (+ C22 type registry) — every observability, clustering, replay, and loop-closure component reads/writes here. Resolves the most foundational gaps (G17 schemas, G11 content-addressing). No exemplar for the v4-specific type bundle, so spec this first and carefully.
2. **C20 Bead schema** (on C19 bead store) — `override`/`fix_task`/`factory_build_in_progress` types are referenced by override loop, self-heal, and bootstrap resume; G17/G18 make this a blocker until defined.
3. **C32 Judge harness + C29 Model floor/stylesheet** — the cross-family-judge requirement (G08/G20) is in direct tension with the single-Max-adapter floor; this unsolved sourcing question gates the entire evaluation tier (C30–C34) and meta-metrics (C46).
4. **C51 Gene-transfusion discipline** — Phases 3b/3c/3d (self-heal, twins, self-opt) are all gated on this "bet" (G07/G14); without a correctness predicate the whole factory-builds-factory plan (C52–C54) has no acceptance contract.
5. **C49 Counterfactual replay driver** — the single hardest, admittedly-unsolved invention (G19); the self-optimization batch (C46–C50) cannot close without it. Highest-risk leaf on the critical path.

Cross-cutting load-bearers that touch nearly everything but are not on a single linear path: **C41 identity/attribution** (every action), **C57 failure-mode coverage** (the integration/residual-risk ledger, finalized last), and **C43 isolation boundary** (the security posture that is "Addressed on paper" but unbuilt through Phase 3b — G31).
