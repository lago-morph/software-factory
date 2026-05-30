# C01 — Gas City Runtime Substrate  (Spec, Track A)

> Source: README §Part 4 (Layer/principle placement tables — Pipeline engine line 121, Tool node / reconciler lines 158–160, attribution lines 226–228, memory lines 239–242, event substrate line 252), §Part 6 Phase 0 (lines 353–374) and Phase 1 (lines 376–399); AI-CONTEXT §2 (three-layer + persistence shape, lines 46–54), §3 (Gas City as load-bearing dependency: §3.1 coverage map lines 62–77, §3.2 "nine concepts" lines 79–93, §3.3 vocabulary lines 95–112, §3.4 smallest viable install lines 114–122, §3.5 migration tail lines 124–129, §3.6 extractability lines 131–135), §11 decisions (lines 463–476, 494–502), §13.1 Phase 0 skeleton (lines 522–544), §13.2 Phase 1 additions (lines 546–580), §14 risk register (line 616); component-inventory C01 row (line 13) + critical-path notes; ambiguities-and-gaps G11, G03.
> Inventory ID: C01   Kind: subsystem   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C01 is the **load-bearing third-party runtime substrate** of Software Factory v4: an *adopted* (not
authored) install of **Gas City** — a single Go binary `gc` — configured as the factory's foundation.
It is the engine on which everything else runs. Per AI-CONTEXT §2 it occupies the **pipeline-engine tier**
of the convergent "three-layer + persistence" shape (the DOT-graph workflow runner) — the
*three-layer-architecture* sense of "layer" (C07 canonical sense 1, G01), **not** the numbered
"Layer 0–6" principle-tier sense — and it natively *supplies* the persistence + dispatch tiers. The component's job is to provide, from a *minimum
install*, a principled runtime that already satisfies ~5–6 of the 12 principles before any custom code
is written (AI-CONTEXT §3.6: "Gas City provides P1, P2, P3, P4, P9, P10 native").

**Responsibilities (what Gas City natively owns and C01 is the spec-of-record for):**
- **DOT-shaped TOML workflow running** — execute formulas (TOML DAG templates) by instantiating them
  into molecules (live bead-trees) and driving them to completion (AI-CONTEXT §3.2 concept 7; README
  line 121 "DOT-shaped workflow runner … The baseline").
- **Agent dispatch** — the `sling` mechanism routes a bead/wisp to an agent or pool (AI-CONTEXT §3.2
  concept 8). C01 owns the substrate; the dispatch *policy* component is C05.
- **Persistence** — the bead store (durable typed work-graph, file or Dolt) and the event bus
  (append-only JSONL with monotonic seq) (AI-CONTEXT §3.2 concepts 2–3; README lines 239, 252).
- **Reconciler / Health Patrol** — the per-tick desired-state convergence loop with bounded gates
  (AI-CONTEXT §3.2 concept 9; README line 159 "native").
- **Config / feature-flag model** — layered TOML where section presence enables a capability
  (AI-CONTEXT §3.2 concept 4). C01 hosts it; the model itself is specced by C03.
- **Universal attribution** — `created_by` flows automatically through every bead and event with no
  configuration (README lines 227, 231 "Gas City's strongest native match").
- **Pack-based extension surface** — load distributable bundles (TOML + tool-node binaries + prompt
  templates) as the *only* sanctioned extension mechanism (no Go fork). C01 hosts; C02 specs the ABI.
- **Provider-backed sessions** — a stable runtime backed by a Provider (tmux/k8s/subprocess/exec),
  hosting the `claude` agent preset (AI-CONTEXT §3.2 concept 1). C01 hosts; C04 specs the session model.

**Explicitly NOT (boundaries):**
- **NOT authored by the factory.** C01 is *adopted verbatim* from upstream (`github.com/gastownhall/gascity`,
  AI-CONTEXT §15.1, MIT). v4 does **not** fork it and does **not** import it as a Go library
  (AI-CONTEXT §3.5, §11 lines 476/502; README line 334). Our deliverable is the **install + config +
  version-pin + pack-loading contract**, not Gas City's source.
- **NOT the things that merely *sit on* Gas City.** The config model (C03), session/provider model (C04),
  sling policy (C05), messaging (C06), vocabulary (C07), formula format (C12), molecule runtime (C13),
  tool-node abstraction (C17), reconciler-loop *behaviour* (C18), bead store schema (C19/C20), event
  bus seam (C23), identity model (C41), and Orders (C40) each have their own spec. C01 is the **host
  and the boundary** — it states *that* Gas City provides these and *how the substrate is installed and
  pinned*, deferring each concept's detailed contract to its owning component.
- **NOT CXDB.** CXDB (C21) is a *separate* Apache-2.0 store added in Phase 1 via a bridge (README line 122
  "CXDB via bridge"); it is not part of the Gas City substrate.
- **NOT the agent loop.** Claude Code (C28) is the agent/LLM-client layer that Gas City *drives* via the
  `claude` provider preset; it is a distinct dependency, not part of C01.

> [FAITHFUL-FILL] The inventory one-liner says "covers ~5–6 principles natively." v4 names the native set
> precisely as **{P1, P2, P3, P4, P9, P10}** (AI-CONTEXT §3.6, line 135; README Phase 0 "What's delivered",
> lines 367–372). The ~5–6 range is the same ambiguity as G03 (see §6); the minimal faithful reading is
> "6 sections claim native, but at the *smallest* (Phase 0) install one of them (P3) is only latent." This
> is the smallest consistent choice because it reproduces both the headline count and the Phase-0 caveat
> verbatim rather than asserting a single number v4 never commits to.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C03** Config / feature-flag model | C01 *hosts* the layered-TOML config; C03 defines its semantics (section-presence = flag). C01 cannot be configured without C03's model. (inventory C01 "Depends on: C03, C04") |
| Upstream (depends on) | **C04** Session & provider runtime | C01 *hosts* sessions; C04 defines the provider abstraction (tmux/k8s/subprocess) + cross-session resume that C01's `[[agent]]` preset relies on. |
| External dependency | **Gas City** (`gc` binary, MIT) | The adopted third-party runtime itself. **G11 blocker** lives here (§6). |
| External dependency | **Claude Code CLI** (C28, under Max) | Driven by the `claude` provider preset; the agent/LLM layer C01 dispatches to. |
| Downstream (consumers) | **C02** Pack ABI; **C05** Sling; **C06** Messaging; **C07** Vocabulary; **C08** Spec artifact; **C12** Formula format; **C13** Molecule; **C17** Tool-node; **C18** Reconciler loop; **C19/C20** Bead store/schema; **C21/C23** CXDB bridge / Event bus; **C40** Orders; **C41** Identity; **C42** Rig partitioning | Per inventory, these list C01 (directly or transitively) as a dependency. They consume C01's runtime, persistence, dispatch, and extension surfaces. |

> [AMBIGUITY: C01↔C03 dependency direction] The inventory lists C01 `Depends on: C03, C04`, but the C03,
> C04, C07, C02 rows each list `Depends on: C01`. C01↔C03 is therefore a **cycle** in the canonical
> inventory (the same XC-1 class flagged for C19↔C20). Both rows are cited here verbatim. The faithful
> reading that resolves the cycle is C01-B's: C01 depends on C03's *contract* at **load time** (it calls
> C03's loader), while C03 depends on C01 as the **host** that parses the TOML — a contract dependency, not
> a build-order cycle. C01 records both and **defers** the canonical ruling to the integrator pass.

**Position in the system.** C01 is **Batch-1 foundational** (inventory line 107) and sits at the root of
the dependency forest: it is the "load-bearing third-party dependency. If Gas City fails, the whole plan
reorganizes" (README §11 / AI-CONTEXT, the G11 admission). It is Phase 0 in the delivery plan (C54) and
is the only component that ships with "no custom code" (README line 355).

## 3. Interfaces / contracts

Sweep-1: interfaces are **named and described**; signatures/schemas defer to sweep 2 and to owning
components. C01's contracts are the *substrate seams* — what the install exposes to the rest of v4.

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **`gc` CLI** | inbound (operator/automation) | The single Go binary's command surface — e.g. `gc bd find --type …`, `gc formula export <name> --format dot`, `gc converge resume <bead_id>` (AI-CONTEXT §16 lines 695–699; README line 384). The control plane for the substrate. | C01 (this) |
| I2 | **`city.toml` / `pack.toml` config load** | inbound (config) | Layered TOML the runtime parses at boot; section presence toggles capabilities (`[formulas]`, `[mail]`, `[daemon]`, `[rigs]`, `[[service]]`, `[beads]`). | C03 (semantics), C01 (hosting) |
| I3 | **Pack-load + tool-node ABI** | inbound (extension) | Load a pack (TOML + tool-node binaries + prompt templates); invoke a tool node as a subprocess with a defined input/output protocol. The *sole* extension surface (no Go fork). | **C02** (the ABI itself) |
| I4 | **Provider / session interface** | outbound (to agent) | The `runtime.Provider` interface (~18 methods, AI-CONTEXT §3.6) backing a Session; hosts the `claude` preset to drive Claude Code. | **C04** (session model), C28 (agent) |
| I5 | **Workflow-run interface (formula → molecule)** | internal/inbound | Instantiate a formula (TOML DAG) into a molecule (bead-tree) and run it; sling routes resulting wisps/beads. | C12/C13 (formats), C05 (sling), C01 (execution host) |
| I6 | **Bead store API** (`gc bd …`) | outbound (persistence) | CRUD + query over the durable typed work-graph (file or Dolt), with `created_by` attribution. | **C19/C20** (store/schema) |
| I7 | **Event bus** (append-only JSONL) | outbound (persistence/telemetry) | Monotonic-seq append log recording every action; lowest-impedance CXDB source. | **C23** (event bus), C24 (bridge) |
| I8 | **Reconciler / Health Patrol tick** | internal control loop | Per-tick desired-state convergence with bounded convergence gates. | **C18** (loop behaviour) |

**Invariants C01 must uphold (substrate-level):**
- **INV-1 (pinned version):** the running `gc` is at a single pinned version; the install is reproducible
  from the pin (mitigates AI-CONTEXT §3.5 migration tail).
- **INV-2 (no fork / no Go import):** v4 never imports Gas City `internal/` or `pkg/` paths; all extension
  is via packs (AI-CONTEXT §11 lines 476/502).
- **INV-3 (universal attribution):** every bead written and every event emitted carries `created_by`
  with no per-call configuration (README line 231).
- **INV-4 (feature-gating by section presence):** a capability is OFF iff its config section is absent;
  the Phase-0 install has `[daemon]`, `[mail]`, `[formulas]`, `[rigs]`, Dolt, `[[service]]`, orders all
  absent ⇒ off (AI-CONTEXT §3.4 line 122).

## 4. Data model / state

C01 *owns the install and config*; the **schemas** of the stores it hosts are owned downstream (deferred,
faithful to inventory). State C01 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Install + version pin** | The `gc` binary, its pinned version, and the workspace layout (`packs/*`, `agents/<name>/prompt.template.md`). | Filesystem + version control (packs are git-versioned, README line 107). | C01 |
| **`city.toml` / `pack.toml`** | Layered TOML config (workspace, agents, beads provider, optional sections). | Version-controlled file. | C03 |
| **Bead store** | Durable typed work-graph; `provider = "file"` at Phase 0, Dolt optional later. | File (`.beads`) or Dolt server. | C19/C20 |
| **Event bus log** | Append-only JSONL, monotonic seq. | `events.jsonl`-style append log. | C23 |
| **Molecule (in-flight)** | A formula instantiated into a live bead-tree; the runtime state of a running workflow. | In bead store (molecule = bead-tree). | C13 |

**Phase-0 install (the canonical minimum — AI-CONTEXT §13.1):**

```toml
# pack.toml
[imports.core]
```
```toml
# city.toml
[workspace]
name = "v4-bootstrap"

[[agent]]
name = "worker"
provider = "claude"

[beads]
provider = "file"
```
Plus `agents/worker/prompt.template.md`. ~30 lines TOML + one template = full minimum (AI-CONTEXT §3.4).
**Explicitly off at Phase 0:** `[daemon]`, `[mail]`, `[formulas]`, `[rigs]`, Dolt server, `[[service]]`,
orders (AI-CONTEXT §3.4 line 122; README line 364).

**Consistency / lifecycle.** Beads + events provide cross-session durability and the audit trail (P9/P10).
Phase-1 layering adds `[formulas]` and `[[service]]` blocks (langfuse/cxdb/otel) per AI-CONTEXT §13.2;
these are additive — they do not alter the Phase-0 substrate, only turn on latent capabilities (INV-4).

## 5. Behavior

**Boot & configure (Phase 0).** Operator installs the pinned `gc`, writes `pack.toml` (`[imports.core]`)
and `city.toml`, and one prompt template. `gc` parses the layered TOML; absent sections ⇒ capabilities
off (INV-4). One `[[agent]]` with `provider = "claude"` makes Claude Code (C28) the worker via the
session Provider (C04). `[beads] provider = "file"` stands up the file-backed work-graph. Result:
a runnable single-agent factory with attribution + memory, no custom code (README line 355).

**Run a unit of work (single-step at Phase 0; formula-driven from Phase 1).**
1. Work is represented as a bead/wisp in the store.
2. **Sling** (C05) routes it to the `worker` agent/pool by template/role.
3. The agent runs inside a provider-backed **session** (C04) driving Claude Code.
4. Every action emits an **event** (append-only JSONL) and updates **beads**, all carrying `created_by`.
5. The **Health Patrol** reconciler (C18) ticks toward desired state, applying bounded convergence gates.
6. At Phase 1, multi-step work is a **formula** (TOML DAG, C12) instantiated into a **molecule**
   (bead-tree, C13); the same dispatch/persist/reconcile loop drives each node.

**Phase-1 capability turn-on.** Adding `[formulas]` enables DAG composition; adding `[[service]]` blocks
registers external services (LangFuse, CXDB, OTel collector) and agent `env` wires Claude Code telemetry
(AI-CONTEXT §13.2). The substrate's behaviour is unchanged; latent sections light up (INV-4).

> Sequence/state diagrams (Mermaid), exact `gc` subcommand contracts, and the formula→molecule execution
> algorithm are **sweep-2+** and largely owned by C04/C05/C12/C13/C18. Deferred here per sweep-1 altitude.

## 6. Failure modes & handling

C01 is where the two foundation-level gaps assigned to it live.

**G11 (blocker) — "Gas City exists, is obtainable, and works as described" is an unverified assumption.**
v4 itself admits "Gas City is the load-bearing third-party dependency. If Gas City fails, the whole plan
reorganizes" (README §11). There is no evidence any author has run `gc`, no version pin, and the repo
URL is asserted not verified. Every "Native" cell in README Part 4 is an unverified claim about a
third-party tool.
> [AMBIGUITY: G11] Two readings. **(a)** *Treat Gas City as proven* — spec the substrate as if all Native
> cells hold (the docs' surface stance). **(b)** *Treat adoption as a risk to retire first* — the install
> + every Native claim is a hypothesis requiring a verification gate before downstream specs rely on it.
> **Chosen: (b)**, as most consistent with the rest of v4: README §552 and AI-CONTEXT §14 *both* name
> this as the single highest structural risk and Phase 0's explicit goal is "validate baseline before
> adding complexity" (AI-CONTEXT §11 line 473). Faithful handling ⇒ C01's acceptance criteria (§8)
> include a **Gas City-conformance verification** that exercises each claimed-native capability against
> a *pinned* `gc`, and a recorded version pin (INV-1). v4 prescribes no fallback design if the bet fails
> (the API-key/Temporal fallbacks are for other risks), so C01 **defers** "what replaces Gas City" to the
> phase-plan/residual-risk register (C54/C57) — it is out of C01's faithful scope to invent a replacement.

**G03 (major) — the "6 of 12 native" count is internally unsupported.** AI-CONTEXT §11.1 and §3.6 say
"6 of 12 native" listing {P1,P2,P3,P4,P9,P10}; but §3.1 rates P3 only "**Strong when `[formulas]`
enabled**," and Phase 0 turns `[formulas]` **off** (§3.4; README Phase 0 itself: P3 "full when formulas
turn on in Phase 1"). So at the *smallest* install P3 is latent, not delivered ⇒ Phase-0 native count is
**5, not 6**; the headline double-counts P3.
> [AMBIGUITY: G03] Two readings. **(a)** *6 native* — count P3 because the *capability* (formula engine)
> exists in `gc` even when the section is off. **(b)** *5 native at Phase 0, 6 from Phase 1* — count only
> what is *delivered* at the given install. **Chosen: (b)**: it is the only reading consistent with both
> §3.4 ("explicitly off: `[formulas]`") and README Phase 0's own "full when formulas turn on in Phase 1."
> Faithful resolution: C01's spec states the native set as **{P1,P2,P4,P9,P10} at Phase 0 (=5)** and
> **{P1,P2,P3,P4,P9,P10} from Phase 1 (=6)**, and the inventory's "~5–6" is read as exactly this
> phase-dependent range — not a hand-wave. The C57 coverage register is the canonical reconciler of the
> count; C01 defers the corpus-wide headline-count fix to C57.

**Migration tail (AI-CONTEXT §3.5, §14 line 616).** Two CI-enforced upstream migrations are in flight;
expect 1–2 breaking pack-schema/formula-format changes per quarter through 2026. **Mitigation (faithful):**
pin a specific `gc` version (INV-1), track migrations, budget for breakage (AI-CONTEXT §14). Detection:
conformance suite (§8) fails on a version bump that breaks a Native claim.

**Degraded behaviour.** If a non-Phase-0 capability's section is misconfigured, INV-4 means it is simply
*off* (fail-safe to the smaller install) rather than a crash — faithful to "section presence = flag."

> F-mode applicability is owned by C57 (coverage map); C01 surfaces the substrate-level failure classes
> (dependency unavailability G11, version drift) and defers the canonical F1–F61 mapping there.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C01 hosts the substrate; the lethal-trifecta / isolation posture is **NOT** C01's
  (deferred to C43/C42/C44). C01 only guarantees universal attribution (INV-3) as the audit foundation
  (P9). Secret handling for `env`/`[[service]]` endpoints is flagged but unspecced in v4 (G37) ⇒ deferred
  to C37-config/C57; C01 notes the plaintext-TOML exposure but does not resolve it (out of faithful scope).
- **Cost.** Phase-0 substrate cost is effectively the `gc` binary (free, MIT) + one Claude Code Max seat
  ($200/mo, AI-CONTEXT §4.1). v4 gives no other substrate cost model (G32, deferred to C46/C57).
- **Scale.** The substrate's throughput ceiling is the single-Max-seat agent limit (G34) — a property of
  C28/C29, not the runner. C01 imposes no additional ceiling at Phase 0 (single agent).
- **Observability.** The event bus (I7) records every action; Phase-1 wires Claude Code OTLP + raw-API
  bodies (AI-CONTEXT §13.2). C01 *hosts* these; C23–C27 own them.
- **Ops.** Install = single Go binary; "single-engineer day to a few days, mostly config" (README line
  374). Version pin + reproducible install are the key ops invariants (INV-1).

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (Phase-0 install runs):** the ~30-line `pack.toml` + `city.toml` + one template install boots a
   single Claude Code worker with file-backed beads and **no custom code** (README Phase 0; AI-CONTEXT §13.1).
2. **AC-2 (native capabilities verified — resolves G11/G03):** a **Gas City conformance check** exercises
   each Phase-0 Native claim against the *pinned* `gc` and records pass/fail: P1 (templates+config in VC),
   P2 (three-layer: agent+client+engine+beads), P4 (reconciler + tool-node primitives present), P9
   (`created_by` on every bead+event), P10 (bead store task-graph + cross-session resume). **P3 is
   asserted NOT delivered at Phase 0** and becomes an AC only after Phase 1 turns `[formulas]` on.
3. **AC-3 (version pinned & reproducible — INV-1):** the install records a single `gc` version; re-install
   from the pin is byte-reproducible; a version bump that breaks any AC-2 claim is detected by the suite.
4. **AC-4 (no-fork invariant — INV-2):** no v4 artifact imports Gas City `internal/`/`pkg/`; all extension
   is via packs (verifiable by build-graph inspection).
5. **AC-5 (feature-gating — INV-4):** with the Phase-0 config, `[daemon]`, `[mail]`, `[formulas]`,
   `[rigs]`, Dolt, `[[service]]`, orders are all OFF; adding the Phase-1 `[formulas]` section turns DAG
   composition on without altering Phase-0 behaviour (AI-CONTEXT §3.4, §13.2).
6. **AC-6 (attribution end-to-end — INV-3):** a unit of work produces beads and events all carrying a
   resolvable `created_by`, queryable via `gc bd …` and the event log (README line 231).

**Test strategy.** A conformance pack (transfusable shape: Gas City's own `runtimetest/conformance.go`,
AI-CONTEXT §3.6) that boots the pinned `gc`, runs one trivial unit of work, and asserts AC-1…AC-6. This
suite is the *de-risking gate* for G11 and must pass before any Batch-2 component builds against C01.

## 9. Open questions

- **OQ-1 (→ review-log, top):** **G11** — has anyone actually run `gc` end-to-end against the v4 Native
  claims, and what is the pinned version + commit? Until a conformance run exists, every downstream
  "Native" dependency is provisional. *This is the single highest-leverage unknown in v4.*
- **OQ-2:** Which `gc` version to pin given two in-flight CI-enforced migrations (AI-CONTEXT §3.5)? Need a
  version that satisfies all Phase-0/1 Native claims *and* a documented upgrade procedure.
- **OQ-3:** Exact `gc` CLI surface (subcommands/flags) v4 relies on (`gc bd`, `gc formula export`,
  `gc converge resume`) — enumerate and freeze at sweep 2 so C05/C12/C18 can build against it.
- **OQ-4 (→ C57):** The corpus-wide "6 of 12 native" headline still needs reconciling to the
  phase-dependent 5/6 (G03); C01 fixes its own statement but the global count lives in the coverage map.
