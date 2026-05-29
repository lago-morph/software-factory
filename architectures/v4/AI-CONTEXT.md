# V4 architecture — dense AI session capture

Dense AI-readable artifact capturing decisions, alternatives, tradeoffs, and accumulated context from the session that produced v4. Companion to `README.md` (human-facing approach doc). Designed for an AI agent picking up v4 cold.

**Session date**: 2026-05-29
**Conversation owner**: jonathan@manton.com
**Primary outputs**: this file + `README.md`

---

## 0. Pivot summary

| Layer | v3 frame | v4 frame |
|---|---|---|
| Decision unit | Methodology candidate | Component-per-principle |
| Primary deliverable | Lean-eval for chosen candidate | Principle-bound runtime |
| Methodologies | Compete for selection | Become pipeline files on the runtime |
| Substrate | Methodology-specific | Convergent across methodologies |
| Risk on misfit | High (rewrites substrate) | Low (rewrites pipeline file) |

**Trigger for pivot**: user observation that the v3 README primer missed continuous-improvement / closed-loop refinement. Investigation showed: methodologies are second-order; runtime is first-order; build runtime, methodology becomes empirical.

---

## 1. The 12 working principles

10 of 11 originally from El Kaim "Dark Factory" synthesis (`reference-only/f675af7d98/dark-factory-article.txt`). Principle 12 in the original ("pipeline files worth sharing") is community-norms, deferred. Self-optimization added as the 12th working principle.

| # | Name | One-line definition |
|---|---|---|
| 1 | Specs as source of truth | Code is disposable; specs are load-bearing |
| 2 | Three-layer architecture | LLM client + agent loop + pipeline engine + persistence |
| 3 | Pipeline-file as process | Workflow is a DAG file, version-controlled, runner-agnostic |
| 4 | Deterministic-first | Tool nodes for most steps; LLM only where reasoning required |
| 5 | Scenarios as held-out test set | External, unread-by-agent, independently judged |
| 6 | Satisfaction not test-pass | Probabilistic over trajectory population |
| 7 | Digital twins | Behavioral clones of critical external dependencies |
| 8 | "Why am I doing this?" | Manual overrides surface as new validation rules |
| 9 | Attribution | Every event carries actor identity |
| 10 | Memory layer | Persistent dependency-aware task graph + trajectory store |
| 11 | Self-healing loop | Observability → anomaly → diagnosis → fix, no human |
| 12 | Self-optimization | System measures its own meta-performance and improves |

---

## 2. Convergent architectural shape (recap from corpus)

Three-layer + persistence:
1. **LLM client** — provider abstraction (LiteLLM, or Claude Code under Max)
2. **Agent loop** — multi-turn reasoning + tool dispatch (Claude Code, OpenHands, Overstory, Codex)
3. **Pipeline engine** — DOT-graph workflow runner (Gas City, Kilroy, Mammoth, Fabro, Smasher, Tracker)
4. **Persistence** — event store (CXDB) + work ledger (Beads)

Source: corpus convergence finding; every public dark-factory implementation lands here.

Five-Levels autonomy ladder: L0 manual → L1 intern → L2 pair → L3 HITL (the trap) → L4 PM mode → L5 dark. v4 targets L4-L5.

---

## 3. Gas City — load-bearing third-party dependency

### 3.1 Coverage map (smallest viable install vs 12 principles)

| Principle | Coverage from minimum Gas City install |
|---|---|
| 1 | Strong (prompt templates + config + version control) |
| 2 | Strong (session provider, templates, beads) |
| 3 | Strong when `[formulas]` enabled (TOML DAGs) |
| 4 | Strong (reconciler + tool nodes) |
| 5 | None — convention only; user provides enforcement |
| 6 | None — convergence gate slot exists but no judge |
| 7 | None |
| 8 | Weak (convergence gates partially impose; mostly user discipline) |
| 9 | **Strongest match in entire corpus** — automatic everywhere |
| 10 | Strong (bead store, file or Dolt) |
| 11 | Mechanism present (Orders subscribing to crashes/gates); no Healer agent shipped |
| 12 | None |

### 3.2 Gas City's "nine concepts"

5 primitives + 4 derived mechanisms:

| # | Concept | Definition | Principles |
|---|---|---|---|
| 1 | Session | Stable runtime backed by Provider (tmux/k8s/subprocess/exec) | P2, P9 |
| 2 | Bead Store | Durable typed work-graph (Dolt or file) | P1, P5, P9, P10 |
| 3 | Event Bus | Append-only JSONL with monotonic seq | P9, P10, P11 |
| 4 | Config | Layered TOML; section presence = feature flag | P1, P3, P12 |
| 5 | Prompt Templates | Go `text/template` markdown | P1, P2, P12 |
| 6 | Messaging (Mail + Nudge) | Mail = durable; Nudge = ephemeral | P9, P10 |
| 7 | Formulas + Molecules | Formula = TOML DAG template; Molecule = instantiated bead-tree | P1, P3, P4, P12 |
| 8 | Dispatch (Sling) | Routes bead/wisp to agent or pool | P2, P3 |
| 9 | Health Patrol (Controller + Convergence) | Per-tick reconciler; bounded convergence with gates | P4, P11 (partial), P8 (weak) |

### 3.3 Gas City vocabulary translation table

| Gas City term | Generic equivalent |
|---|---|
| city | workspace |
| rig | agent worker role |
| formula | pipeline file / workflow DAG template |
| molecule | instantiated workflow / bead-tree |
| pack | distributable methodology bundle |
| convoy | batched workflow |
| sling | dispatch / route |
| wait | gating / synchronization primitive |
| polecat | (specific role in Gas Town pack; not in interface) |
| wisp | unit of dispatchable work |
| order | event-triggered workflow |
| Mayor | senior coordinator agent role (Gas Town pack vocab) |

Vocabulary is real cognitive cost but front-loaded and recoverable.

### 3.4 Smallest viable install (Phase 0 exactly)

- `gc` binary (single Go)
- `pack.toml` declaring `[imports.core]`
- `city.toml` with `[workspace]`, one `[[agent]] provider = "claude"`, `[beads] provider = "file"`
- One `agents/<name>/prompt.template.md`
- ~30 lines TOML + one template = full minimum

**Explicitly off**: `[daemon]`, `[mail]`, `[formulas]`, `[rigs]`, Dolt server, `[[service]]` blocks, orders.

### 3.5 Migration tail risk

- Two CI-enforced migrations in flight (worker boundary, session-first)
- Expect 1-2 breaking pack-schema or formula-format changes per quarter through 2026
- `internal/` paths in Go — GitHub blocks direct library import. **Only matters for Go library use.** v4 extends Gas City via packs (TOML + tool node binaries + prompt templates) — no Go imports needed, no fork required for the v4 extension model.
- `pkg/` exposure unlikely until both migrations settle — does not block v4's pack-based work

### 3.6 Extractability findings (research subagent verified)

The tmux runtime is deliberately vocabulary-free. `runtime.Provider` interface (~18 methods) imports only stdlib + 4 internal packages: `internal/runtime`, `internal/sessionlog`, `internal/shellquote`, `internal/overlay`. Extraction surface is ~20 Go files. `runtimetest/conformance.go` contract suite travels with it.

**Recommendation tested**: full Gas City adoption (smallest install) beats tmux-only extraction for the v4 goal because Gas City provides P1, P2, P3, P4, P9, P10 native vs. building Layer 1 from scratch.

---

## 4. Claude Code under Max — capabilities and constraints

### 4.1 Authentication

- Claude Max subscription: $200/month
- No separate API key issued
- Claude Code CLI authenticates via OAuth tied to Max session
- Subprocess automation of `claude` CLI is officially supported
- Anthropic does NOT permit OAuth tokens to be used outside Claude Code/claude.ai

### 4.2 Claude Agent SDK availability under Max

- **June 15, 2026**: Max plan holders get monthly Agent SDK credit (~$200 equivalent)
- SDK authenticates via OAuth, picks up credentials from Claude Code login
- Before June 15: subagents + Claude Code CLI subprocess automation is the Max-supported path
- Source: `code.claude.com/docs/en/agent-sdk/overview`, `support.claude.com/en/articles/15036540`

### 4.3 Claude Code telemetry surface

Native OpenTelemetry support, configurable via env vars. Works under Max with no API key.

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Three OTLP protocols**: gRPC (default :4317), HTTP/JSON (:4318), HTTP/protobuf (:4318).

**Configurable**: headers, mTLS (`OTEL_EXPORTER_OTLP_CLIENT_KEY` / `_CERTIFICATE` for gRPC, `CLAUDE_CODE_CLIENT_CERT` / `_KEY` for HTTP), per-signal endpoints.

**Emitted**:
- Metrics: session count, lines of code, PRs, commits, costs, token usage, edit decisions, active time
- Events/logs: user prompts, tool results, API requests/errors, tool decisions, permission changes, auth, MCP connections, plugins, skills
- Traces (beta — `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`): distributed tracing across user prompts → API calls → tool executions

**Special escape hatch**: `OTEL_LOG_RAW_API_BODIES=file:<dir>` dumps untruncated request/response JSON to disk. Conversation-shaped, ideal for CXDB ingestion.

**Correlation attributes**: `prompt.id`, `session.id`, `user.account_uuid`, `organization.id`, `terminal.type`.

**Export intervals**: metrics 60s default (`OTEL_METRIC_EXPORT_INTERVAL`), logs 5s default (`OTEL_LOGS_EXPORT_INTERVAL`).

### 4.4 Claude Code skills + subagents + hooks

Under Max:
- **Skills** in `.claude/skills/` — multi-step workflow definitions
- **Subagents** for parallel work (Explore, Plan, general-purpose, custom)
- **Hooks** (PreToolUse, PostToolUse, SessionStart, Stop) — deterministic gates around tool calls
- **MCP servers** — tool layer

These together cover much of what a small pipeline runner does, all under Max budget.

---

## 5. CXDB — content-addressed trajectory store

### 5.1 Project metadata

- **Repo**: `github.com/strongdm/cxdb`
- **License**: Apache 2.0
- **Composition**: Rust server (~16k LOC) + Go client library (~9.5k LOC) + React/TS frontend (~6.7k LOC) + type registry + k8s manifests
- **Released**: February 2026 alongside StrongDM Software Factory unveil
- **Maintenance**: 3-person team; load-bearing for StrongDM's Healer pattern internally

### 5.2 Ingestion API

Two protocols:
- **Binary**: msgpack on port 9009 (high-throughput writer; Go client library)
- **HTTP/JSON**: REST on port 9010 (browsers, dashboards, ad-hoc queries)

**Critical**: **no native OTLP receiver**. StrongDM explicitly positions CXDB *against* OTel: "Built for distributed tracing. Spans model request trees, not conversations."

### 5.3 Event schema (the "turn" model)

- Unit = **turn**, not span/event
- Each turn has a parent turn pointer (DAG, not tree)
- Branching from any point = O(1) fork (just a new head pointer; no history copy)
- Payloads content-addressed via BLAKE3 of msgpack-serialized bytes ("Blob CAS")
- Dynamic type system: `{bundle_id, type, version}` per payload
- Type registry: JSON bundles like `mycompany.agents.v1` with `mycompany:DeployEvent` schemas
- Storage layout: `turns.log`, `blobs.pack`, `registry/` — no Postgres/Redis/Kafka

### 5.4 Bridges to CXDB from Claude Code / Gas City

Three options, ranked by impedance (lower = better):

| Path | Impedance | Why |
|---|---|---|
| Gas City event bus JSONL → CXDB | **Lowest** | Events already attributed and trajectory-shaped |
| Claude Code raw API bodies → CXDB | Low | Conversation-shaped already; parent-chain via `session.id` |
| Claude Code OTLP → CXDB | **Highest** | Span tree → turn DAG mapping is what CXDB was designed against |

**Recommended**: raw API bodies path. The bridge is a small standalone Go binary that watches `OTEL_LOG_RAW_API_BODIES` directory and posts to CXDB HTTP API. Pattern is transfused from Gas City's `internal/sessionlog` (which parses Claude Code JSONL) — but the bridge is a standalone tool-node binary in a pack, not a Go import of Gas City code.

### 5.5 What CXDB adds over plain JSONL

- BLAKE3 content-addressing → free dedup (long repeated payloads stored once), tamper-evidence
- O(1) trajectory branching → counterfactual replay essential for self-healing investigations and self-optimization variant tests
- Type-aware projection → not just raw JSON dumps; UI can render typed payloads structurally
- Performance contract: p50 <1ms append for 10KB payloads, sub-ms retrieval over TB-scale
- Query interface: HTTP/JSON REST instead of grep over log files

---

## 6. Integrated pipeline-runner survey (Layer 2-6 coverage)

Research subagent verified findings:

### 6.1 OpenHands (All-Hands AI)

- Repo: `github.com/All-Hands-AI/OpenHands`
- License: MIT
- **Strong**: Layer 2 (sibling repo `OpenHands/benchmarks` with SWE-Bench 77.6%, GAIA, ToM-SWE), Layer 3 (V0/V1 event store, React SPA, Cloud GUI, k8s GUI)
- **None**: Layers 4 (self-healing), 5 (twins), 6 (self-optimization beyond cost tracking)
- **Strongest v4 transfusion target**: Layer 2 scenario authoring + judge harness patterns from `benchmarks/` repo

### 6.2 Fabro (Bryan Helmkamp / Qlty.sh)

- Repo: `github.com/fabro-sh/fabro` (Rust)
- License: verify; likely MIT
- **Strong**: Layer 3 operator surface (React UI, REST + SSE, Daytona sandboxes, SLSA-attested releases), Layer 6 cost-aware routing (CSS-like model stylesheet)
- **None**: Layer 2 (no scenario DSL), Layer 4 (intra-DAG retry only, not closed-loop diagnosis), Layer 5
- **Strongest v4 transfusion target**: CSS model stylesheet pattern for cost-aware routing

### 6.3 Kilroy (Daniel Shapiro)

- Repo: per Shapiro's references; Go
- License: verify; likely MIT
- **Strong**: Layer 3 recording (CXDB-backed run history, commit-per-node, worktree-per-run, multi-mode resume), Layer 6 cost routing (model stylesheet + `--force-model` + `modeldb`)
- **None**: Layers 2, 4 (basic resume only), 5
- **Strongest v4 transfusion target**: CXDB integration pattern (per-stage `prompt.md` / `response.md` / `events.ndjson` / etc.)

### 6.4 Mammoth (2389 Research)

- Repo: `github.com/2389-research/mammoth`
- License: verify; 2389 convention is MIT
- **Strong**: Layer 3 (delegates to Tracker — `activity.jsonl`, `tracker.NewNDJSONWriter`, per-node artifacts; Bubble Tea TUI; web UI on :2389), Layer 4 **DIAGNOSIS** (Tracker's `Diagnose` / `DiagnoseMostRecent` / `Audit` / `Doctor` programmatic APIs returning JSON-serializable failure reports — **strongest Layer 4 source in survey**), Layer 6 cost routing
- **None**: Layer 2 (jsonl file is LLM-streaming patterns, not held-out scenarios), Layer 5
- **Strongest v4 transfusion target**: Tracker's Diagnose/Audit/Doctor shape for the Healer agent + 21-rule DOT linter for formula linting

### 6.5 Cross-runner pattern

- Layer 2: essentially absent except OpenHands' sibling repo
- Layer 3: well-covered, three different shapes (Kilroy/recording, Fabro/operator surface, OpenHands/session management)
- Layer 4: primitive in Mammoth/Tracker only (programmatic diagnosis surface)
- Layer 5: unshipped everywhere
- Layer 6: cost-routing covered; A/B + promotion absent

---

## 7. Per-capability OSS landscape

(Aggregated from research; expanded in `README.md` Part 4)

### Layer 2 — scenarios + judge (P5 + P6)

| Capability | Best OSS | License | Status |
|---|---|---|---|
| Scenario authoring | Inspect AI | MIT | Mature; recommended |
| Alternative authoring | promptfoo, OpenAI Evals, DeepEval, AgentDojo | MIT/MIT/Apache 2.0/MIT | Mature alternatives |
| Scenario runner | Inspect AI runner | MIT | Recommended |
| LLM-as-judge | Inspect AI scorer, Ragas, DeepEval | MIT/Apache 2.0/Apache 2.0 | Mature |
| Satisfaction aggregation | Inspect AI score reduction | MIT | Mature within framework |
| Holdout isolation | None purpose-built | DIY | OPA + file permissions composition |
| Cross-family enforcement | None | DIY | Custom model stylesheet rule |

### Layer 3 — observability + "why" (P8 + observability)

| Capability | Best OSS | License | Status |
|---|---|---|---|
| LLM instrumentation | OpenLLMetry, OpenInference | Apache 2.0 | Mature |
| Claude Code instrumentation | Native OTLP via env vars | n/a (Anthropic) | Native |
| Generic event collection | OpenTelemetry Collector | Apache 2.0 | Very mature |
| LLM event storage | LangFuse, Helicone | Apache 2.0/Apache 2.0 | Mature |
| **AVOID** | Phoenix (Arize) — **Elastic License** | Elastic | Restrictive on hosted services |
| Trace browsing | LangFuse, Jaeger, Tempo | Apache 2.0/Apache 2.0/Apache 2.0 | Mature |
| Session/conversation | LangFuse (best), Phoenix | Apache 2.0/Elastic | LangFuse cleaner |
| Manual override logging | None purpose-built | DIY (Claude Code hook) | Small custom |
| "Why" field capture | None | DIY (hook handler) | Small custom |
| Pattern surfacing | None | DIY (SQL queries) | Small custom |

### Layer 4 — self-healing loop (P11)

| Capability | Best OSS | License | Status |
|---|---|---|---|
| Content-addressed substrate | CXDB | Apache 2.0 | Only player; mature for purpose |
| Generic event substrate fallback | LangFuse | Apache 2.0 | Mature |
| Numeric anomaly detection | PyOD, Anomalib | BSD-2/Apache 2.0 | Mature generic |
| LLM-trajectory anomaly | None turnkey | DIY | Compose on generic |
| Trajectory embedding | sentence-transformers | Apache 2.0 | Mature |
| Clustering | scikit-learn, HDBSCAN | BSD/BSD | Mature |
| Diagnosis agent | **None — strongest exemplar is Tracker's Diagnose API** | TBD verify | DIY with strong gene-transfusion source |
| Fix-task generation | None | DIY | Small custom |
| Durable workflow | Temporal, Inngest, Trigger.dev, Restate, Hatchet | MIT/Apache 2.0/Apache 2.0/Apache 2.0/Apache 2.0 | Very mature (generic) |
| Loop closure tracking | None | DIY | Small custom — bead schema |
| Healer governance | OPA | Apache 2.0 | Mature |

### Layer 5 — digital twins (P7)

| Capability | Best OSS | License | Status |
|---|---|---|---|
| HTTP record/replay | VCR.py, polly.js, go-vcr, HoverFly | MIT/Apache 2.0/MIT/Apache 2.0 | Mature |
| Stateful HTTP mocking | WireMock, Mountebank, Mockoon | Apache 2.0/MIT/MIT | Mature |
| OpenAPI-driven mock | Prism, Stoplight | Apache 2.0/various | Mature |
| Contract verification | Pact, schemathesis | MIT/MIT | Mature |
| Service-specific exemplar | **LocalStack** (AWS), Firebase Local Emulator | Apache 2.0/Apache 2.0 | **Strongest Layer 5 gene-transfusion target** |
| Twin scaffolding from SDK | **None** | DIY | Per-service work; no turnkey |
| Behavioral fidelity testing | None turnkey | DIY | Manual diff tooling |

### Layer 6 — self-optimization (P12)

| Capability | Best OSS | License | Status |
|---|---|---|---|
| Meta-metric tracking | MLflow, Aim, Weights & Biases (freemium) | Apache 2.0/Apache 2.0/freemium | Mature |
| Manual variant identification | Git branches + tags | n/a | Trivial |
| Auto variant — prompt-program | DSPy | MIT | Mature in narrow domain |
| Auto variant — hyperparameter | Optuna, Ray Tune | MIT/Apache 2.0 | Mature generic |
| Auto variant — methodology/topology | **None** | DIY | Research frontier |
| A/B routing | Unleash, GrowthBook, Flagsmith, OpenFeature | Apache 2.0/MIT/BSD-3/CNCF spec | Mature for product features |
| Counterfactual replay | CXDB branching + driver | Apache 2.0 + DIY | Primitive exists; driver yours |
| Statistical comparison | scipy.stats, statsmodels, Evidently AI | BSD/BSD/Apache 2.0 | Mature |
| Multi-armed bandit | Vowpal Wabbit, MABWiser | BSD/Apache 2.0 | Mature narrow domain |
| Promotion gate | None | DIY | Small custom (formula) |
| Experiment registry | MLflow, W&B, DVC | Apache 2.0/freemium/Apache 2.0 | Mature |
| Regression detection | Evidently AI, NannyML | Apache 2.0/Apache 2.0 | Mature for ML monitoring |

---

## 8. Multi-capability projects (reduce dependency count)

| Project | Slots covered | License |
|---|---|---|
| Gas City | All Layer 0-1; bead substrate for DIY items | MIT |
| Inspect AI | L2: authoring + runner + judge + aggregation | MIT |
| LangFuse | L3: storage + browsing + session + prompt versioning; weak L4 fallback | Apache 2.0 |
| CXDB | L4 substrate + L4 trajectory enabler + L6 counterfactual primitive | Apache 2.0 |
| Temporal | L4 durable workflow + L6 experiment orchestration foundation | MIT |
| DSPy | L6 variant identification + L6 statistical comparison (prompt-programs) | MIT |
| MLflow | L6 meta-metric tracking + L6 experiment registry | Apache 2.0 |

---

## 9. Gene transfusion technique

Reference: corpus term from Jesse Vincent / Compound Atelier. From `architectures/v3/build-guide/01-vocabulary.md`: "applying a working pattern from one codebase to another by pointing the agent at a concrete exemplar and asking it to reproduce the behavior, instead of describing the pattern from scratch."

**Application to v4**: every component the factory builds for itself transfuses from at least one external exemplar. This is the technique that makes the factory-builds-factory plan tractable. Current-generation models port and adapt reliably; they invent from scratch unreliably.

### 9.1 Transfusion source map per layer

**Layer 2 — scenarios + judge**:
- Authoring: Inspect AI Task class, promptfoo YAML, OpenAI Evals JSONL, AgentDojo
- Judge: Inspect AI scorer, Ragas, DeepEval
- Aggregation: Inspect AI score reduction, MLflow tracking
- Holdout enforcement: ML training pipelines (sklearn train_test_split, MLflow experiment isolation)

**Layer 3 — observability + "why"**:
- LLM telemetry: OpenLLMetry, OpenInference
- Storage schema: LangFuse data model, Phoenix OpenInference, Jaeger spans
- Sessions: LangSmith conventions, LangFuse hierarchy
- Override pattern: AWS CloudTrail, GCP Audit Logs, auditd, git reflog
- Pattern surfacing: Honeycomb BubbleUp (documented), Datadog Watchdog (documented)

**Layer 4 — self-healing**:
- Content-addressed: git object store (canonical), IPFS, Bazel CAS
- Anomaly detection: Anomalib (PyTorch), PyOD, Prometheus alerting patterns
- Embedding + clustering: sentence-transformers + HDBSCAN (standard recipe)
- **Diagnosis agent**: Tracker's `Diagnose`/`Audit`/`Doctor` (strongest LLM-pipeline transfusion target), Anthropic's Claude Code investigation patterns, Sentry Performance Insights (documented), Honeycomb BubbleUp blog posts
- Durable workflow: Temporal SDK examples (Go/Python/TS), Inngest patterns, AWS Step Functions
- Fix-task: AWS Auto Remediation Lambda, K8s controllers, Ansible auto-remediation playbooks

**Layer 5 — digital twins**:
- HTTP record/replay: VCR.py, polly.js, go-vcr, HoverFly
- Stateful twin: WireMock (Java gold standard), Mountebank, Mockoon
- Service exemplars: **LocalStack** (AWS, canonical), Firebase Local Emulator, Stripe test mode (documented)
- Contracts: Pact, schemathesis, Dredd

**Layer 6 — self-optimization**:
- Prompt optimization: DSPy compilers (Bootstrap, BootstrapFewShot, MIPRO), Anthropic prompt-improver patterns
- Hyperparameter search: Optuna, Ray Tune
- A/B routing: Unleash, GrowthBook, OpenFeature spec implementations
- Statistical comparison: scipy.stats, Evidently AI
- Multi-armed bandit: Vowpal Wabbit, MABWiser
- Counterfactual replay: git cherry-pick mechanics, Temporal workflow replay (closest analogs; no LLM-specific exemplar)

### 9.2 Discipline patterns

- Attribute every transfusion in component metadata: `transfused_from: <url>`
- Scenarios cite original exemplar behavior
- License hygiene: track transfusion source license per component
- Permissively-licensed transfusions can be donated back upstream; restrictively-licensed ones stay private

---

## 10. License caveats

### 10.1 Specific issues to remember

- **Phoenix (Arize)**: Elastic License — restrictive for hosted services. Use LangFuse instead.
- **Gas City `internal/` paths**: GitHub blocks direct module import. **Only matters for Go library use of Gas City.** v4 extends Gas City via packs (TOML config + tool node binaries + prompt templates), which require no Go imports. No fork needed for v4. Would only become relevant if a future v4 need required source-level Gas City modification — new runtime Provider, modified reconciler, urgent upstream bug fix.
- **Tracker license**: verify before adoption (likely MIT, 2389 convention)
- **Claude Code CLI**: Anthropic ToS — Max subscription allows subprocess automation; OAuth tokens NOT permitted outside Claude Code/claude.ai
- **Weights & Biases**: free tier non-commercial; consider MLflow or Aim as fully-OSS alternatives

### 10.2 License-clean alternatives chosen

Where multiple options exist with different licenses, v4 picks the permissive choice for OSS-release viability:

| Slot | Chosen | Alternative considered | Why |
|---|---|---|---|
| LLM observability | LangFuse | Phoenix | Phoenix Elastic License restrictive |
| Experiment tracking | MLflow or Aim | Weights & Biases | W&B is freemium |
| Prompt optimization | DSPy | OpenAI Evals optimization | DSPy is more general |

---

## 11. Decision history (session decisions made + deferred)

### 11.1 Decisions made

| Decision | Resolution | Rationale |
|---|---|---|
| Pivot from v3 methodology-pick to v4 principle-runtime | Yes | Methodology is variable; substrate is convergent |
| Gas City as runtime baseline | Yes | Smallest viable install handles 6 of 12 principles natively |
| CXDB integration | Yes, Phase 1 | Required for principle 10 (memory layer) full + principles 11 + 12 |
| Bridge path: raw API bodies → CXDB | Yes, recommended | Lowest impedance; bridge is a standalone tool-node binary in a pack that transfuses the pattern from `internal/sessionlog` (no Go imports of Gas City needed) |
| Skip OTLP → CXDB path | Yes | StrongDM explicitly designed CXDB against OTel span tree model |
| Inspect AI for Layer 2 | Yes | Most mature general-purpose; agent-trajectory model fits |
| LangFuse for Layer 3 | Yes | Phoenix's Elastic License excludes it for hosted-service paths |
| Formula↔DOT bidirectional translator | Yes, Phase 1 | Resolves Gas City vs Attractor-shape impedance; enables Mammoth-style linting |
| Gene transfusion technique | Yes | Makes Phase 3+ tractable for factory self-build |
| Factory-builds-factory after Layer 2 | Yes | StrongDM pattern; minimizes human engineering investment |
| Self-optimization as 12th working principle | Yes | Replaces "publish pipeline files" in working set; natural extension of P11 |
| Phase 0 = minimum Gas City install only | Yes | Validates baseline before adding complexity |
| Phase 1 = verbatim OSS adoption (no invention) | Yes | Separates "configure" from "invent" risk |
| Phase 2 = Layer 2 + bootstrap validation | Yes | First factory-built component proves/disproves whole approach |
| Pack-based extension of Gas City; no fork | Yes | Gas City's pack model (TOML + tool node binaries + prompt templates) covers all v4 extension needs. Forking only warranted for source-level Gas City modification (new runtime Provider, modified reconciler, urgent upstream bug fix), none of which v4 needs. |

### 11.2 Decisions deferred

| Decision | Deferred until | Why deferred |
|---|---|---|
| Which v3 candidate methodology to pursue first | After Phase 2 | Pick whichever has smallest custom-pack scope (likely GF-M) |
| Whether to contribute Gas City extraction upstream | After Gas City migrations settle | Two CI-enforced migrations in flight; team likely "thanks, not yet" |
| Whether to look at Warren (Overstory successor) | When fleet-shape multi-agent need surfaces | Overstory archived 2026-05-28; Warren status unverified |
| Whether to extract just Gas City tmux runtime vs adopt minimum install | Settled: adopt minimum install | Earlier extraction recommendation was framed around different goal |
| Whether to add Temporal for durable workflow | When Gas City Orders prove insufficient | Gas City Orders may be enough; Temporal is fallback |
| Whether to build twins (Layer 5) for which dependencies | After rate limits or production exposure bite | Just-in-time per dependency |
| Self-optimization-as-principle in El Kaim 11 | Not formally added to corpus | v4 working principle only |

### 11.3 Considered and rejected

| Option | Rejected because |
|---|---|
| Build pipeline runner from scratch | Gas City exists and covers Layer 0-1 substantially |
| Use Kilroy as pipeline runner instead of Gas City | Kilroy minimal, no work-ledger or attribution at Gas City's depth |
| Use Mammoth as pipeline runner instead of Gas City | Mammoth is DOT-runner frontend; Tracker library underneath is good but less integrated |
| OTLP path for Claude Code → CXDB | Span tree vs turn DAG impedance; CXDB designed against OTel |
| Phoenix instead of LangFuse | Elastic License restrictive on hosted services |
| Wait until June 15 for Agent SDK Max access before starting | Subprocess automation works under Max today |
| Build self-healing before evaluation (Layer 2) | Can't evaluate factory's own work without scenarios + judge |
| Pick a v3 methodology and build for it | Wrong question per pivot rationale |
| Fork Gas City and vendor `internal/` paths | Earlier framing in v4 docs overstated this. Pack-based extension handles all v4 needs without Go library imports. Fork only warranted for source-level Gas City modification, which v4 doesn't need. Corrected 2026-05-29. |

---

## 12. Open technical questions

- **Tracker's license**: needs verification before transfusion / adoption
- **Mammoth's exact 21 DOT linter rules**: should be documented and ported to formulas
- **Kilroy's exact CXDB integration shape**: per-stage `prompt.md` / `response.md` etc. — pattern is described; need direct repo inspection for transfusion
- **Warren (Overstory successor) status**: project description known; capabilities and license unknown
- **Inspect AI's session-id model vs Gas City's**: likely needs adapter layer; impedance unknown
- **OPA policy for scenario isolation**: scope of "agent can't read" needs concrete enforcement design
- **Cross-family judge enforcement**: specific Gas City model stylesheet syntax for "judge != coder"
- **Counterfactual replay driver**: no good exemplar; design problem largely unsolved
- **Self-optimization meta-metrics**: which specifically? Values question — needs operator input

---

## 13. Specific config skeletons

### 13.1 Phase 0 minimum (verified to satisfy minimum-viable spec)

**`pack.toml`**:
```toml
[imports.core]
```

**`city.toml`**:
```toml
[workspace]
name = "v4-bootstrap"

[[agent]]
name = "worker"
provider = "claude"

[beads]
provider = "file"
```

**`agents/worker/prompt.template.md`**: arbitrary; whatever the worker's initial prompt should be.

That's the entire Phase 0 install. ~30 lines.

### 13.2 Phase 1 additions to `city.toml`

```toml
[formulas]
# enables formula DAG composition

[[service]]
name = "langfuse"
type = "external"
endpoint = "http://localhost:3000"

[[service]]
name = "cxdb"
type = "external"
endpoint_msgpack = "tcp://localhost:9009"
endpoint_http = "http://localhost:9010"

[[service]]
name = "otel_collector"
type = "external"
endpoint = "http://localhost:4317"
```

Plus Claude Code environment variables (set in Gas City session config):

```toml
[[agent]]
name = "worker"
provider = "claude"
env = { CLAUDE_CODE_ENABLE_TELEMETRY = "1",
        OTEL_METRICS_EXPORTER = "otlp",
        OTEL_LOGS_EXPORTER = "otlp",
        OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317",
        OTEL_LOG_RAW_API_BODIES = "file:/var/lib/cxdb-bridge/inbox" }
```

### 13.3 Phase 2 additions

Inspect AI scenario rig partition:

```toml
[[rig]]
name = "scenario_authoring"
read_partition = "scenarios"
write_partition = "scenarios"

[[rig]]
name = "implementer"
read_partition = "code"
write_partition = "code"
# explicitly does NOT include scenarios in read_partition
```

Inspect AI invocation as Gas City tool node (sketch):

```toml
[[tool]]
name = "inspect_eval"
type = "subprocess"
command = "inspect"
args = ["eval", "{scenario_path}", "--task", "{task}"]
work_partition = "scenarios"
```

---

## 14. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Gas City migration breaks downstream | Medium | Medium | Pin specific Gas City version; track migrations; budget for 1-2 breaking changes/quarter |
| ~~Internal path forking forever~~ Not applicable to v4 | n/a | n/a | v4 doesn't import Gas City as Go library; pack-based extension handles all v4 needs. Forking only warranted if future work requires source-level Gas City modification. |
| CXDB stays small-team | Medium | Medium | Apache 2.0 means fork is always available; design integration to minimize lock-in |
| Phase 2 bootstrap validation fails | Medium | High | Iterate on spec; if persistent, add more substrate before Phase 3 |
| Layer 5 twin work doesn't transfer well | Medium | Medium | LocalStack is the strong exemplar; budget per-service work |
| Layer 6 self-optimization driver too research-flavored | High | Medium | Build last; heaviest human review; can stop at L4 self-healing if needed |
| Vocabulary cost causes team friction | High | Low | Glossary; pair sessions; cost is front-loaded |
| OpenHands' eval harness model doesn't fit | Medium | Low | Inspect AI is the primary choice; OpenHands is transfusion source not direct dep |
| Claude Code Max policy changes | Low | High | Anthropic ToS could shift; not under our control; have API-key fallback path ready |
| Tracker license is non-permissive | Low | Medium | Verify before adoption; if restrictive, transfuse pattern without adopting code |

---

## 15. Key URLs and references

### 15.1 OSS projects

- Gas City: `github.com/gastownhall/gascity`
- Beads: `github.com/gastownhall/beads`
- CXDB: `github.com/strongdm/cxdb`
- Claude Code: `github.com/anthropics/claude-code` (CLI)
- LangFuse: `github.com/langfuse/langfuse`
- Inspect AI: `github.com/UKGovernmentBEIS/inspect_ai`
- OpenLLMetry: `github.com/traceloop/openllmetry`
- OpenTelemetry Collector: `github.com/open-telemetry/opentelemetry-collector`
- Temporal: `github.com/temporalio/temporal`
- DSPy: `github.com/stanfordnlp/dspy`
- Optuna: `github.com/optuna/optuna`
- LocalStack: `github.com/localstack/localstack`
- WireMock: `github.com/wiremock/wiremock`
- Mountebank: `github.com/bbyars/mountebank`
- PyOD: `github.com/yzhao062/pyod`
- Anomalib: `github.com/openvinotoolkit/anomalib`
- sentence-transformers: `github.com/UKPLab/sentence-transformers`
- HDBSCAN: `github.com/scikit-learn-contrib/hdbscan`
- MLflow: `github.com/mlflow/mlflow`
- Unleash: `github.com/Unleash/unleash`
- GrowthBook: `github.com/growthbook/growthbook`

### 15.2 Documentation references

- Claude Code OTLP: `code.claude.com/docs/en/monitoring-usage.md`
- Agent SDK Max: `support.claude.com/en/articles/15036540`
- Agent SDK overview: `code.claude.com/docs/en/agent-sdk/overview`

### 15.3 Local references (this repo)

- v3 build guide: `architectures/v3/build-guide/`
- v3 vocabulary: `architectures/v3/build-guide/01-vocabulary.md`
- v3 paradigm + 12 principles matrix: `architectures/v3/build-guide/02-paradigm.md`
- v3 substrate map: `architectures/v3/build-guide/03-substrate.md`
- v3 candidates: `architectures/v3/build-guide/04-candidates.md`
- v3 per-candidate diagrams: `architectures/v3/build-guide/05-per-candidate-diagrams.md`
- Gas City deep dive: `research/followup/13-gas-city-deep-dive.md`
- Gas Town beads: `research/followup/04-gastown-beads.md`
- Gas Town deep dive: `research/followup/14-gas-town-deep-dive.md`
- Gas systems substrate: `research/38-gas-systems-substrate.md`
- Attractor implementations: `research/followup/02-attractor-implementations.md`
- Dark factory article: `reference-only/f675af7d98/dark-factory-article.txt`

---

## 16. For the agent picking up v4 cold

Read in this order:
1. **This file** for the dense map
2. **`architectures/v4/README.md`** for the human-readable approach + diagrams
3. **`architectures/v3/build-guide/02-paradigm.md`** for the 12 principles matrix
4. **`architectures/v3/build-guide/03-substrate.md`** for the OSS substrate landscape
5. **`research/followup/13-gas-city-deep-dive.md`** for Gas City internals

Then if you're working on:
- **Phase 0 setup**: Section 13.1 above, plus Gas City README upstream
- **Phase 1 OSS adoption**: Sections 4-5 above + each project's docs
- **Phase 2 Layer 2**: Sections 7 (Layer 2 row) + 11.1 (Inspect AI choice) + 13.3
- **Phase 3+ factory-builds-factory**: Sections 9 (gene transfusion) + 8 (multi-capability projects)
- **License questions**: Section 10 + `README.md` Part 5

If you're picking up an in-progress factory-built component:
1. Find its bead with `gc bd find --type factory_build_in_progress`
2. Check `transfused_from` attribution
3. Find the spec in `packs/*/spec.md`
4. Find the scenarios at `scenarios/<component>/`
5. Resume the workflow with `gc converge resume <bead_id>`

If you're updating this document:
- The next agent will read this. Be dense, structured, attributed.
- Cite sources by repo URL or relative path within this repo.
- Mark decisions vs. deferrals explicitly.
- Update Section 11 (decision history) when new decisions are made.
- Update Section 12 (open questions) when items get resolved.

---

*Document created: 2026-05-29 by Claude during v4 planning session. Dense, AI-readable. Companion to human-facing `README.md`. Last updated: 2026-05-29.*
