# C45 — Twin contract & fidelity verification  (Spec, canonical track)

> Source: README §"Principle 7 — Digital twins" (L193–204: L195 "Behavioral clones of critical external
> dependencies. Lets scenarios run **thousands per hour without rate limits**"; the 4-row table —
> **"Contract verification" = "Verify usage matches service promises" / "Pact (multi-language, MIT)" /
> "Gas City pack per service"** (L201); "Stateful HTTP twin … Per-twin Gas City `[[service]]` block" (L200);
> "Twin scaffolding from SDK = **No OSS** — bespoke per service, transfusion from LocalStack pattern …
> n/a (your work)" (L202); L204 "P7 is **the most labor-intensive principle** … No turnkey OSS for 'twin a
> service from its SDK'. Build per-dependency twins, gene-transfusing from LocalStack"); README §Phase 3c
> (L468 "factory builds twins per critical dependency … each twin is bounded engineering … follow the
> LocalStack-shaped pattern for a specific service's SDK **contract**"); README §"Scenarios drive
> evaluation" (**L499 "The twins' scenarios verify behavioral fidelity against the real service"**);
> README §"sparse" (L520 "Layer 5 (twins) is genuinely sparse … building twins is per-service engineering");
> AI-CONTEXT §6.2 Layer-5 capability table (L344 "Contract verification | **Pact, schemathesis** | MIT/MIT |
> Mature"; L343 "OpenAPI-driven mock | Prism, Stoplight"; **L347 "Behavioral fidelity testing | None
> turnkey | DIY | Manual diff tooling"**); AI-CONTEXT §13 decision table (L487 "Whether to build twins
> (Layer 5) for which dependencies | After rate limits or production exposure bite | **Just-in-time per
> dependency**"); AI-CONTEXT §14 risk register (L620 "Layer 5 twin work doesn't transfer well | … LocalStack
> is the strong exemplar; budget per-service work"); F-MODE-COVERAGE §4 (**F12 "Lethal trifecta" /
> F33 "Adversarial-prompt defeat of LLM-judge" / F44 "Lethal-Trifecta Production-Scissors Default" /
> F56 "Guardrail-bypass under stress" — all "Addressed" on the strength of twins** that "remove the
> deploy-to-production vector" / "isolate the agent from production entirely"); F-MODE-COVERAGE §6 (F55
> "Behavioural drift … signed scenarios + twins as **external truth**" — "Partial"); F-MODE-COVERAGE §9
> (F3 "Spec-completeness fallacy" / F13 "Missing-config blindspot" — "Twins (P7) … partially compensate by
> checking against environment-wide behavior. **Residual gap**"); component-inventory C45 row (subsystem
> Digital Twins; **kind: invariant**; "Verifies twin usage matches service promises **and** twin behavior
> matches the real service; **needs a 'how close is close enough' bar**"; maps A63/A64b/B66; depends on
> **C44, C30**; gap **G22**; foundational: no; Batch 4); ambiguities-and-gaps **G22** (major — "Digital-twin
> fidelity has no acceptance contract … no definition of *how close is close enough* for a twin, yet
> F12/F33/F44/F56 are all marked Addressed on the basis of twins that don't yet exist and have no fidelity
> bar"); review-log **D-6** (canonical track); SURVIVOR-PASS C43-07 ("boundary_class tag
> (production/twin/isolated) → **DROP** … we don't have twins yet") and SURVIVOR-PASS C04-02 ("ResumeToken
> **with fidelity contract** → DROP … we don't add a fidelity-contract layer" — a *different* fidelity
> contract, noted to disambiguate).
> Inventory ID: C45   Kind: invariant   Status: sweep-1
> Track: canonical

## 1. Purpose & responsibility

C45 is the **twin-fidelity invariant**: it is the piece that makes Principle 7's claim — that a digital
twin (C44) is a faithful enough stand-in for a real external dependency that scenarios can "run **thousands
per hour without rate limits**" against the twin instead of production (README:195) — *checkable*, by
defining and enforcing the **"how close is close enough" bar** (G22) and wiring the two verifications that
back it. Per the inventory one-liner, C45 verifies **both** directions of the twin↔service relationship: (a)
**twin-usage-vs-service-promises** — that the agent's *use* of the twin honours the real service's published
contract (README:201 "Verify usage matches service promises", Pact-shaped), so a twin cannot silently
license usage the real service would reject; and (b) **twin-behavior-vs-real-service** — that the *twin's
own behaviour* matches the real service within an accepted tolerance (README:499 "the twins' scenarios
verify behavioral fidelity against the real service"). C45 is **kind: invariant** (inventory), not a
service: it owns the **fidelity predicate** (the bar) and the **gate** that asserts the invariant, not the
twin (C44) and not the scenarios (C30).

C45 exists because **G22 is the genuine unsolved deliverable**. v4 names mature OSS for the *contract-
verification technique* — **Pact / schemathesis** ("Contract verification — Verify usage matches service
promises", README:201, AI-CONTEXT:344; schemathesis being the OpenAPI-conformance/property tester) — but for
the *behavioural-fidelity diff* and the actual *acceptance bar* it says **"Behavioral fidelity testing | None
turnkey | DIY | Manual diff tooling"** (AI-CONTEXT:347). (Prism, AI-CONTEXT:343, is an OpenAPI-driven **mock**
— C44's twin-construction surface, a *subject* of verification, **not** a C45 conformance checker.) The
over-build trap is to re-build the contract-testing tooling the stack already provides; the genuine KEEP is
the **definition of
"close enough"** — the fidelity predicate over a fidelity-probe corpus, plus the wiring that gates a twin as
fit-for-substitution — which no OSS supplies. F-MODE-COVERAGE §4 marks **F12/F33/F44/F56 "Addressed" purely
on the strength of twins** that "remove the deploy-to-production vector"; without C45's bar those four
"Addressed" cells rest on twins of *unknown* fidelity (G22), which is exactly the gap C45 closes.

> [FAITHFUL-FILL] **C45 is the fidelity *bar + gate*, not a new contract-testing engine.** Per the
> capability-for-principle bar, contract verification (**Pact / schemathesis**, README:201/AI-CONTEXT:344 —
> schemathesis = OpenAPI conformance) and HTTP record/replay **reference capture** (VCR/go-vcr/polly,
> README:199 "capture and replay") are **mature stack tooling C45 *invokes*, not custom code C45 *writes***.
> The two things v4 says have **no turnkey OSS** are the *behavioural-fidelity diff* and the *fidelity bar
> itself* — "Behavioral fidelity testing | None turnkey | DIY | Manual diff tooling" / "how close is close
> enough" (G22; AI-CONTEXT:347). So the tolerance-scored **behaviour diff/compare over the recorded reference
> is part of C45's DIY KEEP**, not an off-the-shelf engine (record/replay supplies the reference + replay, not
> the compare). (Prism, AI-CONTEXT:343, is an OpenAPI-driven *mock* — C44's twin surface, not a C45 verifier.)
> The minimal faithful reading of C45's "invariant" (inventory kind)
> is therefore: C45 **owns the fidelity predicate** (the threshold + the probe-corpus contract that defines
> "close enough" per twin) and **owns the verification wiring** (run the contract check + the
> behaviour-diff, combine them against the predicate, emit a pass/fail fidelity verdict). C45 does **not**
> build a Pact replacement, a schema-diff library, or a new mocking runtime, and does **not** build the twin
> (C44) or the scenarios (C30). The custom KEEP is small — the predicate definition + the combine-and-gate
> wiring — matching "build per-dependency twins … bounded engineering" (README:468/520).

**Responsibilities**
- **Define the fidelity predicate — the "how close is close enough" bar (G22, the genuine KEEP).** C45
  owns, per twinned service, the **acceptance predicate** that decides whether a twin is fit to substitute
  for the real service: which dimensions are checked (contract conformance + behavioural match), the
  **tolerance** on each (exact vs bounded — e.g. error taxonomy must match exactly, latency/ordering within
  a stated band), and the **probe corpus** the predicate is evaluated over. This is the artifact v4 says has
  no OSS (AI-CONTEXT:347) and the inventory says C45 "needs" (the "how close is close enough" bar).
- **Verify twin-usage-vs-service-promises (contract half — A63/README:201).** C45 runs the **contract
  verification** that the agent's usage of the twin conforms to the real service's published contract
  (**Pact / schemathesis**, README:201/AI-CONTEXT:344 — schemathesis providing OpenAPI conformance/property
  testing), so a twin cannot accept a request shape, auth, or response the real service would reject. The
  *tool* is stack OSS; C45 owns *that the check runs and feeds the predicate*.
- **Verify twin-behavior-vs-real-service (behaviour half — README:499).** C45 runs the **behavioural
  fidelity check**: the twin's responses over the fidelity-probe corpus are compared against a **reference**
  of real-service behaviour (recorded interactions / golden responses — record/replay, README:199), and the
  diff is scored against the predicate's tolerance. This is the "twins' scenarios verify behavioral fidelity
  against the real service" check (README:499), driven by C30's fidelity-probe scenarios.
- **Assert the fidelity invariant + emit a fidelity verdict.** As an *invariant* (inventory kind), C45's
  output is a per-twin, per-version **`fidelity_pass | fidelity_fail`** verdict with the failing dimensions,
  published so downstream can act: a twin that has **not** passed C45 is **not certified for substitution**
  in scenario runs (C31) or as a dependency stand-in (C43). C45 is the observability + gate surface that
  makes F12/F33/F44/F56's "Addressed" honest (G22).
- **Consume C44's twin + C30's fidelity-probe scenarios.** C45 reads the twin under test (C44) and the
  **fidelity-probe corpus** authored as scenarios in C30 (README:499). It does not author probes (C30) or
  build/run the twin (C44).

**Explicitly NOT**
- **NOT the digital twin itself (C44).** C44 builds the per-service behavioural clone (record/replay +
  stateful + OpenAPI mock, LocalStack-shaped, README:200/202; inventory C44). C45 **verifies** C44's output
  against the bar; it does **not** build, host, or run the twin. (Inventory: C45 `depends on C44`.)
- **NOT the scenario store / probe authoring (C30).** C30 owns the Inspect-AI scenario DSL and stores the
  fidelity-probe scenarios in the isolated rig (README:499 "the twins' scenarios"; inventory C30). C45
  **consumes** the probe corpus to evaluate the predicate; it does not author or store scenarios. (Inventory:
  C45 `depends on C30`.)
- **NOT a new contract-testing / schema-diff / mocking engine (bar — the over-build trap).** **Pact /
  schemathesis** (contract verification, README:201/AI-CONTEXT:344) and **HTTP record/replay** (reference
  capture + replay, VCR/go-vcr/polly, README:199) are **mature OSS** that C45 **invokes**; **Prism**
  (AI-CONTEXT:343) is an OpenAPI-driven *mock* belonging to C44's twin, not a C45 tool. C45 does **not**
  re-implement contract testing or record/replay capture; building any of those is polish/what-the-stack-
  already-does → **DROP** (capability-for-principle bar). C45's only custom surface is the **fidelity
  predicate + the tolerance-scored behaviour diff + the combine-and-gate wiring** — the parts v4 says have no
  turnkey OSS ("Manual diff tooling / DIY", AI-CONTEXT:347).
- **NOT the isolation / lethal-trifecta boundary (C43).** C43 owns the deterministic boundary typing and
  twin *isolation* that bounds blast radius for Bash/network/fs access (G31; inventory C43). C45 establishes
  *whether a twin is faithful enough to substitute*; C43 establishes *that the agent is confined to the twin
  and cannot reach production*. Distinct concerns: C45 = fidelity of the stand-in; C43 = confinement to the
  stand-in. C45 does **not** absorb C43's boundary job. (Note: the `boundary_class` production/twin/isolated
  tag is **DROPPED** — SURVIVOR-PASS C43-07 — so C45 does not key off such a tag.)
- **NOT a resume/state fidelity contract (disambiguation).** SURVIVOR-PASS C04-02 dropped a *ResumeToken
  "fidelity contract"* — that is **session-resume** fidelity (KV-cache/continuity), a **different** concept;
  C45's fidelity is **twin↔real-service behavioural** fidelity (README:499). Named only to prevent
  conflation; C45 does not touch resume.
- **NOT a real-service oracle / live-traffic interceptor.** C45 does **not** call the real production
  service as part of the substrate loop to get ground truth at run time (that would defeat the
  "thousands per hour without rate limits / no production exposure" purpose, README:195, F44/F56). The
  reference is a **recorded/golden** corpus captured out-of-band (record/replay, README:199); how and how
  often the reference is refreshed against the real service is **OQ-C45-2**.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (declared dep) | **C44** Digital twin (per service) | C44 builds the per-service behavioural clone (record/replay + stateful + OpenAPI mock, README:200/202). C45 reads the **twin under test** (its endpoint + the service contract/OpenAPI it claims to honour) to run both verifications. Inventory: C45 `depends on C44`. |
| Upstream (declared dep) | **C30** Scenario authoring & store | C30 authors + stores the **fidelity-probe corpus** as scenarios (README:499 "the twins' scenarios verify behavioral fidelity"). C45 consumes the probe set to drive the behaviour-diff and the predicate evaluation. Inventory: C45 `depends on C30`. |
| Upstream (verification tooling) | **C17** Tool-node abstraction · **C02** Pack ABI | > [FAITHFUL-FILL] — **not a declared inventory edge**; faithful fill. The contract check (Pact/schemathesis) and the OpenAPI/record-replay diff run as **Gas City pack tool nodes** ("Gas City pack per service", README:201; "Per-language tool node", README:199), which is C17/C02's surface. C45 packages its checks as tool nodes; it does not redefine the ABI. |
| Upstream (probe→twin run target) | **C31** Scenario runner | > [FAITHFUL-FILL] — faithful fill. Executing the fidelity-probe corpus against the twin is a *scenario run*; C31 is the Inspect-AI runner (inventory C31). Whether C45 invokes C31 to drive probes at the twin, or runs probes directly as a pack, is **OQ-C45-3** (mirrors C31:OQ-5 run-target selection). |
| Downstream (substitution gate) | **C31** Scenario runner · **C43** Isolation boundary | C45's `fidelity_pass` is the **certification** that lets a twin substitute for the real service in scenario runs (C31) and as the confined dependency stand-in behind C43's boundary. A twin that fails C45 is **not** certified for substitution — so F12/F33/F44/F56's "twins not production" claim only holds for twins C45 passed. |
| Downstream (residual-risk register) | **C57** Failure-mode coverage map & residual-risk register | C57 owns the honest residual/caution register. C45 routes the **G22 caveat** — F12/F33/F44/F56 are "Addressed" *conditional on a passing fidelity verdict*, and any twin below the bar (or a stale reference, OQ-C45-2) is a **residual** — so "Addressed" is not over-trusted for an unverified twin. (F3/F13 already note the residual environment-surface gap; C57 owns it.) |
| Downstream (per-twin acceptance gate) | **C53 / C50** bootstrap-validation · promotion gate | > [FAITHFUL-FILL] — faithful fill. A factory-*built* twin (C44, Phase 3c) is itself a factory output; its `fidelity_pass` is a natural acceptance signal for the build's go/no-go (C53) — C45 supplies the fidelity dimension of "did the built twin work". C45 publishes; C53 consumes. |

C45 is **not foundational** (inventory: no) and is in **Batch 4** (alongside C43/C44 and the self-heal +
bootstrap mechanics — "factory builds factory"). Per AI-CONTEXT:487 twins are built **just-in-time per
dependency** ("after rate limits or production exposure bite"), so C45's predicate is likewise instantiated
**per twinned service**, not once globally. C45 is **load-bearing for the Layer-5 integrity claim**: per
F-MODE-COVERAGE §4 the entire weight of F12/F33/F44/F56's "Addressed" sits on twins being faithful enough to
replace production, and C45 is the *only* component that establishes whether that premise holds (G22).

## 3. Interfaces / contracts

Sweep 1 — interfaces **named and described**; the concrete fidelity-predicate schema, the contract-check
adapter contract, the behaviour-diff record schema, and the verdict bead schema are sweep-2 deliverables.

1. **Fidelity-predicate contract (the bar — the custom KEEP, G22).** The named artifact C45 owns: per
   twinned service, a **predicate** declaring (a) the **checked dimensions** — contract conformance
   (usage-vs-promises) + behavioural match (twin-vs-real); (b) the **tolerance per dimension** — exact-match
   dimensions (status/error taxonomy, response schema, auth semantics) vs **bounded** dimensions (latency
   band, ordering, numeric-field tolerance, allowed-omission set); (c) the **probe corpus** (from C30) the
   predicate is evaluated over; (d) the **pass rule** that combines per-dimension results into
   `fidelity_pass | fidelity_fail`. This is the "how close is close enough" definition the inventory says
   C45 "needs" and AI-CONTEXT:347 says has no OSS. (Sweep-1: named + its dimensions enumerated; the concrete
   tolerance schema is sweep-2.)
2. **Contract-verification check (twin-usage-vs-service-promises — A63/README:201).** A named check that
   the twin honours the real service's published contract: a **Pact** consumer-contract run or a
   **schemathesis** OpenAPI-conformance/property run (README:201/AI-CONTEXT:344), against the twin's endpoint.
   Input: the service contract/OpenAPI (from C44) + the agent's usage interactions. Output: a per-dimension
   **contract-conformance result** feeding the predicate. *Tool is stack OSS; C45 owns the wiring + the result
   mapping.* *(Prism, AI-CONTEXT:343, is an OpenAPI **mock** in C44's twin — a subject of this check, not the
   checker.)*
3. **Behavioural-fidelity check (twin-vs-real-service — README:499).** A named check that compares the
   **twin's responses** over the fidelity-probe corpus against a **reference** of real-service behaviour
   (recorded/golden interactions — record/replay, README:199), producing a **behaviour diff** scored against
   the predicate's tolerance. Output: a per-dimension **behaviour-match result** feeding the predicate. This
   is the check README:499 names; the *diff* is stack tooling, the *tolerance scoring* is C45's predicate.
4. **Fidelity verdict + report feed.** The named surface C45 publishes: per twin × version, a
   **`fidelity_pass | fidelity_fail`** verdict + a report of the failing dimensions and the margins. Emitted
   as a **bead** (the existing work-graph, C19/C20) consumable by C31/C43 (substitution gate), C57
   (residual-risk register — the G22 caveat), and C53 (twin-build acceptance). A `fidelity_fail` is also a
   natural **fix-task** candidate against the twin (C44/C39).
5. **Reference-capture note (OQ — not a frozen contract).** A one-line statement that the behavioural
   reference is a **recorded/golden corpus captured out-of-band** (record/replay, README:199), **not** a
   live production call in the substrate loop (preserves "no production exposure", F44/F56). The capture +
   refresh cadence (how the golden stays current as the real service evolves — drift) is **OQ-C45-2**.

**Invariants**
- **Fidelity invariant (the asserted invariant — inventory kind).** A twin is **certified for
  substitution** *iff* it has a current `fidelity_pass` against its predicate: contract conformance holds
  (usage-vs-promises) **and** behavioural match holds within tolerance (twin-vs-real) over the probe corpus.
  A twin without a current passing verdict is **not** a sanctioned production substitute — so the
  F12/F33/F44/F56 "twins not production" guarantee is **conditioned on this invariant** (G22).
- **Two-sided-verification invariant.** Fidelity requires **both** directions (inventory: "usage matches
  service promises **AND** behavior matches the real service"). A twin that conforms to the contract but
  diverges behaviourally (or vice-versa) is a **fidelity_fail**; neither half alone certifies.
- **Bar-is-explicit invariant (G22).** Every certified twin has an **explicit, recorded** predicate (the
  tolerances and the probe corpus), not an implicit "looks right". The bar must be a written artifact so a
  pass is auditable and a residual (twin below bar / stale reference) is discoverable in C57.
- **No-engine-rebuild invariant (bar).** C45 verifies using **stack tooling** for the parts the stack
  provides — **Pact / schemathesis** (contract verification, README:201/AI-CONTEXT:344) and **record/replay**
  reference capture (VCR/go-vcr/polly, README:199) — and contains **no** custom contract-testing engine,
  record/replay capturer, or mocking runtime. The custom code is the predicate + the **tolerance-scored
  behaviour diff** + the combine-and-gate wiring — the "Manual diff tooling / DIY" parts v4 says have no
  turnkey OSS (AI-CONTEXT:347).

## 4. Data model / state

C45 owns **the fidelity predicate (the bar), the fidelity verdicts, and the fidelity reports** it raises. It
does **not** own the twin (C44), the probe scenarios (C30), the contract-test tooling (stack OSS), or the
recorded reference corpus's *authoring* (captured via record/replay; home is OQ-C45-2).

### 4.1 Fidelity-predicate object (the bar — the owned definition, G22)

| Field | Meaning | v4 source |
|---|---|---|
| service / twin ref | which twinned service this predicate certifies (per-dependency, just-in-time) | README:468; AI-CONTEXT:487 |
| checked dimensions | the set verified: contract conformance + behavioural match (both required) | inventory C45 ("usage … AND behavior") |
| tolerance per dimension | exact-match set (status/error taxonomy, schema, auth) vs bounded set (latency/ordering/numeric/omission band) | AI-CONTEXT:347 (DIY); G22 |
| probe corpus ref | the C30 fidelity-probe scenarios the predicate is evaluated over | README:499 |
| pass rule | how per-dimension results combine into `fidelity_pass \| fidelity_fail` | G22 (the "how close" bar) |

### 4.2 Fidelity verdict + report (the owned instance state)

| Field | Meaning | v4 source |
|---|---|---|
| fidelity verdict | per twin × version: `fidelity_pass \| fidelity_fail` | inventory C45 (invariant); README:499 |
| contract result | usage-vs-promises conformance result (per dimension) | README:201 (Pact); AI-CONTEXT:344 |
| behaviour result | twin-vs-real behaviour diff scored vs tolerance (per dimension) | README:499; README:199 (record/replay) |
| failing dimensions + margins | on fail: which dimensions breached and by how much | G22; AI-CONTEXT:347 |

> [FAITHFUL-FILL] **Verdicts/reports are beads; the predicate is config; no new store.** v4 says behavioural
> fidelity testing is "DIY / Manual diff tooling" with no turnkey OSS (AI-CONTEXT:347) and the inventory
> kind is **invariant**, not data-store. The minimal faithful choice is that C45 **derives** verdicts from
> stack checks over C30 probes vs C44's twin and **raises verdicts/reports as beads** in the existing
> work-graph (C19/C20); the **predicate** is a per-service **config artifact** (kept under git review,
> alongside the twin's pack). C45 stands up **no new persistence store**. The concrete verdict/report bead
> types are a C20 schema-registry concern (sweep-2 seam), and the recorded **reference corpus** is captured
> via record/replay (README:199) whose storage home is OQ-C45-2.

### 4.3 Which tooling is authoritative for each half (bar — sweep-1 note, not a new framework)

> **Scope note (capability-for-principle bar).** This maps each verification half to the **stack tool** that
> performs it, to make explicit that C45 *invokes* rather than *rebuilds*. It is explanatory, not a new
> abstraction layer.

| Half | What it checks | Tool (stack OSS) | C45's custom part |
|---|---|---|---|
| usage-vs-promises | agent usage / twin responses conform to the real service contract | **Pact / schemathesis** — schemathesis = OpenAPI conformance (README:201/AI-CONTEXT:344) *(Prism, AI-CONTEXT:343, is an OpenAPI **mock** in C44's twin, not a verifier)* | wire the check; map result to the predicate dimension |
| twin-vs-real | twin behaviour matches recorded real-service behaviour over the probe corpus | **record/replay** reference capture + replay (VCR/go-vcr/polly, README:199); the **diff/compare** itself is DIY ("Manual diff tooling", AI-CONTEXT:347) | the **golden-compare + tolerance scoring** + the probe corpus (C30) |
| the bar | combine both into `pass\|fail` at a stated tolerance | **None turnkey — DIY** (AI-CONTEXT:347) | **the fidelity predicate (G22) — the genuine KEEP** |

### 4.4 Persistence & consistency

C45 holds **no new store**. The predicate is per-service config (git-reviewed); verdicts/reports are **beads**
(C19/C20); the reference is a recorded corpus (record/replay home, OQ-C45-2). C45's only consistency
requirement is that **a twin's certification is valid only against the twin version + contract version + probe
corpus + reference it was computed over** — i.e., a verdict is **keyed to those versions**, and a change to
the twin, the service contract, or the reference **invalidates** the prior `fidelity_pass` and requires
re-verification (so a drifted twin or a refreshed reference cannot silently keep stale certification —
related to OQ-C45-2 drift).

## 5. Behavior

C45's behaviour is **bar-definition** (config) + a **two-sided verification + gate** pass, run per twin (and
re-run on twin/contract/reference change):

- **Bar-definition time (the custom KEEP — G22).** For a twinned service, C45 declares the **fidelity
  predicate** — the checked dimensions, the tolerance per dimension (exact vs bounded), the C30 probe corpus,
  and the pass rule (§4.1). This is the explicit "how close is close enough" artifact (AI-CONTEXT:347).
- **Contract-check time (usage-vs-promises — README:201).** C45 runs the contract verification
  (**Pact / schemathesis**, README:201/AI-CONTEXT:344) of the twin against the real service's contract → a
  **contract-conformance result** per dimension.
- **Behaviour-check time (twin-vs-real — README:499).** C45 drives the C30 fidelity-probe corpus at the twin
  (C44) and diffs the twin's responses against the recorded reference (record/replay, README:199), scoring
  the diff against the predicate's tolerance → a **behaviour-match result** per dimension.
- **Gate time (assert the invariant).** C45 combines both results via the predicate's pass rule →
  **`fidelity_pass | fidelity_fail`** + the failing dimensions/margins. A `fidelity_pass` certifies the twin
  for substitution (C31/C43); a `fidelity_fail` blocks certification and is a fix-task candidate (C44/C39).
- **Publish time.** C45 emits the verdict + report **bead** to C31/C43 (substitution gate), C57
  (residual-risk register — the G22 caveat), and C53 (twin-build acceptance).

(Sequence/state diagrams for the verification pass and the version-invalidation logic are deferred to sweep 2
per BUILDER-BRIEF altitude.)

## 6. Failure modes & handling

| F-mode / gap | Relevance | Handling in C45 (faithful) |
|---|---|---|
| **G22** Digital-twin fidelity has no acceptance contract (major — **C45's core deliverable**) | "No definition of *how close is close enough* … F12/F33/F44/F56 Addressed on twins with no fidelity bar." | **Resolved (the genuine KEEP).** C45 **defines the fidelity predicate** — the explicit, per-service "how close is close enough" bar (checked dimensions + tolerance + probe corpus + pass rule, §4.1) — and **wires the two-sided verification** (contract + behaviour) that asserts it, emitting a `fidelity_pass\|fidelity_fail` verdict. The bar is a **written, version-keyed artifact** (auditable), and any twin below it (or a stale reference) is routed as a **residual** to C57 — so F12/F33/F44/F56's "Addressed" becomes *conditional on a passing verdict*, not an unverified assumption. The verification tooling is stack OSS — **Pact / schemathesis** (contract, README:201/AI-CONTEXT:344) + **record/replay** reference capture (README:199) — and the **only custom code is the predicate + the tolerance-scored behaviour diff + the gate wiring** (AI-CONTEXT:347 "Manual diff tooling / DIY"). |
| **F12** Lethal trifecta (F-MODE §4, "Addressed") | "scenarios use twins not production." | **Conditioned on C45 (faithful).** The "twins not production" substitution is only as safe as the twin is faithful; C45's `fidelity_pass` is what makes substituting the twin for production *justified*. C45 does **not** own the *isolation* that keeps the agent off production — that is **C43's** boundary (G31). C45 = the twin is faithful enough to substitute; C43 = the agent is confined to it. |
| **F33** Adversarial-prompt defeat of LLM-judge (F-MODE §4, "Addressed") | "twins remove the deploy-to-production vector." | **Conditioned on C45 (faithful).** Removing the production vector relies on the twin being a faithful stand-in; C45 certifies that. (Defeat of the *judge* itself is C32/C34/C43's concern, not C45's.) |
| **F44** Lethal-Trifecta Production-Scissors Default (F-MODE §4, "Addressed") | "Substrate default: twins for everything; production scissors require explicit declaration." | **Conditioned on C45 (faithful).** "Twins for everything" is only a real default if the twins are fidelity-certified; C45 supplies the certification. C45 does **not** own the production-scissors *declaration* (a C43/pack policy); it supplies *whether the twin substituted by default is faithful*. |
| **F56** Guardrail-bypass under stress (Replit-class) (F-MODE §4, "Addressed") | "Twins isolate the agent from production entirely; bounded blast radius." | **Conditioned on C45 + bounded by C43 (faithful).** The "bounded blast radius" holds because the agent hits a *faithful twin* (C45) behind a *confinement boundary* (C43). C45 certifies fidelity; C43 bounds the radius. |
| **F55** Behavioural drift / self-reference loop (F-MODE §6, "Partial") | "twins as **external truth**; held-out scenarios." | **Partial (faithful — matches F-MODE).** Twins serve as *external grounding* only if they are faithful to the real external service; C45's bar is what makes "twin = external truth" defensible. The residual — a twin's *reference* itself drifting from the evolving real service (OQ-C45-2) — keeps F55 "Partial"; C45 surfaces it as a residual, does not close it. |
| **F3 / F13** Spec-completeness fallacy / Missing-config blindspot (F-MODE §9, "Residual gap") | "Twins partially compensate … but the unspecified environment surface is fundamentally larger than any test set." | **Inherent residual (faithful — not C45 to close).** C45's predicate is evaluated over a **finite probe corpus** (C30); a twin can pass the bar yet diverge from the real service on un-probed inputs (the environment surface exceeds any test set, F3/F13). C45 makes the bar *explicit and auditable* but **cannot** make a finite corpus exhaustive — this residual is routed to **C57**, not silently absorbed (G22 honesty). |
| **G31 (lethal-trifecta blast radius, C43)** | The confinement that keeps a faithful-but-not-perfect twin's residual divergence from reaching production. | **Deferred to C43 (faithful — not C45's to build).** C43 owns twin *isolation* + boundary typing (inventory C43). C45 establishes fidelity; C43 bounds what a fidelity gap can do. Distinct boundaries; C45 does not absorb C43's job. |

> [AMBIGUITY: G22] **Is the "how close is close enough" bar a single global fidelity threshold, or a
> per-service predicate over named dimensions?**
> Reading A (single global bar): one numeric similarity threshold (e.g. "≥ X% response match") applied to
> every twin — simplest to state, one knob.
> Reading B (per-service predicate over named dimensions): "fidelity" is **not** one number — a payment API
> twin must match **error taxonomy and idempotency exactly** but may tolerate a latency band, whereas a
> read-only data API may tolerate omitted fields but must match pagination; a single global % both over- and
> under-constrains. v4 names the technique as "**Manual diff tooling … DIY**" and "**bounded engineering …
> per a specific service's SDK contract**" (AI-CONTEXT:347, README:468), i.e. **per-service and
> contract-shaped**, not one global number.
> **Pick: Reading B (binding — most consistent with v4).** v4 explicitly frames twins + their fidelity as
> **per-dependency, just-in-time, contract-shaped** work (README:468/520, AI-CONTEXT:487), and "Manual diff
> tooling / DIY" (AI-CONTEXT:347) implies a *judgement per service*, not a universal constant. So C45's bar
> is a **per-service predicate over named dimensions with per-dimension tolerances** (exact for
> contract/error-taxonomy/schema; bounded for latency/ordering/numeric/omission), combined by a stated pass
> rule. A single global similarity threshold is rejected as both over- and under-constraining. (The exact
> default tolerance values + the dimension catalog are sweep-2; the *shape* of the bar is fixed here as
> per-service-predicate.)

> [AMBIGUITY: G22] **Where does the "real service" ground truth come from — a live call, or a recorded
> reference?**
> Reading A (live oracle): call the real service at verification time to get current ground truth — maximal
> accuracy, always-current.
> Reading B (recorded/golden reference): capture real-service interactions out-of-band (record/replay,
> README:199) and diff the twin against that recorded corpus — no production call in the substrate loop.
> **Pick: Reading B (binding — most consistent with v4).** P7's entire purpose is to let scenarios run
> "thousands per hour **without rate limits**" and to "**remove the deploy-to-production vector**" / "isolate
> the agent from production entirely" (README:195, F-MODE §4 F33/F56). Putting a **live production call in
> the fidelity loop** would re-introduce exactly the rate-limit + production-exposure the twin exists to
> remove. So C45 diffs the twin against a **recorded/golden reference** captured out-of-band via record/replay
> (README:199) — the same capture C44's record/replay produces. The cost: the reference can **drift** from
> the evolving real service, so a `fidelity_pass` is only as current as its reference; the **refresh cadence
> + drift handling is OQ-C45-2**, surfaced as a residual (F55) — not a live-call in the loop.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C45 is the component that makes the **twin-based security posture honest**: F12/F33/F44/F56
  ("Addressed") all assert the agent meets a *twin* instead of production, which is only safe if the twin is
  faithful (C45) **and** the agent is confined to it (C43). C45 certifies the **former**; the **latter**
  (blast-radius confinement, G31) is **C43's** boundary, a distinct concern C45 does not absorb. C45's verdict
  is what lets a reviewer trust "twins not production" for a given twin. No new attack surface: C45 reads a
  twin + a recorded corpus and emits a verdict; it does **not** call production in the loop (the recorded-
  reference choice, OQ-C45-2).
- **Cost.** The verification is **bounded per-service engineering** (README:468/520) run against the **twin**,
  so it inherits P7's core cost win — fidelity probes run against the rate-limit-free twin, not the real
  service (README:195) — **except** the out-of-band **reference capture**, which does touch the real service
  occasionally (record/replay) and is the one place real-service cost/rate-limit applies (bounded by capture
  cadence, OQ-C45-2). C45 adds **no policy-engine / framework runtime cost**: the contract check is stack OSS
  (Pact/schemathesis) over record/replay-captured references, the custom part is the predicate + the
  behaviour diff + wiring.
- **Scale.** No new store; verdicts/reports are beads (C19/C20), the predicate is per-service config. C45 is
  instantiated **per twinned dependency, just-in-time** (AI-CONTEXT:487), so it scales with the number of
  twinned services × probe-corpus size, not with traffic. The probe corpus's scale story is C30's; C45 adds a
  per-twin verification pass over it.
- **Observability.** C45's **verdict + report feed *is* the observability surface for twin fidelity** — it is
  what makes "the twins verify behavioral fidelity against the real service" (README:499) auditable, and what
  makes F12/F33/F44/F56's "Addressed" inspectable (does *this* twin actually clear the bar?). The report's
  failing-dimensions/margins are the diagnostic for a `fidelity_fail`.
- **Ops.** The fidelity predicate (the bar) is authored **per service alongside the twin's pack** and kept
  under git review (it is the contract a twin must clear). Verification runs as **Gas City pack tool nodes**
  (README:201 "Gas City pack per service"; README:199 "Per-language tool node"). A twin/contract/reference
  change **invalidates** the prior verdict and triggers re-verification (§4.4). Refreshing the recorded
  reference against the evolving real service is a scheduled ops concern (OQ-C45-2).

## 8. Acceptance criteria & test strategy

1. **Fidelity bar is explicit + per-service (G22, the core deliverable)**: for a twinned service, C45 has a
   **written fidelity predicate** naming the checked dimensions, the per-dimension tolerances (exact vs
   bounded), the C30 probe corpus, and the pass rule — i.e. "how close is close enough" is a recorded,
   auditable artifact, **not** an implicit/"looks right" judgement. A twin with **no** predicate cannot be
   certified.
2. **Usage-vs-promises verified (contract half, README:201)**: C45 runs the contract verification
   (**Pact / schemathesis**, README:201/AI-CONTEXT:344) of the twin against the real service's contract and
   produces a per-dimension contract-conformance result; a twin that accepts a request/auth/response the real
   contract forbids yields a contract-dimension **fail**.
3. **Twin-vs-real verified (behaviour half, README:499)**: C45 drives the C30 fidelity-probe corpus at the
   twin and diffs responses against the recorded reference, scoring against tolerance; a twin whose behaviour
   breaches a dimension's tolerance yields a behaviour-dimension **fail**. (Reference is recorded/golden, not
   a live call — the residual is OQ-C45-2.)
4. **Two-sided pass rule asserts the invariant**: C45 yields **`fidelity_pass` only when both** halves pass
   their dimensions within the predicate; passing one half while breaching the other yields `fidelity_fail`
   with the failing dimensions named. A twin without a current `fidelity_pass` is **not certified for
   substitution** (C31/C43).
5. **Verdict + report feed present (downstream seam)**: C45 publishes, per twin × version, a
   `fidelity_pass|fidelity_fail` + the failing-dimension report as a bead, consumable by C31/C43 (substitution
   gate), C57 (residual register — the G22 caveat), and C53 (twin-build acceptance); a `fidelity_fail` is a
   fix-task candidate (C44/C39).
6. **Version-keying invalidates stale certification**: a change to the twin version, the service contract, or
   the recorded reference **invalidates** the prior `fidelity_pass` and requires re-verification — a drifted
   twin cannot retain stale certification (§4.4; related to OQ-C45-2).
7. **G22 residual routed (honesty)**: the residuals are explicit and discoverable in C57 — (a) a passing twin
   can still diverge on un-probed inputs (finite corpus vs unbounded environment surface, F3/F13), and (b) the
   recorded reference can drift from the evolving real service (F55/OQ-C45-2). "Addressed" for F12/F33/F44/F56
   is recorded as **conditional on a current passing verdict**, not unconditional.
8. **No tooling-rebuild over-build (bar)**: C45 contains **no** custom contract-testing engine, record/replay
   capturer, or mocking runtime — the stack-provided parts are **Pact / schemathesis** (contract,
   README:201/AI-CONTEXT:344) + **record/replay** reference capture (VCR/go-vcr/polly, README:199); the
   **only** custom code is the fidelity predicate + the **tolerance-scored behaviour diff** + the
   combine-and-gate wiring — the "Manual diff tooling / DIY" parts (AI-CONTEXT:347). *(Prism, AI-CONTEXT:343,
   is C44's OpenAPI mock, not a C45 check.)*

(Concrete fidelity-predicate schema + default tolerance catalog, the contract-check adapter contract, the
behaviour-diff record schema, and the verdict/report bead types are sweep-2 deliverables.)

## 9. Open questions

- **OQ-C45-1** (→ review-log; **the G22 bar — top open question**): **What are the concrete default fidelity
  dimensions + tolerances, and is there a sanctioned per-service-class template?** Sweep-1 fixes the bar's
  *shape* (per-service predicate over named dimensions: exact for contract/error-taxonomy/schema; bounded for
  latency/ordering/numeric/omission — §6 G22 ambiguity Reading B). Open: the concrete **dimension catalog**,
  the **default tolerance values**, and whether common service classes (REST/CRUD, payment, queue) get
  **starter predicate templates** so each twin doesn't redefine the bar from scratch. This is the residual of
  G22 after the shape is fixed — sweep-2, per first real twin (C44).
- **OQ-C45-2** (→ review-log): **How is the real-service reference captured and kept current (drift)?** C45
  diffs the twin against a **recorded/golden reference** (record/replay, README:199), not a live call (§6 G22
  ambiguity Reading B). Open: where the reference is stored (C44's record/replay capture? a C30 corpus? CXDB?),
  and the **refresh cadence** that keeps it current as the real service evolves — a stale reference makes a
  `fidelity_pass` certify against an outdated truth (F55 residual). Confirm capture home + refresh policy.
- **OQ-C45-3** (→ review-log; mirrors **C31:OQ-5**): **Does C45 invoke C31 to drive probes at the twin, or
  run the probe corpus directly as a pack tool node?** The fidelity-probe run is a *scenario run* against the
  twin as the run target (README:499); C31 is the Inspect-AI runner that selects the run target/twin
  (C31:OQ-5). Confirm whether C45 delegates probe execution to C31 (reuse the runner) or runs probes itself
  as a Gas City pack — a C45↔C31 seam.
- **OQ-C45-4** (→ review-log): **Is a `fidelity_pass` a hard gate on twin substitution, or advisory?** Sweep-1
  treats it as the **certification** that justifies substitution (C31/C43), implying a hard gate ("uncertified
  twin ⇒ not a sanctioned production substitute"). But v4 builds twins **just-in-time** "after rate limits or
  production exposure bite" (AI-CONTEXT:487), so an operator may want to run an un-certified twin in a
  scenario-only context. Confirm whether C45's verdict **blocks** substitution or only **annotates** it, and
  whether that differs for scenario-runs (C31) vs production-default substitution (F44/C43).
