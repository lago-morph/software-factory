# C44 — Digital Twin (per service)  (Spec, canonical track)

> Source: README §"Principle 7 — Digital twins" (line 195 "Behavioral clones of critical external dependencies. Lets scenarios run thousands per hour without rate limits."; the capability table lines 199–202 — "HTTP record/replay … VCR.py/go-vcr/polly.js … Per-language tool node"; "Stateful HTTP twin … Mock with custom logic … WireMock/Mountebank/**LocalStack** … Per-twin Gas City `[[service]]` block"; "Twin scaffolding from SDK … **No OSS** — bespoke per service, transfusion from LocalStack pattern … Per-twin Go binary"; line 204 "P7 is the most labor-intensive principle to implement. No turnkey OSS for 'twin a service from its SDK.' Build per-dependency twins, gene-transfusing from LocalStack as the strong exemplar"; line 305 dependency table "LocalStack | Apache 2.0 | The strong exemplar for Layer 5 twin patterns"; Part 6 graph node line 452 "P3C[P7: digital twins / factory builds per service]" + line 468 "Phase 3c — P7 (digital twins, per service): factory builds twins per critical dependency. LocalStack is the strong gene-transfusion exemplar. Each twin is bounded engineering; the factory's job is to follow the LocalStack-shaped pattern for a specific service's SDK contract. Repeat per dependency"; line 499 "The twins' scenarios verify behavioral fidelity against the real service"; line 520 "Layer 5 (twins) is genuinely sparse … building twins is per-service engineering work"). AI-CONTEXT §3 P7 row (line 37 "Digital twins | Behavioral clones of critical external dependencies"); §7 "Layer 5 — digital twins (P7)" capability table (lines 339–347 — "HTTP record/replay | VCR.py, polly.js, go-vcr, HoverFly | Mature"; "Stateful HTTP mocking | WireMock, Mountebank, Mockoon | Mature"; "OpenAPI-driven mock | Prism, Stoplight | Mature"; "Service-specific exemplar | **LocalStack** (AWS), Firebase Local Emulator | **Strongest Layer 5 gene-transfusion target**"; "Twin scaffolding from SDK | **None** | DIY | Per-service work; no turnkey"; "Behavioral fidelity testing | None turnkey | DIY | Manual diff tooling"); §10 exemplar list (lines 411–414 "Stateful twin: WireMock (Java gold standard), Mountebank, Mockoon … Service exemplars: **LocalStack** (AWS, canonical), Firebase Local Emulator, Stripe test mode"); §11.2 build-decision (line 487 "Whether to build twins (Layer 5) for which dependencies | After rate limits or production exposure bite | Just-in-time per dependency"); §14 risk (line 620 "Layer 5 twin work doesn't transfer well | … LocalStack is the strong exemplar; budget per-service work"); §15.1 (line 644 "LocalStack: `github.com/localstack/localstack`"). F-MODE-COVERAGE §4 "F-modes addressed by Layer 5 (P7)" (lines 54–57 — F12 lethal trifecta, F33 adversarial-prompt defeat of LLM-judge, F44 lethal-trifecta production-scissors default, F56 guardrail-bypass under stress) + §9 F55 (line 78 "twins as external truth"). component-inventory C44 row (line 56 "Behavioral clone of a critical external dependency (record/replay + stateful + OpenAPI mock); LocalStack-shaped"; maps A61/A62/A62b/A64/B65; depends C17; gaps G22/G31; foundational no) + Batch-4 placement (line 113). Maps inventory lens-IDs A61/A62/A62b/A64 (structural) + B65 (dataflow) — these are inventory-internal labels, not strings in the four source docs. ambiguities-and-gaps G22 (twin fidelity has no acceptance contract), G31 (lethal-trifecta "Addressed" but twins unbuilt+last). review-log D-13 (C43 owns lethal-trifecta blast-radius bound + twin isolation, G31; C34 owns holdout enforcement), D-6 (canonical track nomenclature). Sibling specs (same Batch 4, **on disk, sweep-1, canonical track** — and they confirm this seam): C45 `twin-fidelity` (verifies this twin; C45 §1/§3 "owns the fidelity predicate … does not build the twin (C44)"), C43 `isolation-boundary` (isolates the agent behind this twin; C43 §1 "C43 OWNS the … lethal-trifecta blast-radius bound … routes `twin`-typed surfaces to C44 twins").
> Inventory ID: C44   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C44 is **one digital twin: a behavioral clone of a single critical external dependency**, packaged so the
factory's agents and scenarios can call the twin **instead of the real service** — "Behavioral clones of
critical external dependencies. Lets scenarios run thousands per hour without rate limits" (README:195).
It is the **LocalStack-shaped** answer to P7 / Layer 5: a per-service component that **records and replays**
the dependency's traffic, **holds the dependency's state** across a session, and **answers per its OpenAPI/SDK
contract**, exposed to the workflow as a **C17 tool node** (README:199–202; AI-CONTEXT §7 lines 341–345).

C44 is **the spec-of-record for the twin's construction and its contract surface** — *what slice of the real
service this twin clones, and how that clone is exposed and assembled from off-the-shelf parts*. v4 is explicit
that this is the **"most labor-intensive principle … no turnkey OSS for 'twin a service from its SDK' … build
per-dependency twins, gene-transfusing from LocalStack as the strong exemplar"** (README:204). The keep at this
seam is therefore **not** a mocking engine (those are off-the-shelf) but the **assembly + contract surface**:
selecting and wiring the record/replay layer (VCR.py/go-vcr/HoverFly), the stateful-mock layer
(WireMock/Mountebank/Mockoon), and the OpenAPI-mock layer (Prism/Stoplight) into **one named, callable twin of
one service**, with a declared cloned-surface, transfused from the LocalStack pattern (README:199–202;
AI-CONTEXT §7 lines 341–346; C51 transfusion discipline).

**This component is a per-service template, instantiated once per twinned dependency.** "Repeat per
dependency" (README:468). C44 specifies the *shape every twin instance follows*; each concrete twin (the
twin of service X) is one instantiation.

**Responsibilities (what C44 is the spec-of-record for):**
- **Declare the cloned contract surface** — the named slice of the real dependency this twin reproduces:
  which endpoints/operations of the service's OpenAPI/SDK contract are in-scope, exposed as the twin's promise
  (README:202 "twin scaffolding from SDK"; AI-CONTEXT §7 line 343 "OpenAPI-driven mock"). This declared surface
  is the artifact C45 verifies fidelity *against* and C43 isolates the agent *behind*.
- **Compose the three off-the-shelf twin modes** into one twin (README:199–200; AI-CONTEXT §7 lines 341–343):
  - **record/replay** of captured real traffic (VCR.py/go-vcr/HoverFly — "capture and replay HTTP traffic"),
  - **stateful mock** with custom logic for state that evolves within a session (WireMock/Mountebank/Mockoon —
    "mock with custom logic"),
  - **OpenAPI-driven mock** for contract-shaped responses to un-recorded requests (Prism/Stoplight).
- **Hold the twin's session state** — the dependency state the clone must carry so a scenario's multi-step
  interaction behaves like the real service within a run (the "stateful" in "stateful + OpenAPI mock";
  AI-CONTEXT §7 line 342).
- **Expose the twin as a C17 tool node** — the twin is reached through the deterministic-step abstraction
  (C17) over the pack ABI (C02), placed via a per-twin Gas City `[[service]]` block (README:200 "Per-twin Gas
  City `[[service]]` block"; line 202 "Per-twin Go binary"). The agent calls the twin exactly as it would the
  real dependency's tool node; **service selection (twin vs real) is the caller's/scenario's choice**, not
  C44's.
- **Capture record/replay fixtures** — the recorded real-service traffic the replay layer serves, plus the
  seed/known-state the stateful layer starts from. These fixtures are C44-owned data.
- **Transfuse the LocalStack pattern** — follow LocalStack's shape for "clone a service from its contract"
  (README:204; AI-CONTEXT §7 line 345 "Strongest Layer 5 gene-transfusion target"); record `transfused_from`
  per C51. Pattern transfusion (and direct reuse of the permissive OSS engines), **not** a bespoke twin
  framework.

**Explicitly NOT (boundaries):**
- **NOT the fidelity verifier (C45).** "How close is close enough" — whether the twin's behavior actually
  matches the real service, and whether the twin's *usage* matches the service's promises — is **C45's**
  (`twin-fidelity`, inventory C45; G22). v4 lists "Behavioral fidelity testing: None turnkey / DIY / Manual
  diff tooling" (AI-CONTEXT §7 line 347) and "Contract verification … Pact … verify usage matches service
  promises" (README:201) as a **separate capability** from the twin itself. C44 *provides the twin behavior and
  declares the cloned surface*; C45 *judges it*. C44 carries no fidelity bar (G22 deferred to C45 — below).
- **NOT the isolation / blast-radius boundary (C43).** Using the twin to *bound the lethal trifecta* — typing
  Bash/network/filesystem access so the agent is held *behind* the twin and cannot reach production — is
  **C43's** (`isolation-boundary`, inventory C43; G31), per **review-log D-13** ("C43 owns the distinct
  lethal-trifecta blast-radius bound … twin isolation; G31"). C44 *builds a twin that CAN stand in for the real
  service*; C43 *makes standing-in mandatory and bounds what escapes*. The "production scissors require explicit
  declaration per pack" default (F-MODE F44) is C43's enforcement, not C44's (G31 deferred to C43 — below).
- **NOT a custom twin framework / generic twin engine.** The mocking, recording, and OpenAPI-mock engines are
  **off-the-shelf, permissive OSS** (README:199–202; AI-CONTEXT §7) — C44 wires them per service, it does not
  reimplement them. A from-scratch general-purpose twin/mock framework is the **DROPPED** scope (THE BAR).
- **NOT a multi-service / universal twin.** Each twin is **per dependency** ("Repeat per dependency",
  README:468; "build per-dependency twins", README:204). C44 is one service's clone; a cross-service twinning
  platform is out of scope.
- **NOT the scenario/judge tier.** Scenarios (C30) *choose to run against the twin* and the judge (C32) scores
  trajectories; C44 only *answers like the dependency*. C44 does not select which scenario runs against a twin
  (README:499 — that is the scenario's choice; cf. C31:OQ-5).
- **NOT the tool-node ABI or pack format.** The subprocess wire protocol + bundle format is **C02**; the
  workflow-engine tool-node abstraction is **C17**. C44 is *delivered as* a C17 tool node in a pack; it does
  not define that contract (inventory C17/C02; C44 depends on C17).
- **NOT a production-state mutator.** The twin holds *its own* state; it never writes to the real dependency
  (that is the entire point — README:195/468, isolation from production).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Dependency (sole) | **C17** Tool-node abstraction | C44 is exposed to formulas/molecules + the agent as a **C17 tool node** (the unified deterministic-step interface), placed via a per-twin `[[service]]` block (README:200, 202). Inventory C44 "Depends on: C17". |
| Packaging substrate | **C02** Pack/tool-node ABI | The per-twin Go binary (README:202) is shipped + invoked as a subprocess tool node over the C02 wire ABI (C17 is realized over C02). *Transitive via C17; not a direct C44 edge.* |
| Verifier (sibling, same batch) | **C45** Twin contract & fidelity verification | C45 verifies this twin's behavior matches the real service and its usage matches service promises (G22). C44 **provides** the twin + the declared cloned-surface contract C45 checks against. C45 depends on C44 (inventory C45). *Not on disk yet.* |
| Isolator (consumer, same batch) | **C43** Isolation & lethal-trifecta boundary | C43 uses this twin to bound blast radius (typed Bash/net/fs; production-scissors-by-declaration), G31, per D-13. C43 depends on C44 (inventory C43). C44 **provides** the standalone twin C43 isolates behind. *Not on disk yet.* |
| Consumers (run target) | **C30/C31** Scenario store + runner | Scenarios run "thousands per hour without rate limits" *against the twin* (README:195); the scenario/runner selects the twin as run target (README:499; C31:OQ-5). C44 is the addressable target, not the selector. |
| Transfusion exemplar | **LocalStack** (`github.com/localstack/localstack`, Apache 2.0) | The "Strongest Layer 5 gene-transfusion target" (AI-CONTEXT §7 line 345; §15.1 line 644). Pattern: clone a service from its SDK/contract. Recorded `transfused_from` per C51. |
| OSS engines (off-the-shelf, reused) | VCR.py/go-vcr/HoverFly; WireMock/Mountebank/Mockoon; Prism/Stoplight | The record/replay, stateful-mock, and OpenAPI-mock engines C44 composes — permissive (MIT/Apache 2.0), reused not reimplemented (README:199–200; AI-CONTEXT §7 lines 341–343; license hygiene → C57). |
| Discipline | **C51** Gene-transfusion | Every factory-built component transfuses ≥1 exemplar + records `transfused_from`; the twin transfuses LocalStack (README:204; C51). |

**Position in the system.** C44 is **Batch-4** (component-inventory line 113), **Phase 3c** — "factory builds
twins per critical dependency" (README:468), built *after* the substrate, scenarios/judge, and self-heal
mechanics are proven. It is **not foundational** (inventory C44): nothing in Batches 1–3 contracts against a
twin; it is a leaf the security tier (C43) and the fidelity invariant (C45) consume. Twins are built
**just-in-time per dependency — "After rate limits or production exposure bite"** (AI-CONTEXT §11.2 line 487),
so C44 is the *template* that the factory instantiates per dependency, not a single global service. It is
**feature-gated** by the per-twin `[[service]]` block (a twin exists only when its block is declared; README:200,
C03 section-presence-enables-capability model).

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete wire signatures / fixture formats / `[[service]]` TOML
schema / record-replay match rules defer to sweep 2 (and the tool-node ABI to C17/C02, the fidelity contract
to C45).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Twin tool-node endpoint** | inbound (call) | The agent/scenario calls the twin as a **C17 tool node** standing in for the real dependency — same request surface the real service exposes (README:200, 202). Reached via the per-twin `[[service]]` block. | C17 (abstraction), C02 (ABI), C44 (impl) |
| I2 | **Cloned-contract surface declaration** | outbound (contract) | The named slice of the real service this twin reproduces (endpoints/operations of its OpenAPI/SDK contract). The twin's *promise* — the artifact **C45 verifies against** and **C43 isolates behind**. | C44 (this); **C45** consumes (fidelity); **C43** consumes (isolation) |
| I3 | **Record/replay fixture I/O** | internal/data | Serve previously-recorded real-service traffic for matching requests (VCR.py/go-vcr/HoverFly "capture and replay"); capture-mode populates fixtures from real traffic. | C44 (this) |
| I4 | **Stateful-mock behavior** | internal | Custom-logic responses whose result depends on accumulated session state (WireMock/Mountebank/Mockoon "mock with custom logic"); the "stateful" half. | C44 (this) |
| I5 | **OpenAPI-driven mock** | internal | Contract-shaped responses to in-scope requests with no recorded fixture, driven by the service's OpenAPI spec (Prism/Stoplight). The fall-through that keeps the twin answering on-contract. | C44 (this) |
| I6 | **Twin session-state lifecycle** | internal/state | Initialize from seed/known-state, evolve within a run, reset between runs/scenarios (so each scenario sees a clean, deterministic twin). | C44 (this) |
| I7 | **`[[service]]` placement + config** | inbound (ops) | Per-twin Gas City `[[service]]` block (README:200): which service, fixture source, OpenAPI spec ref, mode precedence (replay→stateful→OpenAPI), reset policy. | C03 (config model), C44 (binding) |
| I8 | **Fidelity-observation hook** | outbound | Expose the twin's request/response trail (and a real-vs-twin diff seam) so **C45** can verify behavioral fidelity (AI-CONTEXT §7 line 347 "manual diff tooling"; README:201 contract verification). C44 *exposes*; C45 *judges*. | C44 provides; **C45** owns the bar |

**Invariants C44 must uphold (twin-construction level):**
- **INV-1 (on-contract within the declared surface):** for any request inside the declared cloned surface
  (I2), the twin returns a response that is **shape-valid against the service's OpenAPI/SDK contract** — via a
  recorded fixture (I3), stateful logic (I4), or the OpenAPI mock (I5), in that precedence. The twin never
  silently returns a non-contract-shaped body for an in-scope request. *(Whether the response is behaviorally
  faithful — the right value, not just the right shape — is **C45's** bar, G22; C44 guarantees on-contract +
  served-from-the-twin, not "indistinguishable from real".)*
  > [FAITHFUL-FILL] v4 names the three twin modes (README:199–200; AI-CONTEXT §7 341–343) but does not state
  > their **precedence**. **replay → stateful → OpenAPI-mock** is the minimal faithful ordering: a recorded
  > real interaction is the highest-fidelity answer (closest to truth), custom stateful logic covers
  > session-dependent behavior recording can't, and the OpenAPI mock is the on-contract fall-through so the twin
  > never goes off-contract. This is the LocalStack-shaped layering (specific recorded/programmed behavior first,
  > generic contract behavior last); the exact match/merge rule is sweep-2 (OQ-2).
- **INV-2 (no production reach):** the twin **never** calls or mutates the real dependency in serve-mode; it is
  a closed stand-in. The whole P7 value — "scenarios run thousands per hour without rate limits" and isolation
  from production — rests on this (README:195/468). *(Capture-mode (I3) MAY touch the real service to record
  fixtures; that is an explicit, separate, offline mode — never the serve path. Enforcing that the agent
  *cannot bypass the twin to reach production* is **C43's** boundary, G31, D-13 — C44 only guarantees the twin
  itself does not reach out while serving.)*
- **INV-3 (deterministic per run / resettable):** given the same fixtures + seed state, the twin produces the
  same responses for the same request sequence within a run, and **resets to a known state between
  runs/scenarios** (I6). This is what lets a held-out scenario suite run repeatably against the twin and what
  makes the twin usable as "external truth" (F-MODE F55 line 78).
  > [FAITHFUL-FILL] v4 does not state reset semantics, but "scenarios run thousands per hour" (README:195) plus
  > scenarios as repeatable evaluation (README:499) imply each scenario must see a clean, deterministic twin;
  > per-run reset to seed state is the minimal choice that makes scenario runs independent and reproducible.
- **INV-4 (the twin is a C17 tool node, not a fork):** the twin is delivered + invoked over the C17/C02
  tool-node contract (a per-twin Go binary in a pack, README:202) — **no Gas City Go import**, **no custom
  twin framework**. The off-the-shelf engines (I3–I5) are reused as-is (README:199–200).
- **INV-5 (declared-surface honesty):** a request **outside** the declared cloned surface (I2) is answered with
  an explicit "out-of-scope / not-cloned" signal — **never faked**. A twin must not pretend to clone what it
  does not, or fidelity (C45) and isolation (C43) reason over a false surface.
  > [FAITHFUL-FILL] v4 gives no out-of-scope behavior; fail-explicit (not silent fake) is the minimal choice
  > that keeps the cloned-surface contract (I2) truthful for the consumers (C45/C43). Whether out-of-scope
  > **blocks** the run or **degrades** depends on C43's isolation policy (deferred, G31).
- **INV-6 (license + provenance hygiene):** the composed engines are permissive (MIT/Apache 2.0) and the
  LocalStack transfusion is recorded (`transfused_from`, C51); license vetting rolls up to C57. No
  copyleft-contaminated engine enters a twin binary.

## 4. Data model / state

C44 *owns the twin's fixtures + session state*; the **tool-node ABI** is C17/C02's, the **fidelity bar** is
C45's, the **isolation policy** is C43's. State C44 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Cloned-surface declaration** | The named in-scope slice of the real service's OpenAPI/SDK contract this twin reproduces (I2). The twin's promise. | Per-twin pack artifact (versioned with the twin). | C44; consumed by C45 (fidelity), C43 (isolation) |
| **Record/replay fixtures** | Captured real-service request/response traffic the replay layer (I3) serves. | Per-twin fixture store in the pack (file-based, VCR-cassette-shaped). | C44 |
| **OpenAPI spec reference** | The service's OpenAPI/SDK contract that drives the OpenAPI mock (I5) + bounds the declared surface (I2). | Per-twin pack artifact (vendored spec). | C44 (binds); the service vendor (authors) |
| **Twin session state** | The dependency state the stateful layer (I4) evolves within a run; seeded, mutated, reset per run (I6/INV-3). | In-memory per run; seed/known-state in the pack. | C44 |
| **Per-twin `[[service]]` config** | Service id, fixture source, OpenAPI ref, mode precedence (replay→stateful→OpenAPI), reset policy, capture-vs-serve mode (I7). | Pack TOML (C03 model). | C03 (model), C44 (binding) |
| **Fidelity-observation trail** *(exposed, not owned)* | The twin's request/response trail + real-vs-twin diff seam (I8) — **surfaced for C45**, which owns the comparison. | Transient / emitted; the *bar* lives in C45. | C44 exposes; **C45** owns |

> [FAITHFUL-FILL] v4 specifies the twin *capability set* (record/replay + stateful + OpenAPI mock, LocalStack-
> shaped) but not its on-disk state layout. The minimal faithful set is **fixtures + seed/session-state +
> cloned-surface declaration + vendored OpenAPI spec** — exactly the inputs the three named modes (README:199–
> 200) need and the declared surface the two consumers (C45 fidelity, C43 isolation) require. Concrete fixture
> format (cassette schema), the OpenAPI-mock wiring, and the `[[service]]` TOML schema are sweep-2 (OQ-4); the
> off-the-shelf engines largely dictate them, which is the point of reuse.

**Consistency / lifecycle.** A twin is **authored per dependency** in Phase 3c (README:468), instantiated when
"rate limits or production exposure bite" (AI-CONTEXT §11.2 line 487). Its fixtures + seed state are
**versioned with the twin pack** (so a twin is reproducible and a fidelity result, C45, is attributable to a
specific twin version). Session state is **per-run and reset** (INV-3). The twin is **declarative-config-gated**
by its `[[service]]` block (C03). The authoritative behavior of the *real* service is external; the twin is a
**versioned, resettable clone of a declared slice of it** — which is exactly what lets C45 ask "how close" and
C43 ask "is the agent held behind it".

## 5. Behavior

**Author a twin (Phase 3c, per dependency).** Pick the dependency; declare the cloned surface from its
OpenAPI/SDK contract (I2); capture real traffic into fixtures (I3 capture-mode); seed the stateful layer (I4)
and point the OpenAPI mock (I5) at the vendored spec; transfuse the LocalStack assembly pattern (C51); ship as
a per-twin Go binary in a pack with a `[[service]]` block (I7; README:200, 202). C45 then verifies it; C43 then
isolates behind it.

**Serve a request (steady state, in a scenario run).**
1. **Receive** (I1): the agent/scenario calls the twin's tool-node endpoint with a request shaped like the real
   dependency's.
2. **Scope check** (I2/INV-5): if the request is **outside** the declared cloned surface → explicit
   out-of-scope signal (never faked); else continue.
3. **Resolve by precedence** (INV-1): **replay** (I3, a matching recorded fixture) → else **stateful** (I4,
   custom logic over current session state) → else **OpenAPI mock** (I5, an on-contract synthetic response).
4. **Update state** (I6): apply any state mutation the interaction implies (so the next call in the run sees
   it — the "stateful" guarantee).
5. **Answer + observe** (I1/I8): return the on-contract response; surface the request/response on the
   fidelity-observation hook for C45. **Never touches the real service in this path** (INV-2).

**Reset (between runs/scenarios).** Session state resets to seed/known-state (I6/INV-3) so each scenario sees a
clean, deterministic twin — enabling "thousands per hour" repeatable runs (README:195/499).

**Capture (offline, explicit).** In capture-mode (I3), the twin records real-service traffic into fixtures.
This is the **only** mode that may reach the real dependency, and it is offline/explicit — never the serve
path (INV-2).

> Sequence/state diagrams (Mermaid), the record-replay request-match algorithm, the precedence/merge rule
> between the three modes, the cassette/fixture schema, the `[[service]]` TOML schema, and the
> session-state model are **sweep-2+**. The tool-node wire contract is **C17/C02**; the fidelity comparison is
> **C45**; the isolation/blast-radius enforcement is **C43**.

## 6. Failure modes & handling

C44 carries the **C44-local half** of the two assigned gaps (G22 twin fidelity, G31 twin isolation); the
verification half of G22 is **C45's** and the enforcement half of G31 is **C43's** per **review-log D-13**.

**G22 (major) — digital-twin fidelity has no acceptance contract. C44-LOCAL PART ADDRESSED; VERIFICATION
DEFERRED TO C45.**
> [AMBIGUITY: G22] v4 marks F12/F33/F44/F56 **Addressed** "on the basis of twins that don't yet exist and have
> no fidelity bar" (ambiguities-and-gaps G22), and lists "Behavioral fidelity testing: None turnkey / DIY /
> Manual diff tooling" (AI-CONTEXT §7 line 347) with **no** "how close is close enough" definition. Two readings
> of where the fidelity bar lives: **(a)** C44 (the twin) owns its own fidelity bar; **(b)** fidelity
> verification is a **separate** capability/component. **Chosen: (b) — C45 owns the fidelity bar; C44 owns the
> twin behavior + the declared cloned-surface contract C45 verifies against.** This is the reading most
> consistent with the rest of v4: the inventory makes C45 (`twin-fidelity`, "Verifies twin usage matches service
> promises and twin behavior matches the real service; needs a 'how close is close enough' bar") a **distinct
> component depending on C44** (inventory C45, gap G22); README:201 lists "Contract verification … verify usage
> matches service promises" as a **separate row** from the twin itself; README:499 ("The twins' scenarios verify
> behavioral fidelity against the real service") frames fidelity as a *scenario/verification* activity, not a
> twin-internal property. **C44-local discharge of G22:** C44 makes fidelity *checkable* — it (i) **declares the
> cloned surface** (I2) so there is a concrete contract to verify against, (ii) guarantees **on-contract
> responses within that surface** (INV-1) and **explicit out-of-scope honesty** (INV-5) so the surface is
> truthful, and (iii) **exposes the request/response + real-vs-twin diff seam** (I8) C45 needs. The **"how close
> is close enough" bar, the diff tooling, and the pass/fail verdict are C45's** (G22 → C45). OQ-1 records the
> residual for the integrator. *(C45 is the same batch and is **on disk, sweep-1**; its §1/§3 confirm it
> "owns the fidelity predicate (the bar) … does not build the twin (C44)" — so this binding is cross-checked
> against the written sibling, not merely asserted from C44's side. C45's recorded fidelity *reference* may
> consume C44's record/replay capture (I3) — C45:OQ-C45-2.)*

**G31 (blocker) — lethal trifecta "Addressed" but twins (the mechanism) unbuilt + last. C44-LOCAL PART
ADDRESSED; ISOLATION/ENFORCEMENT DEFERRED TO C43.**
> [AMBIGUITY: G31] v4 marks F12/F44/F56 **Addressed** via twins, but "from Phase 0 through Phase 3b the factory
> runs Claude Code with Bash/network/filesystem access and **no twin isolation**" (ambiguities-and-gaps G31);
> F44 names a "substrate default: twins for everything; production scissors require explicit declaration per
> pack" (F-MODE-COVERAGE line 56). Two readings of where the **isolation/blast-radius** duty lives: **(a)** C44
> (the twin) enforces that the agent is held behind it; **(b)** a **separate** isolation boundary enforces it
> using the twin. **Chosen: (b) — C43 owns lethal-trifecta blast-radius bounding + twin isolation; C44 builds
> the twin C43 isolates behind.** This is **binding per review-log D-13** ("C43 owns the distinct lethal-trifecta
> blast-radius bound (Bash/net/fs typing, twin isolation; G31)") and matches the inventory (C43
> `isolation-boundary`, gap G31, **depends on C44**; C44 gap G31 is the *construction* half). **C44-local
> discharge of G31:** C44 provides the **prerequisite for isolation** — a twin that (i) is a **closed stand-in
> that never reaches production while serving** (INV-2), (ii) presents the **same call surface as the real
> dependency** (I1) so substituting it requires no agent-visible change, and (iii) **declares its cloned
> surface** (I2) so C43 knows exactly what the agent can be safely confined to. **The boundary typing
> (Bash/net/fs), the "production-scissors-by-declaration" default (F44), and the actual blast-radius bound are
> C43's** (G31 → C43). Until C43 lands, twins are *available* but isolation is **detection/opt-in only** — the
> honest Phase-0..3b posture (XC-8 parallel: "prevention" claims are detection until C43). OQ-1 records the
> residual. *(C43 is the same batch and is **on disk, sweep-1**; its §1/§3 confirm "C43 OWNS the … blast-radius
> bound … routes `twin`-typed surfaces to C44 twins" and that the twin-by-default *routing* is C43's, not C44's
> — so this deferral is cross-checked against the written sibling, not merely asserted from C44's side.)*

**Other failure cases (twin-construction level).**
- **No matching fixture + no stateful rule, in-scope request** → fall through to the **OpenAPI mock** (I5,
  INV-1); the twin stays on-contract rather than erroring. *(That the *value* may be low-fidelity is C45's to
  flag, G22.)*
- **Out-of-scope request** (INV-5) → explicit out-of-scope signal, never a fabricated response.
- **Stale fixtures (real service drifted)** → the twin keeps serving the recorded behavior; **detecting drift
  vs the real service is C45's fidelity job** (G22), not C44's. C44's obligation is fixture **versioning** so a
  drift finding is attributable.
- **Twin crash / unavailable** → surfaces as a tool-node failure over the C17/C02 contract (handled by the
  normal tool-node failure path); C44 adds no special durable queue. *[FAITHFUL-FILL]: v4 silent; defer to the
  C17 tool-node failure contract — the minimal non-inventing choice.]*
- **Capture-mode touching production** → explicit, offline, opt-in only; never the serve path (INV-2). Whether
  capture is *permitted at all* in a given environment is an isolation-policy (C43) call.

> F-mode applicability is owned by **C57** (coverage map). C44 *underwrites* the twin half of F12/F33/F44/F56
> (F-MODE-COVERAGE §4) and F55 ("twins as external truth", line 78) by **providing the clone**, but those modes
> move from "Addressed on paper" to actually-addressed only once **C45 verifies fidelity** (G22) **and C43
> enforces isolation** (G31). C44 surfaces the construction-level failure classes (off-contract serve, stale
> fixtures, out-of-scope, production reach) and defers the canonical F-mode mapping to C57.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** The twin's **reason for being is security**: bound the lethal trifecta by keeping the agent off
  the real dependency (F12/F44/F56). But **C44 alone does not deliver that security** — it provides a closed
  stand-in (INV-2) and the same call surface (I1); the *enforcement* that the agent **must** use the twin and
  cannot bypass it is **C43's** (G31, D-13). Capture-mode is the one production-touching path and is
  offline/opt-in. Fixtures may contain sensitive recorded payloads (real request/response bodies) — they
  inherit the **G37 secret/exposure thread** (deferred to the config/secrets owner; flagged).
- **Cost.** The twin is the **cost lever** for P7: "scenarios run thousands per hour without rate limits"
  (README:195) — running against the twin avoids the real dependency's rate limits and fees. (Note G34: this
  relieves the *dependency*-side limit only; the coder/judge Max-seat ceiling is unaffected — out of C44 scope.)
  Build cost is the labor v4 flags as "the most labor-intensive principle" (README:204) — minimized here by
  **reusing off-the-shelf engines** and transfusing LocalStack, not building a framework.
- **Scale.** A twin must serve high request volume (thousands/hour) deterministically; the off-the-shelf
  stateful/replay engines carry this. **Per-service** scope (README:468) keeps each twin bounded; there is no
  universal-twin scaling problem because there is no universal twin.
- **Observability.** The twin's request/response trail + a real-vs-twin diff seam (I8) is the key signal — it
  is **what C45 consumes** to verify fidelity (AI-CONTEXT §7 line 347 "manual diff tooling"). Surfacing it also
  lets ops see which requests fell through to the OpenAPI mock (a low-fidelity-risk indicator C45 acts on).
- **Ops.** Per-twin Go binary in a pack, placed via a `[[service]]` block (README:200, 202), built
  just-in-time per dependency (AI-CONTEXT §11.2 line 487). Fixtures + OpenAPI spec are **vendored + version-
  pinned with the twin** so behavior is reproducible and fidelity results (C45) are attributable to a twin
  version. License hygiene of the composed engines rolls up to **C57**.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2). C44's ACs cover **twin construction + contract
surface**; **fidelity ACs are C45's**, **isolation ACs are C43's**.

1. **AC-1 (twin answers like the dependency — I1/INV-1):** a request inside the declared cloned surface returns
   an **on-contract** response resolved by replay→stateful→OpenAPI precedence; the caller reaches the twin via
   the C17 tool-node endpoint with no agent-visible change vs the real service (README:199–202).
2. **AC-2 (record/replay — I3):** a request matching a recorded fixture returns the recorded real response;
   capture-mode populates fixtures from real traffic (offline) (README:199; AI-CONTEXT §7 line 341).
3. **AC-3 (stateful behavior — I4/I6):** a multi-step interaction where a later response depends on earlier
   calls behaves like the real service *within a run* (the "stateful" guarantee) (AI-CONTEXT §7 line 342).
4. **AC-4 (OpenAPI fall-through — I5/INV-1):** an in-scope request with no fixture and no stateful rule returns
   an **on-contract** synthetic response (never off-contract, never an error) (AI-CONTEXT §7 line 343).
5. **AC-5 (deterministic + reset — INV-3/I6):** the same request sequence yields the same responses within a
   run; state resets between runs/scenarios, so repeated scenario runs are reproducible (README:195/499).
6. **AC-6 (no production reach in serve-mode — INV-2):** with the real dependency made **unreachable**, the
   twin still serves every in-scope request from fixtures/stateful/OpenAPI — proving the serve path never calls
   production (README:195/468). *(This is the prerequisite C43 builds its blast-radius bound on; the *bound* is
   C43's AC.)*
7. **AC-7 (declared-surface honesty — I2/INV-5):** an out-of-scope request returns an explicit "not-cloned"
   signal, never a fabricated response; the declared cloned surface (I2) is queryable and matches actual twin
   coverage.
8. **AC-8 (C17 tool node, no fork — INV-4):** the twin is delivered + invoked as a C17/C02 tool node (per-twin
   Go binary in a pack, `[[service]]` block) with **no Gas City Go import** and **no custom twin framework**;
   the off-the-shelf engines are reused (README:200, 202, 204).
9. **AC-9 (fidelity seam exposed — I8, hands off to C45):** the twin exposes a request/response + real-vs-twin
   diff seam C45 can consume; **C44 does not assert a fidelity verdict** (that AC is C45's, G22).
10. **AC-10 (isolation seam exposed — I1/I2, hands off to C43):** the twin presents the real dependency's call
    surface and declares its cloned surface, such that C43 can substitute + confine the agent behind it; **C44
    does not assert the blast-radius bound** (that AC is C43's, G31, D-13).

**Test strategy.** A **per-twin conformance harness** that (a) drives AC-1…AC-8 against one concrete twin (the
twin of a chosen dependency) with the **real dependency made unreachable** (the AC-6 isolation-prerequisite
proof), and (b) exercises the three-mode precedence + reset. Fidelity (does the twin's *value* match real?) is
**C45's** suite consuming AC-9's seam; blast-radius (is the agent confined?) is **C43's** suite consuming
AC-10's seam. Because twins are per-service, the harness is the **template** the factory re-runs per
instantiated twin (README:468 "Repeat per dependency").

## 9. Open questions

- **OQ-1 (→ review-log, top): G22/G31 cross-component seams (C45 fidelity, C43 isolation) — sweep-2 joint freeze.**
  §6 binds, from C44's side, that **C45 owns the fidelity bar** (G22) and **C43 owns the isolation/blast-radius
  bound** (G31, per D-13), with C44 providing the twin + declared cloned-surface contract (I2) + fidelity seam
  (I8) + isolation-ready call surface (I1). Both siblings are the same batch and are **on disk (sweep-1) and
  already confirm this attribution** (C45 §1/§3 owns the fidelity predicate, not the twin; C43 §1/§3 owns the
  blast-radius bound + twin-by-default routing) — so OQ-1 is no longer "confirm the sibling is written" but
  **cross-check the concrete shape at the joint sweep-2 freeze**: the I2/I8 contract vs C45 §3 (incl. whether
  C45's recorded reference consumes C44's I3 capture, C45:OQ-C45-2), and the I1/I2 substitution contract vs C43
  §3, with C44 carrying **no** fidelity bar and **no** enforcement teeth confirmed against both.
- **OQ-2 (→ review-log): three-mode precedence + match/merge rule (G22-adjacent).** The
  replay→stateful→OpenAPI ordering (INV-1) is a FAITHFUL-FILL; the exact request-match rule (replay), the
  stateful-vs-replay merge, and when to prefer a stale fixture over a fresh OpenAPI mock interact with C45's
  fidelity bar. Freeze at sweep-2 with C45.
- **OQ-3 (→ review-log): twin session-state + reset granularity (INV-3).** Per-scenario vs per-run-step reset;
  seed-state source; whether one twin instance serves concurrent scenarios (state isolation) — interacts with
  C42 worktree/run isolation and the "thousands per hour" throughput claim. Sweep-2.
- **OQ-4: per-twin packaging schema — `[[service]]` TOML + fixture/cassette format (G29-adjacent).** The
  `[[service]]` block fields (README:200), the fixture-store layout, and the OpenAPI-spec vendoring are
  constrained by the off-the-shelf engines (VCR/WireMock/Prism) + the C02/C17 ABI; pick concrete schemas at
  sweep-2 (the reuse is the point — match the engines).
- **OQ-5: which engine per twin (record/replay + stateful + OpenAPI tooling choice).** v4 lists alternatives
  per mode (VCR.py/go-vcr/HoverFly; WireMock/Mountebank/Mockoon; Prism/Stoplight) but a per-twin Go binary
  (README:202) biases toward Go-native (go-vcr/HoverFly) + an embeddable mock; confirm per twin at instantiation
  (language of the dependency's SDK matters — README:199 "Per-language tool node"). Sweep-2 / per-instance.
