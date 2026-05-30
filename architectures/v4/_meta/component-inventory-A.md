# Component Inventory A — Cartographer A (structural / component-oriented)

**System summary.** Software Factory v4 is a principle-bound *runtime* (substrate) for an AI software factory: it builds the engineering substrate that satisfies 12 working principles, then runs methodologies as swappable pipeline-file configurations on top, with Gas City + Claude Code as the load-bearing baseline and a self-bootstrapping "factory-builds-factory" delivery plan. The architecture is organized as a convergent three-layer-plus-persistence shape (LLM client / agent loop / pipeline engine / persistence) elaborated into six capability layers (L2 scenarios+judge, L3 observability, L4 self-healing, L5 twins, L6 self-optimization) targeting L4-L5 autonomy.

**Decomposition lens.** Structural / component-oriented. Every named component, subsystem, interface, store, agent role, pipeline stage, workflow, artifact, failure mode, and cross-cutting concern the v4 docs mention gets an entry. Source abbreviations: `RM` = README.md, `AC` = AI-CONTEXT.md, `FM` = F-MODE-COVERAGE.md, `OS` = one-shot-specs-and-research.md.

---

## Subsystems (architectural layers / capability tiers)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A01 | Three-layer-plus-persistence convergent shape | subsystem | Canonical architecture: human surface → pipeline engine → agent loop → LLM client, with persistence underneath | RM Part 3; AC §2 | A02,A03,A04,A05,A06 | The convergent finding from the corpus; every working factory lands here |
| A02 | Human surface (CLI / web / IDE) | subsystem | Operator entry point into the factory | RM Part 3 diagram | A03 | Top rung of convergent diagram |
| A03 | Pipeline engine | subsystem | DOT-shaped workflow runner; baseline = Gas City | RM Part 3; P2; AC §2 | A04,A05,A07 | Methodology lives in the pipeline file, not prompts |
| A04 | Agent loop | subsystem | Multi-turn reasoning + tool dispatch; baseline = Claude Code CLI | RM P2; AC §2 | A05 | Candidates: Claude Code, OpenHands, Overstory, Codex |
| A05 | LLM client | subsystem | Model-provider abstraction / routing | RM P2; AC §2 | — | Claude Code under Max, or LiteLLM when not on Max |
| A06 | Persistence layer | subsystem | Event store (CXDB) + work ledger (Beads) | RM P2; AC §2 | A20,A21 | Underpins attribution + memory |
| A07 | Gas City runtime baseline | subsystem | Load-bearing third-party substrate covering principles 1,2,3,4,9,10 natively | RM P2; AC §3 | A20,A22 | Extended via packs, no Go fork |
| A08 | Layer 2 — scenarios + judge | subsystem | Held-out evaluation tier delivering P5 + P6 | RM Part 6 Phase 2; AC §7 | A45,A47,A50 | Anchored on Inspect AI |
| A09 | Layer 3 — observability + "why" | subsystem | Telemetry capture + override surfacing delivering P8 + observability | AC §7; RM P8 | A23,A24,A25 | OTel + LangFuse + CXDB |
| A10 | Layer 4 — self-healing loop | subsystem | Observability→anomaly→diagnosis→fix→ship without human (P11) | RM P11; AC §7 | A55,A56,A57,A58 | Largest custom engineering effort |
| A11 | Layer 5 — digital twins | subsystem | Behavioral clones of external dependencies (P7) | RM P7; AC §7 | A61,A62,A63 | Sparsest OSS coverage; LocalStack exemplar |
| A12 | Layer 6 — self-optimization | subsystem | System measures + improves own meta-performance (P12) | RM P12; AC §7 | A66,A70,A72 | Research-frontier; built last |
| A13 | Autonomy ladder (L0-L5) | subsystem | Five-Levels maturity scale: manual→intern→pair→HITL→PM-mode→dark | RM Part 3; AC §2 | — | v4 targets L4-L5 |

---

## Principles (control objectives realized by components)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A14 | P1 Specs as source of truth | cross-cutting | Code disposable; specs load-bearing artifact | RM P1; AC §1 | A30,A31,A32 | Recursive: applies to factory's own dev |
| A15 | P2 Three-layer architecture | cross-cutting | LLM client + agent loop + pipeline engine + persistence | RM P2; AC §1 | A03,A04,A05,A06 | Don't reinvent any of three |
| A16 | P3 Pipeline-file as process | cross-cutting | Workflow is version-controlled runner-agnostic DAG file | RM P3; AC §1 | A33,A34 | Methodology in file not prompts |
| A17 | P4 Deterministic-first | cross-cutting | Tool nodes for most steps; LLM only where reasoning needed | RM P4; AC §1 | A35,A36 | Primary guard over probabilistic |
| A18 | P5 Scenarios as held-out test set | cross-cutting | External, unread-by-agent, independently judged | RM P5; AC §1 | A45,A46,A47,A48 | Read-isolation enforced |
| A19 | P6 Satisfaction not test-pass | cross-cutting | Probabilistic metric over trajectory population | RM P6; AC §1 | A50,A51,A52,A53,A54 | LLM-as-judge, not boolean |
| A19b | P7 Digital twins | cross-cutting | Behavioral clones of critical external deps | RM P7; AC §1 | A11 | Most labor-intensive principle |
| A19c | P8 "Why am I doing this?" | cross-cutting | Manual overrides surface as new validation rules | RM P8; AC §1 | A38,A39,A40,A41,A42 | Override→pattern→rule pipeline |
| A19d | P9 Attribution | cross-cutting | Every commit/task/event carries actor identity | RM P9; AC §1 | A43,A44 | Gas City's strongest native match |
| A19e | P10 Memory layer | cross-cutting | Persistent dependency-aware task graph + trajectory store | RM P10; AC §1 | A20,A21 | Replaces flat scratchpads |
| A19f | P11 Self-healing loop | cross-cutting | Observability→anomaly→diagnosis→fix, no human | RM P11; AC §1 | A10 | Largest custom effort |
| A19g | P12 Self-optimization | cross-cutting | System improves own meta-performance over time | RM P12; AC §1 | A12 | The added 12th working principle |
| A19h | El Kaim 12th principle (deferred) | cross-cutting | "Pipeline files worth sharing" — community-norms release decision, not runtime component | RM Part 4 preamble; AC §1 | — | Replaced by P12 in working set |

---

## Components — Principle 1 (specs)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A30 | Spec format | component | The artifact that drives execution (Gas City prompt templates, Go text/template + Markdown) | RM P1 | A22,A28 | `agents/<name>/prompt.template.md` |
| A31 | Spec storage | data-store | Version-controlled, attributable spec store (Git + Gas City pack structure) | RM P1 | A22 | Packs are git-versioned |
| A32 | Spec linter (EARS) | component | EARS-style structural rules, INCOSE R7-R35; custom Go pack | RM P1; FM F18,F38 | A35 | Deterministic tool node |
| A32b | Spec → execution binding | interface | Maps which spec drives which work (formulas reference templates; sling routes) | RM P1 | A33,A09b | Native to Gas City |

## Components — Principle 3 (pipeline file)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A33 | Workflow format (formulas) | artifact | DAG specification as Gas City formulas (TOML) | RM P3; AC §3.2 #7 | A07 | Native |
| A34 | Workflow visualizer | component | Renders DAG for review (formula→DOT exporter + graphviz) | RM P3 | A37 | Gas City pack |
| A34b | Workflow linter (21-rule DOT) | component | Structural rules transfused from Mammoth's 21-rule DOT linter | RM P3; AC §6.4 | A37 | Mammoth MIT |
| A37 | Formula↔DOT bidirectional translator | interface | DOT ↔ formula interop for DOT-tool ecosystem | RM P3; RM Phase 1; AC §11.1 | A33 | ~few hundred LOC Go; Phase 1 |

## Components — Principle 4 (deterministic)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A35 | Tool node abstraction | component | Unified interface for deterministic steps (Gas City tool beads) | RM P4; AC §3.2 | A07 | Native |
| A36 | Reconciler / controller loop | control-loop | Desired-state convergence (Gas City Health Patrol) | RM P4; AC §3.2 #9 | A07 | Per-tick reconciler |
| A36b | Discipline tooling (LLM-where-tool linter) | component | Flags LLM nodes used where deterministic tool suffices | RM P4; FM F52 | A35 | Each guard must cite a falsifying scenario |

## Components — Principle 8 ("why")

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A38 | Manual override detection | component | Recognizes operator bypass (Claude Code Pre/PostToolUse hooks) | RM P8; AC §4.4 | A28 | Hook-registered |
| A39 | "Why" field prompting | component | Forces structured explanation of override | RM P8 | A38 | Hook handler |
| A40 | Override log storage | data-store | Durable record of overrides + why (Gas City beads type `override`) | RM P8; FM F10 | A20 | Native bead type |
| A41 | Periodic pattern surfacing | component | Reviews log for recurring overrides (SQL/duckdb pack) | RM P8 | A40 | Honeycomb BubbleUp transfusion |
| A42 | Rule conversion | workflow | Turns recurring overrides into validation rules (manual + new rubric) | RM P8 | A41,A51 | Operator workflow |

## Components — Principle 9 (attribution)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A43 | Identity model (actor schema) | component | Who/what can act: cities, rigs, agents | RM P9; AC §3.3 | A07 | Native |
| A44 | Action attribution (`created_by`) | component | Every action carries identity via beads/events | RM P9 | A20,A21 | Strongest principle match |
| A44b | Audit trail | data-store | Queryable history (event bus + bead history) | RM P9; FM F43 | A20,A21 | Native |
| A44c | Identity verification | component | Verify claimed actor matches actual (signature on bead provenance) | RM P9 | A44 | Optional/deferred |

## Components — Principle 10 (memory)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A20 | Beads / persistent task graph | data-store | Durable typed work-graph with dependencies (file or Dolt) | RM P10,P2; AC §3.2 #2 | — | Work ledger |
| A21 | CXDB trajectory store | data-store | Content-addressed trajectory store (Rust server + Go client + React UI) | RM P10; AC §5 | A26 | Apache 2.0; turn-model |
| A20b | Cross-session continuity | component | Resume after agent restart (Gas City session resume + Claude session-id) | RM P10 | A27,A04 | Native |
| A21b | Memory query interface | interface | Read patterns from memory (`gc bd` + CXDB HTTP API) | RM P10 | A20,A21 | Native + HTTP |

## Components — Principle 11 (self-healing)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A55 | Event substrate (Healer) | component | Records every action (Gas City event bus + CXDB) | RM P11 | A21,A29 | Native + bridge |
| A56 | Anomaly detection (numeric) | component | Detects unusual patterns (PyOD, Anomalib) | RM P11; AC §7 L4 | A55 | Python tool node |
| A56b | Trajectory embedding | component | Embeds trajectories for clustering (sentence-transformers) | RM P11 | A21 | Python tool node |
| A56c | Trajectory clustering | component | Groups similar failures (HDBSCAN, scikit-learn) | RM P11 | A56b | Python tool node |
| A57 | Diagnosis agent (Healer) | agent-role | LLM root-cause analysis; transfused from Tracker Diagnose/Audit/Doctor | RM P11; AC §6.4,§9.1 | A21,A56c | Strongest Layer-4 transfusion target |
| A58 | Fix-task generation | component | Diagnosis → bead of type `fix_task` | RM P11 | A57,A20 | Native bead writing |
| A58b | Loop closure tracking | component | Bead chain anomaly→diagnosis→fix→resolution; did fix work? | RM P11; FM F | A20,A58 | Bead schema |
| A59 | Durable workflow engine | component | Survives crashes/retries (Gas City Orders + Temporal/Inngest/Trigger.dev) | RM P11; AC §8 | A07 | Orders native; Temporal optional |

## Components — Principle 7 (twins)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A61 | HTTP record/replay | component | Capture and replay HTTP traffic (VCR.py, go-vcr, polly.js, HoverFly) | RM P7; AC §7 L5 | — | Per-language tool node |
| A62 | Stateful HTTP twin | component | Mock with custom logic (WireMock, Mountebank, Mockoon, LocalStack) | RM P7 | — | Per-twin `[[service]]` block |
| A62b | OpenAPI-driven mock | component | Mock generated from OpenAPI (Prism, Stoplight) | AC §7 L5 | — | Mature |
| A63 | Contract verification | component | Verify usage matches service promises (Pact, schemathesis, Dredd) | RM P7; AC §7 L5 | A62 | Gas City pack per service |
| A64 | Twin scaffolding from SDK | component | Generate twin from public SDK — no OSS, bespoke per service | RM P7; AC §7 L5 | A62 | LocalStack pattern transfusion |
| A64b | Behavioral fidelity testing | component | Diff twin vs real service behavior — DIY, no turnkey | AC §7 L5 | A64,A46 | Twin scenarios verify fidelity |

## Components — Principle 12 (self-optimization)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A65 | Meta-metric definition | component | What "better" means: cost-per-satisfaction, time-to-threshold, judge FP rate | RM P12; AC §12 | — | Values question; configuration |
| A66 | Meta-metric tracking | component | Records meta-metrics over time (MLflow, Aim, W&B) | RM P12; AC §7 L6,§8 | A65 | Gas City pack |
| A67 | Variant identification (prompt) | component | What to experiment with (DSPy compilers) | RM P12; AC §9.1 | — | Python tool node |
| A68 | Variant identification (hyperparameter) | component | Optimization over configuration (Optuna, Ray Tune) | RM P12 | — | Python tool node |
| A69 | A/B test routing | component | Routes traffic to variants (Unleash, GrowthBook, Flagsmith, OpenFeature) | RM P12; AC §7 L6 | — | Gas City pack |
| A70 | Counterfactual replay driver | component | Re-run from trajectory midpoint via CXDB O(1) branching | RM P12; AC §5.5,§12 | A21 | Driver is the key invention; no exemplar |
| A71 | Statistical comparison | component | Was variant better? (scipy.stats, statsmodels, Evidently AI) | RM P12; AC §7 L6 | A66 | Python tool node |
| A72 | Promotion gate | component | New variant becomes default via statistical gate (Gas City formula) | RM P12; AC §7 L6 | A71,A33 | Multi-metric mandatory (FM F47) |
| A72b | Experiment registry | data-store | Tracks experiments/runs (MLflow, W&B, DVC) | AC §7 L6 | A66 | Mature |
| A72c | Multi-armed bandit | component | Bandit variant routing (Vowpal Wabbit, MABWiser) | AC §7 L6,§9.1 | A69 | Mature narrow domain |
| A72d | Regression detection | component | Detect quality regression (Evidently AI, NannyML) | AC §7 L6 | A66 | ML-monitoring derived |

---

## Components — Layer 2 / 3 (scenarios, judge, observability)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A45 | Scenario authoring format | artifact | Defines a scenario's structure (Inspect AI Task DSL) | RM P5; AC §7 L2 | A50 | Alt: promptfoo, OpenAI Evals, DeepEval, AgentDojo |
| A46 | Scenario storage w/ read-isolation | data-store | Separate git repo + file perms + rig partition; agent can't read during work | RM P5; AC §13.3; FM F28 | A48b,A09b | OPA for finer control |
| A47 | Scenario runner | component | Executes scenarios against the system (Inspect AI runner) | RM P5; AC §7 L2 | A45 | Gas City pack |
| A48 | Holdout integrity audit | component | Detects isolation violation (log audit: agent reads vs scenario paths) | RM P5; FM F28 | A46 | Custom small |
| A48b | Scenario isolation policy (OPA) | component | OPA policy governing what implementer can read | AC §11.1,§13.3; FM F17 | A46 | Open question on scope |
| A50 | LLM-as-judge harness | component | Scores trajectories against scenarios (Inspect AI scorer, Ragas, DeepEval) | RM P6; AC §7 L2 | A45 | Gas City pack |
| A51 | Judge rubric management | artifact | Versioned criteria (Inspect AI objects, promptfoo YAML) | RM P6 | A50 | Native via pack |
| A52 | Multi-judge ensemble | component | Disagreement detection across judges | RM P6; FM F46 | A50 | Gas City formula |
| A53 | Satisfaction metric aggregation | component | Distribution over trajectory population (Inspect AI score reduction + Go aggregator) | RM P6; RM Phase 2 | A50 | Computes distributions from beads |
| A54 | Cross-family enforcement | component | Judge must be different model family than coder | RM P6; AC §12; FM F27 | A11b | Rule on model stylesheet |
| A48c | Independence auditor | component | Audits judge independence (gene transfusion D7-U-1) | FM F48 | A54 | Partial — shared training residual |
| A23 | LLM instrumentation | component | OpenLLMetry / OpenInference telemetry capture | AC §7 L3 | A24 | Apache 2.0 |
| A24 | OpenTelemetry Collector | component | Generic event collection receiving Claude Code OTLP | RM Phase 1; AC §4.3,§7 L3 | A28b | Apache 2.0 |
| A25 | LangFuse | data-store | LLM event storage + trace browsing + session + prompt versioning | RM Phase 1; AC §7 L3,§8 | A24 | Apache 2.0; replaces Phoenix |
| A24b | Trace browsing | component | Browse traces (LangFuse, Jaeger, Tempo) | AC §7 L3 | A25 | Mature |

---

## Gas City internals (the nine concepts + vocabulary primitives)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A22 | Pack | component | Distributable methodology bundle (TOML + tool node binaries + prompt templates) | AC §3.3; RM Part 5 | A07 | v4's sole extension surface; no Go fork |
| A27 | Session | component | Stable runtime backed by Provider (tmux/k8s/subprocess/exec) | AC §3.2 #1 | A07 | Vocabulary-free tmux runtime |
| A28 | Prompt templates | artifact | Go text/template markdown agent prompts | AC §3.2 #5 | A22 | Native to specs |
| A26 | Config (layered TOML) | artifact | Layered TOML; section presence = feature flag (`city.toml`, `pack.toml`) | AC §3.2 #4,§13 | A07 | Drives feature gating |
| A29 | Event Bus | data-store | Append-only JSONL with monotonic seq | AC §3.2 #3 | A07 | Lowest-impedance CXDB source |
| A09b | Sling / dispatch | component | Routes bead/wisp to agent or pool | AC §3.2 #8,§3.3 | A07 | Dispatch primitive |
| A22b | Molecule | artifact | Instantiated bead-tree from a formula | AC §3.2 #7,§3.3 | A33 | Runtime workflow instance |
| A22c | Order | workflow | Event-triggered workflow | AC §3.3; RM P11 | A29 | Subscribes to crashes/gates |
| A22d | Messaging (Mail + Nudge) | interface | Mail = durable; Nudge = ephemeral inter-agent messaging | AC §3.2 #6 | A27 | F32 injection risk |
| A22e | Health Patrol (Controller + Convergence) | control-loop | Per-tick reconciler; bounded convergence with gates | AC §3.2 #9 | A07 | Maps P4, partial P11, weak P8 |
| A22f | Convoy | workflow | Batched workflow | AC §3.3 | A33 | Vocabulary entry |
| A22g | Wait | interface | Gating / synchronization primitive | AC §3.3 | A33 | Vocabulary entry |
| A22h | Wisp | artifact | Unit of dispatchable work | AC §3.3 | A09b | Vocabulary entry |
| A22i | Rig | agent-role | Agent worker role with read/write partitions | AC §3.3,§13.3 | A27 | Partitioning enforces P5 isolation |
| A22j | City | component | Workspace | AC §3.3 | A07 | Vocabulary entry |
| A22k | Polecat | agent-role | Specific role in Gas Town pack (not in interface) | AC §3.3 | A22 | Pack-vocab only |
| A22l | Mayor | agent-role | Senior coordinator agent role (Gas Town pack vocab) | AC §3.3 | A22 | Pack-vocab only |
| A11b | Model stylesheet | artifact | CSS-like cost-aware model routing rules (transfusion from Fabro) | RM P6; AC §6.2 | A05 | Hosts cross-family + cost rules |

---

## Claude Code capabilities (agent loop surface)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A04b | Claude Code CLI (under Max) | component | Agent loop + LLM client via OAuth Max session; subprocess automation allowed | AC §4.1,§4.2 | — | $200/mo; no separate API key |
| A28b | Claude Code native OTLP telemetry | interface | Native OpenTelemetry export via env vars (metrics/events/traces) | AC §4.3 | A24 | gRPC :4317 / HTTP :4318 |
| A28c | Raw API bodies escape hatch | interface | `OTEL_LOG_RAW_API_BODIES=file:<dir>` dumps untruncated conversation JSON | RM Phase 1; AC §4.3,§5.4 | A28b | Ideal CXDB ingestion source |
| A28d | Claude Code Skills | component | `.claude/skills/` multi-step workflow definitions | AC §4.4 | A04b | Under Max |
| A28e | Claude Code Subagents | agent-role | Parallel work agents (Explore, Plan, general-purpose, custom) | AC §4.4 | A04b | Under Max |
| A28f | Claude Code Hooks | interface | Pre/PostToolUse, SessionStart, Stop deterministic gates | AC §4.4; RM P8 | A04b | Powers override detection |
| A28g | MCP servers | interface | Tool layer for Claude Code | AC §4.4 | A04b | Tool integration |
| A28h | Claude Agent SDK (Max credit) | component | June 15 2026 monthly SDK credit, OAuth from Claude Code login | AC §4.2 | A04b | Pre-June: subprocess path |

---

## CXDB internals (trajectory store detail)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A21c | Turn model | artifact | Unit = turn (not span/event), parent-turn pointer forms DAG | AC §5.3 | A21 | Designed against OTel span trees |
| A21d | Blob CAS (BLAKE3) | component | Content-addressed payloads via BLAKE3 of msgpack bytes | AC §5.3,§5.5 | A21 | Free dedup + tamper-evidence (F11) |
| A21e | O(1) trajectory branching | component | Fork from any point = new head pointer, no history copy | AC §5.3,§5.5 | A21 | Enables counterfactual replay |
| A21f | CXDB type registry | data-store | Dynamic `{bundle_id,type,version}` type system with JSON bundles | AC §5.3; FM F50 | A21 | Viewpoint tagging resolves F50 |
| A21g | CXDB binary ingest (msgpack :9009) | interface | High-throughput writer via Go client library | AC §5.2 | A21 | Port 9009 |
| A21h | CXDB HTTP/JSON API (:9010) | interface | REST for browsers/dashboards/ad-hoc queries | AC §5.2 | A21 | Port 9010 |
| A21i | CXDB storage layout | data-store | `turns.log`, `blobs.pack`, `registry/` — no Postgres/Redis/Kafka | AC §5.3 | A21 | Self-contained files |

---

## Interfaces / bridges / integrations

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A29b | Raw-bodies → CXDB bridge | interface | Standalone Go tool-node binary watching raw-bodies dir, posts to CXDB HTTP | RM Phase 1; AC §5.4,§11.1 | A28c,A21h | Lowest-impedance recommended path; transfused from `internal/sessionlog` |
| A29c | Gas City event-bus → CXDB path | interface | Alternative bridge: JSONL events already attributed/trajectory-shaped | AC §5.4 | A29,A21 | Lowest impedance option (ranked) |
| A29d | OTLP → CXDB path (rejected) | interface | Span-tree→turn-DAG mapping CXDB was designed against | AC §5.4,§11.3 | A28b | Highest impedance; rejected |
| A37b | `gc formula export --format dot` | interface | CLI graphviz rendering of a formula | RM Phase 1 | A37 | Phase 1 |
| A28i | Inspect AI subprocess tool node | interface | Gas City `[[tool]] type="subprocess"` invoking `inspect eval` | AC §13.3 | A47,A35 | Scenario provider wrap |
| A28j | Inspect AI `[[service]]` provider block | interface | Gas City service block exposing Inspect AI as scenario provider | RM Phase 2 | A47 | `type = "inspect_ai"` |
| A28k | HMAC signing layer (mail) | interface | Optional signed inter-agent coordination | FM F32 | A22d,A44c | Gene transfusion: signed-message protocol |

---

## Pipeline stages / workflows / phases

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A80 | Phase 0 — Gas City foundation | pipeline-stage | Minimum viable principled runtime, one Claude session, no custom code | RM Part 6; AC §3.4 | A07,A04b,A26 | Delivers P1,P2,P3(basic),P4,P9,P10 |
| A81 | Phase 1 — Verbatim OSS adoption | pipeline-stage | Add ready-to-use OSS: formulas, OTel, LangFuse, CXDB, bridges, translator | RM Part 6; AC §0 | A80,A37,A24,A25,A21,A29b | Configure not invent |
| A82 | Phase 2 — Layer 2 + bootstrap validation | pipeline-stage | Ship P5+P6 via Inspect AI, then prove factory can build for itself | RM Part 6; AC §11.1 | A81,A08 | Critical milestone |
| A83 | Phase 3+ — Factory builds factory | pipeline-stage | Each remaining principle's components built by the factory itself | RM Part 6; AC §11.1 | A82 | Gene transfusion + design review per piece |
| A83a | Phase 3a — P8 "why" discipline | pipeline-stage | Factory builds override-detection hooks + surfacing pack | RM Phase 3a | A83,A38 | CloudTrail/reflog transfusion |
| A83b | Phase 3b — P11 Healer in pieces | pipeline-stage | Anomaly→cluster→diagnosis→fix→loop-closure, each separate build | RM Phase 3b | A83,A56,A57 | Build simplest first |
| A83c | Phase 3c — P7 twins per service | pipeline-stage | Factory builds twin per critical dependency, LocalStack-shaped | RM Phase 3c | A83,A64 | Bounded per-service engineering |
| A83d | Phase 3d — P12 self-optimization | pipeline-stage | Factory builds meta-metric/variant/AB/replay packs, heaviest review | RM Phase 3d | A83,A65,A70 | Highest-risk move |
| A84 | Self-bootstrap mechanic | workflow | Factory→spec→run→human review→deploy→extends-factory recursion | RM Part 7; AC §11.1 | A82 | The recursion |
| A85 | Bootstrap validation milestone | workflow | Author spec for small new component, run factory, review, deploy | RM Phase 2; AC §11.1 | A82,A84 | Pass/fail gate for whole approach |
| A86 | Gene transfusion technique | workflow | Port a working pattern from a concrete exemplar instead of inventing | RM Part 7; AC §9 | — | Every factory-built component transfuses ≥1 exemplar |
| A87 | Design review before deployment | workflow | Human reviews factory design output before production use | RM Part 7 | A84 | Required until P12 trusted |
| A88 | Methodology-as-config experiment | workflow | Run v3 candidates (e.g. GF-M) as pipeline files on the runtime | RM Part 1,8; AC §0 | A08,A33 | Empirical methodology selection |

---

## Artifacts (data / record types)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A90 | `override` bead | artifact | Durable record of operator override + why | RM P8 | A20 | Bead type |
| A91 | `fix_task` bead | artifact | Diagnosis output written as a fix task | RM P11 | A20 | Bead type |
| A92 | `factory_build_in_progress` bead | artifact | In-progress factory-built component marker | AC §16 | A20 | `gc bd find --type` |
| A93 | `transfused_from` metadata | artifact | Records external exemplar URL per factory-built component | RM Part 7; AC §9.2 | A86 | P9 applied to factory's own work |
| A94 | Definition-of-Done (DoD) | artifact | Acceptance-criteria checkbox set driving build loops | OS Part 1 (Kilroy, Fabro, attractor-c) | A45 | DoD-loop spec pattern |
| A95 | One-shot spec | artifact | Markdown/DOT file describing target system an agent builds in one shot | OS Part 1 | A30 | Attractor/Kilroy/Fabro examples |
| A96 | DOT workflow graph | artifact | `.dot` pipeline graph driving a build | OS Part 1 | A37 | Kilroy/attractor-c/pi-dev examples |
| A97 | Intent Crucible 9-field intake | artifact | Structured intent intake (gene transfusion from GF-C) | FM F41 | A86 | Addresses under-defined-intent debt |
| A98 | Signed/cryptographic scenarios | artifact | Day-0 cryptographically signed held-out scenarios | FM F9,F7,F55 | A46 | Anti-overfitting external truth |

---

## Cross-cutting concerns

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A100 | License hygiene | cross-cutting | Compound dependency set must be license-compatible (MIT/Apache/BSD dominate) | RM Part 5; AC §10 | — | Phoenix Elastic avoided; Tracker verify |
| A101 | Gas City `internal/` path constraint | cross-cutting | Go library import blocked; irrelevant since v4 extends via packs | RM Part 5,8; AC §3.5,§10 | A22 | No fork needed |
| A102 | Gas City migration tail | cross-cutting | Two CI-enforced migrations (worker boundary, session-first); 1-2 breaks/qtr | RM Part 8; AC §3.5,§14 | A07 | Pin version |
| A103 | Vocabulary lock-in | cross-cutting | Cities/rigs/formulas/molecules cognitive load; front-loaded, recoverable | RM Part 8; AC §3.3 | A22 | Glossary mitigation |
| A104 | Cross-family judge policy | cross-cutting | Judge model family must differ from coder family | RM P6; FM F27,F46 | A54 | Anti-circularity |
| A105 | Read-isolation / holdout integrity | cross-cutting | Agent must not read scenarios during work | RM P5; FM F28 | A46,A48 | Filesystem + OPA + discipline |
| A106 | Model-floor declaration | cross-cutting | Claude Code declared as the explicit capability floor | FM F19,F31 | A04b | Single-adapter floor |
| A107 | External grounding discipline | cross-cutting | Foundations stay upstream OSS; factory builds only orchestration glue | RM Part 7 | A86 | Reduces drift |
| A108 | Pack governance / derivation-rule check | cross-cutting | Pack adoption must pass derivation check (anti-Federation-drift) | FM F35; RM | A22 | Phase 1 component recommendation |
| A109 | Operator throughput constraint | cross-cutting | Factory may consume specs faster than operator can author (design starvation) | FM F25 | A84 | Honestly documented, unsolved |

---

## Failure modes (61-mode catalog, v4 treatment)

> Source for all: FM (F-MODE-COVERAGE.md), cross-referencing `architectures/v3/failure-modes-v3.md`. Status in Notes: Addressed / Partial / Gap / Caution.

| ID | Name | Kind | Mitigating mechanism | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A110 | F1 Hallucination Loop | failure-mode | Cross-family judge + held-out scenarios | FM §1 | A54,A46 | Addressed |
| A111 | F2 Reward hacking | failure-mode | Probabilistic satisfaction over population | FM §1 | A53 | Addressed |
| A112 | F3 Spec-completeness fallacy | failure-mode | Twins + scenarios partially compensate | FM §9 | A11,A46 | Gap (inherent) |
| A113 | F4 Code-quality teardown | failure-mode | Anomaly detection on quality metrics; Healer | FM §3 | A56,A57 | Partial |
| A114 | F5 Cognitive ceiling | failure-mode | L4-L5 batching (out-of-loop) | FM §9 | A13 | Gap (operator-side) |
| A115 | F6 Cognitive debt | failure-mode | Accepted cost of L4-L5 delegation | FM §9 | A13 | Gap (operator-side) |
| A116 | F7 Normalization of deviance | failure-mode | Healer baselines against signed scenarios | FM §3 | A57,A98 | Addressed |
| A117 | F8 Stale-knowledge inversion | failure-mode | Healer freshness anomaly + curation pack | FM §7 | A56 | Addressed (Phase 3+) |
| A118 | F9 Spec overfitting | failure-mode | Cryptographically signed day-0 scenarios | FM §1 | A98 | Addressed |
| A119 | F10 Findings disappear into chat | failure-mode | Override log + CXDB trajectory store | FM §2 | A40,A21 | Addressed |
| A120 | F11 Renumbering breaks references | failure-mode | CXDB BLAKE3 content-addressing | FM §6 | A21d | Addressed (strongest) |
| A121 | F12 Lethal trifecta | failure-mode | Twins + boundary typing (CaMeL) | FM §4 | A11,A17 | Addressed |
| A122 | F13 Missing-config blindspot | failure-mode | Twins exercise environment (partial) | FM §9 | A11 | Gap (residual) |
| A123 | F14 Attribution collapse | failure-mode | P9 native attribution | FM §2 | A44 | Addressed (strongest match) |
| A124 | F16 Resume-fidelity decay | failure-mode | CXDB replay + session resume | FM §2 | A21,A20b | Partial (KV cache loss) |
| A125 | F17 Parallel agents lose data | failure-mode | Worktree isolation + OPA on partitions | FM §7 | A48b | Addressed |
| A126 | F18 Prose specs lack rigor | failure-mode | EARS linter + satisfaction-not-test-pass | FM §1 | A32,A19 | Partial |
| A127 | F19 Model-floor dependency | failure-mode | Claude Code declared as floor | FM §6 | A106 | Addressed (by declaration) |
| A128 | F20 Maintenance vs greenfield asymmetry | failure-mode | No mandate picked; methodology-level | FM §9 | A88 | Gap (intentional scope) |
| A129 | F21 Context-window exhaustion | failure-mode | Observability detects; doesn't prevent | FM §9 | A09 | Gap (methodology-level) |
| A130 | F22 Zombie agents | failure-mode | PyOD session-liveness anomaly + diagnosis | FM §3 | A56,A57 | Addressed |
| A131 | F23 Stalled-vs-thinking ambiguity | failure-mode | Tracker Diagnose/Audit/Doctor transfusion | FM §3 | A57 | Addressed |
| A132 | F24 Trust creep | failure-mode | Healer monitors gate-relaxation patterns | FM §3 | A57 | Addressed |
| A133 | F25 Design starvation | failure-mode | Honest staffing; unsolved by construction | FM §8 | A109 | Caution |
| A134 | F26 Telephone / inter-agent chain | failure-mode | Pipeline-file controls handoff; lintable | FM §6 | A16,A34b | Addressed |
| A135 | F27 Circularity same-model | failure-mode | Cross-family enforcement at judge nodes | FM §1 | A54 | Addressed |
| A136 | F28 Holdout leakage | failure-mode | Read-isolation: perms + OPA + rig partition | FM §1 | A46,A105 | Addressed |
| A137 | F29 Talent pipeline depletion | failure-mode | Systemic; documented constraint | FM §9 | — | Gap (systemic) |
| A138 | F30 Liability vacuum | failure-mode | Regulatory; pack declares regime | FM §9 | — | Gap (systemic) |
| A139 | F31 Substrate floor = weakest adapter | failure-mode | Single Claude Code adapter defines floor | FM §6 | A106 | Addressed (strongest) |
| A140 | F32 Mail-injection / unsigned coordination | failure-mode | P9 attribution + optional HMAC signing | FM §2,§7 | A44,A28k | Addressed |
| A141 | F33 Adversarial-prompt defeat of judge | failure-mode | Deterministic boundary typing primary; twins | FM §4 | A17,A11 | Addressed |
| A142 | F34 Cross-layer drift | failure-mode | Drift detector pack (U-B transfusion) | FM §7 | A86 | Partial |
| A143 | F35 Federation-as-Family Drift | failure-mode | Pack-derivation-rule check at adoption | FM §7,§8 | A108 | Partial / Caution |
| A144 | F36 Instruction-following ceiling | failure-mode | Spec-chunking (small focused specs) | FM §9 | A14 | Gap (inherent model limit) |
| A145 | F37 Silent contradictory-prompt collapse | failure-mode | Multi-model paraphrase divergence (GF-M) | FM §1 | A52 | Partial |
| A146 | F38 Vocabulary lint debt | failure-mode | EARS spec linter, deterministically detectable | FM §6 | A32 | Addressed |
| A147 | F39 Point-spec / region-mismatch | failure-mode | Inspect AI region scoring over trajectory region | FM §7 | A53 | Addressed |
| A148 | F40 Last-mile drift | failure-mode | Healer monitors shipping rate vs start rate | FM §3 | A57 | Partial |
| A149 | F41 Under-defined-intent debt | failure-mode | Intent Crucible 9-field intake (GF-C) | FM §7 | A97 | Addressed |
| A150 | F42 Cognitive-Escrow Negligence | failure-mode | Layer 3 observability + re-engagement surface | FM §2 | A09 | Partial |
| A151 | F43 RSI Board-Visibility Gap | failure-mode | P9 attribution + audit trail; pack declares RSI | FM §6 | A44b | Partial |
| A152 | F44 Lethal-Trifecta Production-Scissors Default | failure-mode | Substrate default twins; production requires explicit declaration | FM §4 | A11 | Addressed |
| A153 | F45 Language-as-Harness Mismatch | failure-mode | Go strongly typed; Python sections bounded | FM §7 | — | Partial |
| A154 | F46 Single-model review blindspot | failure-mode | Cross-family judge ensemble | FM §1 | A52,A54 | Addressed |
| A155 | F47 Visible-metric drift / Goodhart | failure-mode | Multi-metric simultaneous, no single target | FM §5,§8 | A72 | Partial / Caution |
| A156 | F48 Tacit collusion via shared context | failure-mode | Cross-family judge + independence auditor | FM §1 | A48c | Partial |
| A157 | F49 Discussion-as-Amplification | failure-mode | Substrate-level controls substitute for prompts | FM §9 | A17 | Gap (inherent) |
| A158 | F50 Architecture/spec confusion in typed objects | failure-mode | CXDB type registry viewpoint tagging | FM §2 | A21f | Addressed (strongest) |
| A159 | F51 Ashby-deficient probabilistic guard | failure-mode | Deterministic boundary typing primary guard | FM §6 | A17 | Addressed |
| A160 | F52 Tempting-Wrong-Hybrid | failure-mode | Every guard must cite a falsifying scenario | FM §8 | A36b | Caution (worsen risk) |
| A161 | F53 Voluntary-discipline fragility | failure-mode | Substrate-triggered structural controls (hooks, formula checks) | FM §6 | A28f,A22e | Addressed (strongest) |
| A162 | F54 Goal subversion (RSI prompt-injection) | failure-mode | CXDB history + Healer objective-shift anomaly | FM §7 | A21d,A56 | Partial (weakest) |
| A163 | F55 Behavioural drift / self-reference loop | failure-mode | Signed scenarios + twins as external truth | FM §6 | A98,A11 | Partial |
| A164 | F56 Guardrail-bypass under stress (Replit-class) | failure-mode | Twins isolate agent from production; bounded blast radius | FM §4 | A11 | Addressed |
| A165 | F57 Design-authority erosion | failure-mode | Healer monitors classification-threshold drift | FM §3 | A57 | Partial (values question) |
| A166 | F58 Runtime/design-time compliance split | failure-mode | Continuous observability + meta-metric runtime evidence | FM §7 | A09,A66 | Partial |
| A167 | F59 Premature decomposition | failure-mode | Runtime supports either flow; pack authors choose | FM §9 | A88 | Gap (methodology-level) |
| A168 | F60 Parallel-cycle compounding error | failure-mode | Aggregate-rate meta-metric (1−(1−p)ⁿ); A/B reports aggregate | FM §5 | A66,A69 | Addressed |
| A169 | F61 Context fragmentation across agents | failure-mode | Shared CXDB trajectory store; bead-query reads | FM §6 | A21,A21b | Partial |

---

## External exemplars / transfusion sources (named upstream systems)

| ID | Name | Kind | One-line description | Source | Depends on | Notes |
|---|---|---|---|---|---|---|
| A180 | Tracker (Mammoth's library) | component | Programmatic Diagnose/Audit/Doctor failure-report APIs | AC §6.4,§9.1; RM | A57 | Strongest Layer-4 transfusion target; license verify |
| A181 | Mammoth (2389) | component | DOT-runner frontend; 21-rule DOT linter; Bubble Tea TUI | AC §6.4; RM | A34b | Linter transfusion target |
| A182 | Kilroy (Shapiro) | component | CXDB-backed run history, commit-per-node, worktree-per-run | AC §6.3; OS | A21 | CXDB-integration transfusion target |
| A183 | Fabro (Helmkamp/Qlty) | component | React operator surface + CSS model stylesheet cost routing | AC §6.2; OS | A11b | Model-stylesheet transfusion target |
| A184 | OpenHands (All-Hands) | component | Layer 2 SWE-Bench/GAIA benchmark harness in sibling repo | AC §6.1; OS | A45 | Layer-2 scenario/judge transfusion |
| A185 | LocalStack | component | AWS service emulator; strongest Layer-5 twin exemplar | RM P7; AC §7 L5 | A64 | Per-service twin pattern |
| A186 | StrongDM Attractor | component | Original three-spec dark-factory (workflow / agent-loop / unified-LLM) | OS Part 1 | A95 | DOT-digraph execution model origin |
| A187 | El Kaim Dark Factory synthesis | artifact | Source of the original 11 principles | AC §1; RM Part 4 | A14 | `reference-only/.../dark-factory-article.txt` |
| A188 | v3 methodology candidate catalog | artifact | Ten v3 candidates re-cast as pipeline configs to run on v4 runtime | RM Part 1,2,8; AC §16 | A88 | GF-M is cheapest first experiment |
| A189 | Warren (Overstory successor) | component | Possible future fleet-shape multi-agent runner; status unverified | AC §11.2 | — | Deferred decision |
| A190 | Spec-attribute research corpus | artifact | Papers on how spec completeness/ambiguity/specificity affect AI success | OS Part 2 | A95 | HumanEvalComm, Ambig-SWE, ArchCode, PRDBench, etc. |
