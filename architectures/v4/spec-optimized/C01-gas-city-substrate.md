# C01 — Gas City runtime substrate  (Spec, Track B)

> Source: AI-CONTEXT §3 (Gas City load-bearing dependency: §3.1 coverage map, §3.2 nine concepts, §3.3 vocab, §3.4 smallest viable install, §3.5 migration tail, §3.6 extractability), §11.1 (decisions), §14 (risk register), §13.1 (Phase-0 skeleton); README Part 2 ("three layers + persistence"), Part 4 P3/P4/P9/P10 "Gas City placement" cells, Part 6 (Phase 0 = minimum Gas City install); _meta component-inventory C01 row; _meta gaps G11, G03 (assigned), plus G29/G06/G33 (touched at seam). F-MODE-COVERAGE: F31 (provider lock-in), F52 (controller-patch trap), substrate availability.
> Inventory ID: C01   Kind: subsystem   Status: sweep-1
> Deltas: DELTA-01 (substrate-portability contract: define a thin `RuntimeSubstrate` interface C01 *is*, so Gas City is an implementation not an axiom — retires the G11 single-point-of-failure bet), DELTA-02 (mandatory version pin + conformance-suite gate before any "Native" claim is trusted), DELTA-03 (native-coverage count corrected to 5-at-Phase-0, P3 explicitly `[formulas]`-gated, aligned with C03 DELTA-05), DELTA-04 (the substrate↔pack tool-node seam is a *typed ABI owned by C02*, not an undocumented Gas City internal — C01 only guarantees the subprocess contract exists and is conformance-tested), DELTA-05 (reconciler bounded-iteration + escalation invariant lifted into the substrate contract to pre-empt F52 oscillation at the lowest layer), DELTA-06 (degraded-mode / supervised-restart contract for the substrate process itself, since v4 only ever claims "Orders survive crashes" for *workflows*, never for the runner).

## 1. Purpose & responsibility

C01 is **the runtime substrate**: the single load-bearing process that turns DOT-shaped TOML workflow definitions into running, attributed work. It is the layer README Part 2 calls "the three layers + persistence" collapsed into one adopted third-party runtime (Gas City `gc`) plus the **portability contract** that lets v4 not die if that runtime does (DELTA-01). Concretely, C01 owns five primitive capabilities and exposes them to every other component:

1. **Workflow execution** — load a formula (C12's TOML DAG), instantiate it into a molecule (C13), drive it node-by-node.
2. **Agent/tool dispatch** — hand a unit of work (bead/wisp) to an agent session (C28 via C04) or a deterministic tool node (C17 via C02's ABI). This is the *sling* (C05) sitting on the substrate's dispatch primitive.
3. **Reconciliation** — the per-tick desired-state convergence loop ("Health Patrol") that C18 specializes; C01 owns the bare control-loop primitive and its termination invariant (DELTA-05).
4. **Persistence mount points** — the substrate hosts the bead store (C19), event bus (C23), and session state (C04); it does not define their schemas but provides their storage lifecycle and the `created_by` attribution stamp (C41) on every action.
5. **Config load** — reads the layered TOML (C03) at startup/reload and uses section-presence to decide which of the above capabilities activate.

C01 covers, per the source coverage map, **~5–6 of the 12 principles natively** at minimum install: P1 (prompt-template/spec machinery), P2 (session provider), P4 (reconciler + tool nodes), P9 (attribution — the strongest native match in the corpus), P10 (bead work-graph). P3 (formula DAGs) is native **only when `[formulas]` is enabled**, which Phase 0 turns off — so the honest Phase-0 native count is **5, not 6** (DELTA-03, G03).

What C01 is **NOT**:
- **Not** the workflow *format* — the TOML DAG schema is C12; C01 *executes* it. Not the molecule schema — that is C13.
- **Not** the pack bundle format or the tool-node wire protocol — that is C02. C01 only guarantees a conformance-tested subprocess seam exists (DELTA-04).
- **Not** the config layering/precedence semantics — that is C03. C01 *invokes* C03's loader and acts on the resulting `EffectiveConfig`.
- **Not** the bead/event/CXDB schemas (C19/C20/C23/C21) — it hosts their storage, it does not define their types.
- **Not** the session/provider internals (tmux/k8s/subprocess lifecycle, resume) — that is C04; C01 declares the dispatch boundary C04 plugs into.
- **Not** Gas City itself. C01 is the *contract that Gas City satisfies* (DELTA-01). v4 adopts Gas City as the implementation; C01 is the surface everything else codes against, so a future re-platform is a swap behind one interface, not a rewrite.

## 2. Context & dependencies

- **Depends on (declared in inventory):**
  - **C03** (config / feature-flags) — C01 calls C03's loader to get `EffectiveConfig`; section-presence is what tells C01 which capabilities to start. *Note: this is a load-order dependency, not a build dependency — C03's contract is "what the substrate must honor"; see plan §4.*
  - **C04** (session & provider runtime) — C01 dispatches agent work *through* C04; C04 owns the provider lifecycle/resume, C01 owns the dispatch decision and attribution stamp.
- **Foundational fan-out (consumed by, directly):** C02 (pack ABI extends C01), C05 (sling is C01's dispatch specialized), C06 (messaging rides C01), C07 (vocabulary names C01's concepts), C12/C13 (formula/molecule are what C01 executes), C17 (tool-node abstraction runs on C01's tool-bead primitive), C18 (reconciler specializes C01's control loop), C19/C21/C23 (stores mount on C01), C41 (attribution stamp is C01-provided). Effectively *every* component traces a dependency edge back to C01; it is the root of the dependency DAG.
- **Sits at:** the absolute bottom of the Runtime Substrate subsystem and of the whole system. Nothing is below it except the OS and the third-party runtime binary it wraps.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete signatures + the conformance suite in sweep 2). C01's interfaces are the **`RuntimeSubstrate` contract** (DELTA-01) — the set of operations every dependent codes against, so the Gas City implementation is swappable.

**Inbound (what C01 offers upward):**
- `LoadConfig(layers) → EffectiveConfig` — delegates to C03; returns the validated, capability-resolved view that gates everything else.
- `RunFormula(formula_ref, inputs) → MoleculeHandle` — instantiate a C12 formula into a live C13 molecule and begin execution. Pre: `[formulas]` capability enabled. Post: a molecule exists in the bead store with a root bead and `created_by` attribution.
- `Dispatch(work_unit, target) → DispatchReceipt` — route a bead/wisp to an agent session (→ C04/C28) or a tool node (→ C02 subprocess ABI). The substrate primitive under C05's sling. Post: every dispatch emits an attributed event to C23.
- `Tick(molecule) → ConvergenceStatus` — advance one reconciliation step toward desired state. **Invariant (DELTA-05):** bounded — a molecule node cannot tick more than `max_iterations` times without either converging, gating, or escalating to a `stuck`/`needs_human` terminal; no unbounded controller-patch loop (F52).
- `Persist(action) → EventSeq` / store mount accessors — append-only write to the event bus (C23) and bead store (C19) with monotonic seq and `created_by` stamp (C41).
- Lifecycle: `Start()`, `Reload()`, `Drain()`, `Shutdown()`, `Health() → SubstrateHealth` (DELTA-06).

**Outbound (what C01 requires downward / from the host):**
- The **Provider** boundary (→ C04): a session-lifecycle interface (start/exec/resume/stop) the substrate calls to materialize an agent runtime. v4's baseline provider is `claude` (Claude Code under Max).
- The **tool-node subprocess ABI** (→ C02, DELTA-04): a defined stdin/stdout(+exit-code) contract by which a deterministic tool-node binary receives inputs and returns outputs. C01 guarantees this seam exists and is conformance-tested; **C02 owns the wire format** (resolves the G29 "actual seam is undocumented" finding by assigning ownership, not by re-specifying it here).
- The config loader (→ C03), the bead/event store drivers (→ C19/C23 storage providers `file`|`dolt`).

**Invariants (substrate-wide):**
- **Attribution-total (P9):** every state-changing action that flows through C01 carries a `created_by` actor (C41) and lands an event on C23. No anonymous mutation. This is the load-bearing transform's "every action attributed" half.
- **Config-gated activation:** a capability is live **iff** C03 reports its gating section present *and valid*; C01 never half-starts a capability.
- **Bounded reconciliation (DELTA-05):** see `Tick` above.
- **Deterministic-first dispatch:** where a node is typed as a tool node, C01 dispatches to a subprocess, never to an LLM session (the substrate-level expression of P4; C16 enforces the *discipline*, C01 enforces the *routing*).
- **Conformance-pinned (DELTA-02):** the running substrate binary's version is pinned and must pass the C01 conformance suite before any "Native" capability claim in README Part 4 is trusted in CI.

## 4. Data model / state

C01 owns *storage lifecycle and the attribution stamp*, not the schemas (those are C19/C20/C21/C23). What C01 itself holds:

- **Substrate process state:** the in-memory registry of active capabilities (derived from `EffectiveConfig`), the set of live molecules/sessions, the reconciler tick clock, and the current health/drain state.
- **Mount points (storage lifecycle, not schema):**
  - Bead store (C19) — `file` (Phase 0) or `dolt` (later); C01 opens/closes/migrates it, C20 defines its types.
  - Event bus (C23) — append-only JSONL, monotonic seq; C01 guarantees ordering + durability of the append, C23 defines the record shape.
  - Session state (C04) — provider-backed; C01 tracks which molecule owns which session for attribution + resume.
- **The `created_by` stamp (C41):** the one piece of *content* C01 injects into every persisted action — actor identity threaded from the dispatching session/rig.
- **Version + conformance manifest (DELTA-02):** pinned `gc` version, conformance-suite hash, and the capability→principle coverage assertion (so the "5 native at Phase 0" claim is a checked artifact, not prose — G03/DELTA-03).
- Consistency: event-bus appends are the linearization point — an action is "real" once its event is sequenced; bead/CXDB writes are downstream of that. (Sweep 2 pins the exact ordering vs. the C26→G26 bridge seam.)

## 5. Behavior

Key flows (sweep 1 = prose; sweep 2 = Mermaid sequence + state diagrams):

- **Cold start:** `Start()` → `LoadConfig` (C03) → instantiate enabled capabilities in dependency order (persistence mounts → providers → dispatch → reconciler → formulas-if-on) → emit a `substrate_started` attributed event → ready. If a required capability fails to init, **fail-closed** (refuse to serve), consistent with C03's load-time gate.
- **Run a workflow:** `RunFormula` → C12 parse → C13 instantiate molecule (bead-tree) → reconciler picks up the molecule → per node: classify (tool vs agent) → `Dispatch` → on completion advance desired-state → repeat under the bounded-tick invariant → terminal (converged | gated-on-human | escalated).
- **Reconciliation loop (the "Health Patrol" primitive):** each tick computes (desired − actual) for live molecules, dispatches the next legal step, records progress. **Bounded (DELTA-05):** per-node iteration counter; on hitting `max_iterations` without progress → emit `stuck` bead + escalate (C18/C39 own the escalation policy; C01 owns the *guarantee that the loop terminates*).
- **Reload:** `Reload()` re-runs `LoadConfig`; capabilities observe a config-generation switch (immutable generations, per C03) rather than mutating in place; in-flight molecules continue on their generation.
- **Degraded mode (DELTA-06):** if a *downstream* store/service is unavailable (CXDB down, Dolt unreachable), C01 enters a declared degraded posture — agent work and event-bus appends continue (the irreducible core), capabilities that hard-depend on the missing store are quiesced and their molecules parked, not dropped. Supervised restart of the substrate process replays from the event bus + bead store to reconstruct live molecules. (This is the substrate-level answer to G33 "no story for partial OSS-stack failure," scoped to what C01 can guarantee.)

## 6. Failure modes & handling

| F-mode / gap | Risk | C01 handling |
|---|---|---|
| **G11 (blocker): Gas City is an unverified single point of failure** | "If Gas City fails, the whole plan reorganizes" (README §552); no version run/pinned. | **DELTA-01 + DELTA-02:** C01 *is* a thin `RuntimeSubstrate` interface that Gas City implements, so a re-platform is a swap behind one contract; plus a pinned version + conformance suite that must pass before any "Native" cell is trusted. Converts an unbounded architectural bet into a bounded, tested dependency with an exit. |
| **G03 (major): native-count double-counts P3** | Headline "6 of 12 native" but P3 is `[formulas]`-gated and Phase 0 turns formulas off. | **DELTA-03:** C01's coverage manifest asserts **5** native at Phase 0; P3 flips to native when `[formulas]` enables (consistent with C03 DELTA-05). The claim becomes a CI-checked artifact. |
| **F52: controller-patch / oscillation trap** | A reconciler that keeps "patching" can loop forever; the Healer (C39) can create new anomalies. | **DELTA-05:** bounded-tick invariant *in the substrate contract* — per-node iteration cap → escalate. The lowest layer refuses to spin, so every loop built on it (C18, C39) inherits termination. |
| **F31: provider/runtime lock-in** | Single `claude` provider + single runtime. | Provider boundary (→C04) and `RuntimeSubstrate` interface (DELTA-01) both keep the lock-in behind a named seam; model-floor routing (C29) and provider swap stay possible. |
| **G29 (minor): pack↔runtime tool-node seam undocumented** | "Packs cover all extension" but the subprocess ABI is never specified. | **DELTA-04:** C01 *names and owns the existence of* the seam and conformance-tests it; the wire format is assigned to C02 (no silent gap, no duplication). |
| **G33 (major): partial OSS-stack failure** (scoped) | CXDB/Dolt/LangFuse down mid-run. | **DELTA-06:** declared degraded mode — core (agent loop + event bus) survives, store-dependent capabilities quiesce and park molecules; replay-on-restart from event bus. Full cascade handling is C40/C33's; C01 guarantees the *substrate* doesn't lose committed work. |
| Substrate process crash | The runner itself dies (v4 only ever claims *workflows* survive). | **DELTA-06:** supervised restart + event-bus/bead-store replay reconstructs live molecules. Event-bus append is the durability boundary. |

## 7. Cross-cutting

- **Security:** C01 is where `created_by` attribution becomes total (P9) — the substrate stamps every action, which is the precondition for C41's audit trail and C57's failure attribution. The substrate also hosts the boundary where C43's isolation (Bash/network/fs) is applied per session; C01 declares that boundary exists, C43 defines its policy.
- **Cost/scale:** the substrate-side throughput ceiling is one Claude-Max seat (G34); C01 can't lift it, but the dispatch primitive + provider boundary make pooling/queueing and the C29 model-floor routing the place to manage it. C01's own overhead is the reconciler tick + event append — O(live molecules).
- **Observability:** every action is an attributed event on C23 (the lowest-impedance CXDB source per AI-CONTEXT §5.4); `Health()` exposes substrate posture for the self-healing loop.
- **Ops:** version pin + conformance suite (DELTA-02) is the operational gate for adopting a new `gc` release (the docs warn 1–2 breaking pack/formula changes per quarter through 2026, §3.5). Degraded mode + supervised restart (DELTA-06) is the run-time ops contract.

## 8. Acceptance criteria & test strategy

1. **Conformance gate (DELTA-02):** the pinned `gc` version passes the C01 conformance suite (provider lifecycle, dispatch, reconciler tick, event append + ordering, attribution stamp); a failing suite blocks the "Native" coverage claim in CI.
2. **Phase-0 minimum install runs (G11 evidence):** the §13.1 skeleton (`pack.toml [imports.core]`, `city.toml` with one `[[agent]] provider="claude"` + `[beads] provider="file"`, one prompt template) cold-starts, dispatches one agent unit of work, and lands an attributed event — proving the load-bearing dependency actually works, not just asserted.
3. **Native-coverage honesty (G03/DELTA-03):** with `[formulas]` **off**, the coverage manifest reports exactly **5** native principles (P1,P2,P4,P9,P10) and P3 = gated-off; turning `[formulas]` on flips P3 to native and `RunFormula` succeeds.
4. **Attribution-total invariant:** a fuzz/property test that *no* state-changing path produces an event without a `created_by` actor.
5. **Bounded reconciliation (DELTA-05):** a deliberately non-converging molecule hits `max_iterations` and escalates (emits `stuck`/`needs_human`) rather than looping — asserted with a forced-stall scenario.
6. **Portability contract (DELTA-01):** a no-op / stub `RuntimeSubstrate` implementation satisfies the same conformance suite, proving dependents code against the interface, not against Gas City internals.
7. **Degraded mode + restart (DELTA-06):** kill CXDB mid-run → core agent work + event appends continue, store-dependent molecules park; kill the substrate process → supervised restart replays and reconstructs the live molecule set with no lost committed events.

## 9. Open questions

- **OQ1 (→ review-log, top):** How thick is the `RuntimeSubstrate` interface (DELTA-01) allowed to be before it becomes a de-facto Gas City re-implementation? If Gas City's surface is wide and idiosyncratic, a faithful-but-thin portability contract may be infeasible, and DELTA-01 degrades to "document the lock-in" (cf. AI-CONTEXT §3.6 extraction surface ≈ 20 Go files for the runtime alone). This is the load-bearing risk of the whole optimization.
- **OQ2:** Does Gas City already provide a bounded-iteration guarantee in its reconciler, or must DELTA-05 be enforced by a wrapper C01 owns? Determines whether DELTA-05 is "describe existing behavior" or "add a gate," touching the C18 seam.
- **OQ3:** The C04↔C01 split of provider lifecycle — exactly which lifecycle ops belong to C01's `Dispatch` vs. C04's session management? Needs co-spec with C04 before sweep 2 signatures freeze.
- **OQ4 (→ G11 residual):** No author has run `gc` and the repo URL is asserted, not verified (AI-CONTEXT §15.1). Acceptance criterion #2 is the de-risking action; until it passes, every "Native" claim downstream is provisional.
