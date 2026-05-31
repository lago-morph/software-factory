# Survivor Pass — applying the strict bar to optimized Track B deltas

> **Purpose.** Decide, per Track-B delta, whether to fold a minimal form into the canonical `spec/` track or to drop it as scope creep. Drives the convergence to one track.

> **The bar (from operator, this session):** *"We are building thin glue on a stack of existing software (Gas City + libraries like prometheus / scikit-learn / PyOD / opentelemetry / sigstore / etc.). For each delta, ask: would ANY part of the principle this delta touches be at least partially satisfied by that stack + small glue? If yes → DROP. Only KEEP-MINIMAL if the principle would get NO satisfaction without custom code. Partial satisfaction counts. Perfection is not the bar. Scope creep is very very bad."*

> **Three test outcomes per delta:**
> - **DROP** — hardening / enforcement on top of upstream code, or adds requirements v4 didn't require, or defensive structure not needed yet
> - **KEEP-MINIMAL** — needed because the principle would otherwise get NO satisfaction; pulled in *minimal form* (a slot, a name, a contract — not enforcement, not validation gates, not exhaustive taxonomy)
> - **ALREADY IN** — folded into faithful via INTEGRATION-PASS-1 (D-1..D-5)

> **Pre-decided drops (operator rulings this session):**
> - Bet 1 (Portability contracts): DROP C01-01, C04-01, C21-01, C28-01
> - Bet 2 (Mandatory signing): DROP C41-01, C41-06
> - Bet 3 (L2/L3 judge): DROP C29-02 L2/L3 portion + C29-03 (L1 baseline already in faithful via D-1)
> - Bet 4 (Multi-seat pool): DROP C28-03
> - Skeptic rescind: DROP C07-03, C12-06, C13-07

> **When in doubt: DROP.** The operator's "very very bad" weighting on scope creep flips ties to DROP.

---

## C01 — Gas City Substrate

Stack: Gas City directly. We use `gc` as-is.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | RuntimeSubstrate port | DROP | Bet 1 |
| 02 | Version pin + conformance suite | DROP | Pinning a version is operator config; writing a conformance suite gating Gas City's "Native" claims = hardening upstream |
| 03 | 5 native at Phase-0 (machine-checked) | DROP | Honesty doc, not code |
| 04 | Tool-node typed ABI | KEEP-MIN | The tool-node ABI is where OUR factory code meets tool nodes — name the seam. Drop the "co-specified with C02 + conformance test" framing |
| 05 | Reconciler bounded-iteration | DROP | Gas City's reconciler; we don't add bounds on top |
| 06 | Degraded-mode / supervised restart | DROP | Gas City's behavior; we use what it gives |

**Keep: 1 (DELTA-04 minimal). Drop: 5.**

---

## C02 — Pack Extension ABI

Stack: Gas City packs. Pack contents (tool nodes, prompts, formulas) are OUR code.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Explicit JSON wire protocol | KEEP-MIN | We're authoring tool nodes; they need a calling convention. Minimal = "JSON over stdin/stdout, status in exit code" — not the full typed-envelope machinery |
| 02 | Signed versioned PackManifest | DROP | Signing dropped (Bet 2 spirit); versioned manifest is Gas City's concern |
| 03 | Typed I/O envelope + exit-code taxonomy | DROP | Closed taxonomy is enforcement we don't need yet |
| 04 | Capability declaration → C43 grant | DROP | C43 enforcement layer dropped per "no enforcement on top" |
| 05 | ABI version handshake | DROP | Defensive; add when we actually have ABI breaks |
| 06 | Language-neutral Go + Python parity | DROP | Over-engineered; pick one language as needed |
| 07 | Fork-trigger criteria | DROP | Documentation concern, not spec |

**Keep: 1 (DELTA-01 minimal). Drop: 6.**

---

## C03 — Config / Feature Flags

Stack: Gas City's TOML config + viper-like libraries.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Explicit layer precedence | DROP | Gas City does layered TOML |
| 02 | Capability descriptor registry | DROP | Formal capability model = defensive |
| 03 | Secret-reference indirection | DROP | We don't have a secrets layer yet (G37 unresolved) |
| 04 | Load-time validation gate | DROP | Gas City validates its own config |
| 05 | Phase-0 native-count honesty | DROP | Operator doc, not code |
| 06 | Config provenance event | DROP | Defensive audit |

**Keep: 0. Drop: 6.**

---

## C04 — Session Provider

Stack: Gas City's `runtime.Provider` (~18 methods), Claude Code's session.id.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | SessionProvider contract | DROP | Bet 1 |
| 02 | ResumeToken with fidelity contract | DROP | Gas City session resume + Claude Code session-id exist; we don't add a fidelity-contract layer |
| 03 | CredentialSource fallback ladder | DROP | Max-only for now; no ladder needed |
| 04 | Heartbeat / liveness emission | DROP | Use prometheus / opentelemetry / process-level liveness — don't custom-build |
| 05 | Isolation-at-spawn (C42/C43 binding) | DROP | OS-level enforcement = hardening; we trust process boundaries Gas City gives |
| 06 | Multi-session pool / drain / restart | DROP | Bet 4 spirit; Gas City handles session lifecycle |

**Keep: 0. Drop: 6.**

---

## C05 — Sling Dispatch

Stack: Gas City's sling (dispatch/route is Gas City native).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Typed RoutingDecision over RoutingKey | DROP | Gas City sling has routing; not our code |
| 02 | Admission-controlled back-pressure | DROP | Gas City dispatch handles this |
| 03 | Pool routing + fairness + anti-starvation | DROP | Gas City's |
| 04 | Routing-key vs binding authority split | DROP | Clarification of Gas City behavior, not new code |
| 05 | Convoy atomicity policy | DROP | Gas City convoys |
| 06 | Dispatch record schema | DROP | Audit log; defensive |

**Keep: 0. Drop: 6.**

---

## C07 — Vocabulary / Glossary

Stack: Markdown docs; word discipline.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Machine-readable glossary registry | DROP | Prose glossary suffices; schema fields are scope creep |
| 02 | Canonical-reading authority | DROP | Just write good docs |
| 03 | Provenance + corpus-name mapping | DROP | Skeptic rescind |
| 04 | Vocab-lint hook → C10/C15 | DROP | CI nicety; not needed |
| 05 | Deprecation lifecycle | DROP | Not needed at this scale |
| 06 | Lock-in cost + extraction synonym | DROP | Analytical doc, not code |

**Keep: 0. Drop: 6.**

---

## C08 — Spec Artifact

Stack: OUR spec system (specs are the source of truth, P1).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Spec = standalone bundle (not template) | KEEP-MIN | Structural — specs are their own thing, not prompt content |
| 02 | Multi-file bundle + manifest | KEEP-MIN | `spec.md` + `DoD.md` is sensible structure for P1 |
| 03 | Enumerated per-criterion DoD | KEEP-MIN | Satisfaction scoring (P5) needs SOME structure in DoD |
| 04 | BLAKE3 content-addressed identity | DROP | Defensive; content-hash if we ever need it |
| 05 | Required-section schema validator | DROP | Linter polish |
| 06 | Graded detail level + clarification hook | DROP | Sophistication not needed |

**Keep: 3 (DELTAs 01, 02, 03 minimal). Drop: 3.**

---

## C09 — Prompt Template Binding

Stack: Go `text/template`. Our templates.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Bind template by spec_id | KEEP-MIN | Templates reference specs; minimal = "template includes a spec reference" |
| 02 | Typed RenderContext (closed namespace) | DROP | Our convention, not spec-level |
| 03 | Content-addressed binding_id record | DROP | Defensive audit |
| 04 | Sandboxed FuncMap | DROP | We trust our own templates; standard `text/template` is fine |
| 05 | missingkey=error + prompt.id | DROP | One-line Go config + correlation id; implementation detail |
| 06 | Spec-embed strategy (link/inline/summarize) | DROP | Over-engineered |

**Keep: 1 (DELTA-01 minimal). Drop: 5.**

---

## C10 — Spec Linter (EARS)

Stack: OUR linter component.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Pure tool-node + typed report | KEEP-MIN | We're building a linter; it needs a report shape — minimal = "findings with rule-id and severity" |
| 02 | Lint over C08 bundle | KEEP-MIN | Yes, the linter operates on specs |
| 03 | Severity + advisory/blocking | KEEP-MIN | Linters need severities |
| 04 | Vocab-lint wired to C07 | DROP | No C07 machinery |
| 05 | Versioned configurable rule registry | DROP | Config polish |
| 06 | 0-1 score + threshold gate | DROP | Defensive |

**Keep: 3 (DELTAs 01, 02, 03 minimal). Drop: 3.**

---

## C12 — Formula Pipeline File

Stack: Gas City's formula TOML grammar exists and is native.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Versioned formula schema | DROP | Gas City formula TOML grammar is upstream; we use it |
| 02 | Node taxonomy (agent/tool/gate/sub_formula) | DROP | Gas City already has these node kinds |
| 03 | Parameter + binding contract | DROP | Gas City formula parameters |
| 04 | Methodology-as-data identity | DROP | Documentation convention, not code |
| 05 | DAG well-formedness invariants | DROP | Gas City validates DAGs on load |
| 06 | Provenance + transfusion lineage | DROP | Skeptic rescind |
| 07 | DOT round-trip canonical form | DROP | Gas City `gc formula export --format dot` exists |

**Keep: 0. Drop: 7.**

---

## C13 — Molecule Runtime State

Stack: Gas City molecules. Lifecycle is Gas City native.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Named addressable + lifecycle FSM | DROP | Gas City molecules already have an FSM |
| 02 | Transactional bind→materialize→seal | DROP | Gas City's instantiate semantics |
| 03 | Root bead as resume anchor | DROP | Gas City `gc converge resume <bead_id>` works as-is |
| 04 | Tree-shape invariants | DROP | Gas City's bead graph enforces shape |
| 05 | Run-scope loop bound | DROP | Reconciler control; Gas City's |
| 06 | Direct dep on C19, not C18 | DROP | Architectural clarification; doesn't change our code |
| 07 | Re-instantiation / branch-from-midpoint | DROP | Skeptic rescind |

**Keep: 0. Drop: 7.**

---

## C17 — Tool Node Abstraction

Stack: Tool nodes are OUR code (Python/Go scripts called via C02 wire).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Runtime catalog/registry + invoke facade | KEEP-MIN | We have multiple tool nodes; need a name → invoke mapping. Minimal = "registry of name→executable" |
| 02 | Typed NodeInterface descriptor | DROP | Schema fields = enforcement |
| 03 | Determinism-class taxonomy | DROP | Categorization for caching = optimization, not needed |
| 04 | Result-cache / memoization | DROP | Optimization |
| 05 | Built-in vs pack node parity | DROP | Internal architecture detail |
| 06 | falsifying_scenario_ref as registry field | DROP | Defensive linkage |

**Keep: 1 (DELTA-01 minimal). Drop: 5.**

---

## C19 — Bead Work Graph

Stack: Gas City's bead store (file or Dolt provider, native).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | BeadStore port (file ⇄ Dolt) | DROP | Gas City already supports both providers; not our abstraction |
| 02 | created_by NON-NULL invariant | DROP | Validation v4 doesn't require enforced; faithful records it as required-by-convention |
| 03 | Typed acyclic edge taxonomy | DROP | Gas City beads have edges; our usage picks the labels |
| 04 | File-provider durability (fsync/atomic-rename) | DROP | Gas City's durability; we use what it gives |
| 05 | Monotonic per-store seq | DROP | Gas City's seq |
| 06 | Schema enforcement at write seam | KEEP-MIN | We write fix_task / override / factory_build beads — they need *schemas* (G17). Minimal slot, see C20. Validation hook itself is Gas City's concern |
| 07 | Graph query contract frozen | DROP | Gas City `gc bd` queries exist |

**Keep: 1 (DELTA-06 minimal — really points at C20). Drop: 6.**

---

## C20 — Bead Schema

Stack: OUR bead type definitions (G17 blocker — v4 names types but defines none).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Versioned bead-type registry | KEEP-MIN | G17 closure: v4 names types without schemas. We have to define ours. Minimal = "named types + field list per type" |
| 02 | factory_build = one type + lifecycle | KEEP-MIN | Sensible choice for stable id across build lifetime |
| 03 | Closed bead-type catalog | KEEP-MIN | Pairs with DELTA-01 — minimal catalog of the types we write |
| 04 | Loop-closure contract (bounded fix-attempt) | KEEP-MIN | G18 closure: our fix-task loop hangs without termination slots. Already in faithful (slots only). Keep slot, not the unrepresentable-to-violate enforcement |
| 05 | created_by + transfused_from required | KEEP-MIN | Already in faithful as envelope fields. Minimal — declare required, no enforcement layer beyond what Gas City does |
| 06 | Schema-version migration | DROP | Premature; do when we have actual migrations |
| 07 | Bead-type ↔ CXDB binding | ALREADY IN | D-2/D-3 |

**Keep: 5 (DELTAs 01, 02, 03, 04, 05 minimal). Drop: 1. Already in: 1.**

---

## C21 — CXDB Trajectory Store

Stack: CXDB directly (Apache-2.0; we run it).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | TrajectoryStore port | DROP | Bet 1 |
| 02 | Append-idempotent by content + parent | DROP | CXDB's behavior; we use what it gives |
| 03 | v4 trajectory bundle named/versioned | ALREADY IN | D-2 |
| 04 | Degraded-mode + durable spool | DROP | Defensive resilience; CXDB handles failures |
| 05 | Branch / replay as first-class API | DROP | CXDB API |
| 06 | Retention/GC + BLAKE3 integrity | DROP | CXDB's |
| 07 | Typed projection contract | DROP | CXDB's query surface |

**Keep: 0. Drop: 6. Already in: 1.**

---

## C22 — CXDB Type Registry

Stack: CXDB type registry + bundle id (D-2/D-3 settled).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Concrete v4 trajectory bundle | ALREADY IN | D-2 |
| 02 | Viewpoint as closed enum (F50 mechanism) | DROP | Defensive guard against type-misuse; not blocking |
| 03 | Append-only + version-monotonic | DROP | CXDB registry semantics |
| 04 | Registration mechanism for two namespaces | ALREADY IN | D-3 |
| 05 | Every type carries JSON Schema | DROP | CXDB enforces what it enforces |

**Keep: 0. Drop: 3. Already in: 2.**

---

## C23 — Event Bus

Stack: Gas City's event bus (append-only JSONL with monotonic seq, native).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Named durability/ordering contract | DROP | Hardening Gas City's event bus. Skeptic flagged WJ for downstream dependency, but under strict bar: use what Gas City does, document what survives |
| 02 | Back-pressure bounded | DROP | Gas City's |
| 03 | At-least-once + event_id idempotency | DROP | Gas City's |
| 04 | Partitioned per-run streams | DROP | Gas City's |
| 05 | Segment retention contract | DROP | Gas City's |
| 06 | Schema-on-write envelope + created_by NON-NULL | DROP | Gas City's schema; we use it |

**Keep: 0. Drop: 6.**

---

## C24 — Telemetry → CXDB Bridge

Stack: Standalone Go binary, watches `OTEL_LOG_RAW_API_BODIES` dir, posts to CXDB HTTP. Listed in v4 as a deliverable. Custom code.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Dual-source bridge (BodyWatcher + BusTailer) | KEEP-MIN | We're building this bridge; need to know there are two sources |
| 02 | At-least-once + idempotent posting | KEEP-MIN | Our HTTP client; idempotency = use BLAKE3 hash AI-CONTEXT already mentions |
| 03 | Client-side durable spool | DROP | OS filesystem is the spool; we don't custom-build a state machine |
| 04 | session.id → parent-turn mapping | KEEP-MIN | We need to maintain this mapping for trajectories to thread; minimal map |
| 05 | Atomic-rename readiness for partial files | KEEP-MIN | File-watching needs to handle partials; standard pattern |
| 06 | Supervised long-lived service | DROP | Run it under systemd / supervisord; not our spec concern |

**Keep: 4 (minimal). Drop: 2.**

---

## C25 — OTLP Telemetry Export

Stack: OpenTelemetry Collector (off-the-shelf), Claude Code emits OTLP natively.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | C25 = config, not daemon | KEEP-MIN | Clarifies C25's nature: it's environment vars + collector config |
| 02 | Two-Sink Invariant (OTLP→Collector→LangFuse; raw→C24→CXDB) | KEEP-MIN | Architectural fact; anti-edges are useful design clarity |
| 03 | Raw-bodies escape hatch | DROP | Configuration detail; capture in operator setup |
| 04 | Telemetry mandatory-on + fail-safe | DROP | Operator policy, not spec |
| 05 | Single default gRPC endpoint | DROP | Operator config |

**Keep: 2 (minimal). Drop: 3.**

---

## C28 — Claude Code Agent Loop

Stack: Claude Code (the binary) IS the agent loop. We don't author the loop.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | AgentLoopProvider contract | DROP | Bet 1 |
| 02 | Token/quota governor + admission control | DROP | Claude Code reports tokens; we don't add admission control over it |
| 03 | Multi-seat / seat-pool | DROP | Bet 4 |
| 04 | Capability/egress profile per invocation | DROP | Enforcement we don't add; rely on OS / Claude Code's hook surface |
| 05 | Deterministic context-budget management | DROP | Claude Code has stop conditions; we don't add custom budgeting |
| 06 | Provider-floor conformance suite | DROP | Bet 1 spirit |
| 07 | Hooks/skills/subagents/MCP as typed config | DROP | Claude Code's surface; we use it directly via config |

**Keep: 0. Drop: 7.**

---

## C29 — Model Floor / Stylesheet

Stack: model selection. D-1 ratified L1 (same-provider judge) as Phase-0 baseline.

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | model_family + independence_class as registry fields | KEEP-MIN | Need to name model families to select them (config concern) — minimal slot |
| 02 | Graded L0-L3 judge policy | KEEP-MIN | L1 portion already in faithful via D-1. L2/L3 deferred (Bet 3). Minimal = "policy is gradable, L1 default" |
| 03 | Metered-API judge seat credential | DROP | Bet 3 (FE-1) |
| 04 | Compiled deterministic routing function | DROP | Over-engineered for model selection; we use config-based routing |
| 05 | Cost-tier as live budget-aware input | DROP | Optimization for future |
| 06 | Fail-closed + degraded_eval escape | DROP | L1 baseline is already satisfiable; no need to fail closed |

**Keep: 2 (minimal, D-1 L1 baseline already in faithful). Drop: 4.**

---

## C41 — Identity / Attribution

Stack: Gas City's native `created_by`. v4 marks signing optional/deferred (P9).

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Graduated-mandatory signing | DROP | Bet 2 |
| 02 | Canonical Actor model with 7-class taxonomy | DROP | Without signing, the taxonomy serves no enforcement; v4's loose "cities, rigs, agents" is enough for the audit log |
| 03 | Structured Attribution with delegation chain | DROP | Without signing, structured chain = audit nicety, not requirement |
| 04 | Tamper-evident hash-chain (per-actor over C23 event_ids) | ALREADY IN | D-5 (chain ownership only); signing-effectiveness deferred. Keep the D-5 ownership note in faithful, don't add the chain mechanism itself |
| 05 | First-class verify(attribution) service | DROP | No signing → nothing to verify |
| 06 | Signing-key / actor-credential model | DROP | Bet 2 |
| 07 | boundary_class tag (production/twin/isolated) | DROP | Defensive labeling; we don't have twins yet |

**Keep: 0. Drop: 6. Already in: 1 (D-5 chain *ownership note only*, not mechanism).**

---

## C42 — Rig / Agent-Role Partitioning

Stack: OS filesystem permissions, git worktrees (native to gas city). v4 says "file perms + agent-prompt discipline + audit log."

| # | Delta | Verdict | Why |
|---|---|---|---|
| 01 | Partition model + composition order | DROP | We use file perms + worktrees as-is, no formal composition stack |
| 02 | Read-isolation enforced at OS/process boundary | DROP | v4 says prompt discipline; OS-boundary enforcement = hardening we don't need yet |
| 03 | Closed role taxonomy (worker/scenario-author/judge) | KEEP-MIN | We DO have these three roles in our design; name them. Minimal = "three roles exist with default-deny on cross-role access" — no formal access matrix machinery |
| 04 | Worktree-per-run RunPartition | DROP | Git worktrees are native; we use them as-is |
| 05 | PartitionBinding object | DROP | Defensive unified-binding object; not needed |
| 06 | OPA as optional intra-partition refinement | DROP | No OPA in scope |

**Keep: 1 (DELTA-03 minimal). Drop: 5.**

---

# SUMMARY

| Category | Count | % of 148 |
|---|---|---|
| KEEP-MINIMAL | 26 | 17.6% |
| ALREADY IN (D-1..D-5) | 5 | 3.4% |
| DROP | 117 | 79.0% |

**117 drops, 26 minimal-form keeps, 5 already integrated.**

The 26 KEEP-MINIMAL deltas cluster around components that are genuinely OUR code:
- **C20 bead schema** (5) — G17 blocker: v4 names types without defining them
- **C24 telemetry bridge** (4) — listed as a deliverable in v4, custom code
- **C08 spec artifact** (3) — P1: specs are the source of truth, structural
- **C10 spec linter** (3) — our linter
- **C25 OTLP config** (2) — clarifies which-thing-feeds-what
- **C29 model floor** (2) — D-1 L1 baseline + minimal slot
- One each for C01 (tool-node seam), C02 (wire protocol), C09 (spec_id binding), C17 (tool registry), C19 (points at C20 schemas), C42 (3-role taxonomy)

The 117 drops cluster around components that are mostly Gas City wrappers (C01, C03, C04, C05, C12, C13, C19, C21, C23, C28) where Track B was hardening upstream code, plus C41 (signing dropped) and C07 (vocabulary machinery dropped).

---

# NEXT STEPS

1. Apply each KEEP-MINIMAL delta to its canonical `spec/CNN-*.md` file as a small surgical edit (strengthen an existing FILL or add a small section), recorded in INTEGRATION-PASS-1 style.
2. Capture all DROP rationales touching the 4 bets into `_meta/FUTURE-ENHANCEMENTS.md` so the deferred work is visible.
3. Archive `spec-optimized/` and `plan-optimized/` to `_meta/optimized-reference/` (don't delete — reference for future revisits of the 4 bets).
4. Full cross-spec re-read to verify consistency.
5. Then: author the 34 unbuilt components on the single canonical track, applying the same bar.
