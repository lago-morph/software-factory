# Grounding brief + exemplar — "What's next after the 25-component backbone"

> **Purpose.** This is the shared input for a multi-agent planning exercise. It (a) fixes the
> facts every plan-author and reviewer must work from, and (b) ships one *exemplar* draft plan
> as the format model. Authors produce alternative plans; reviewers critique the synthesis.
> **Scope discipline (operator directive):** consider **only v4** (`architectures/v4/`). Earlier
> architecture versions (v1–v3) are explicitly out of scope for this exercise — they get
> incorporated "much later"; the goal now is to get the *initial prototype factory* working.

---

## Part A — The fixed facts (do not re-derive; cite these)

### A0. The REAL target product: `lago-morph/agent-os` (this is what the factory is FOR)
The operator's actual goal is **not** the factory for its own sake — it is to build
**`lago-morph/agent-os`** semi-autonomously, using the factory as the means. agent-os is the
**architecture-of-record for a Kubernetes-based agent runtime platform** (an open-source clone of
Claude Managed Agents): it runs AI agents as governed, observable, policy-controlled Kubernetes
workloads, with a single chokepoint for LLM / MCP / A2A / outbound-HTTP traffic (LiteLLM), OPA/RBAC
policy everywhere, CloudEvents on a Knative/NATS fabric, Crossplane substrate abstraction, and a
self-management agent (HolmesGPT). Key facts that make it the perfect real workload:

- **It is a pure spec/design corpus, not code** (374 markdown files). Implementation happens in
  **independent per-component repositories**. So agent-os is *already* exactly what a
  "specs-are-the-source-of-truth → working-software-out" factory consumes.
- **~65 components in 6 workstreams** (A: platform install/ops, 23 components; B: custom dev,
  22; C: docs; D: dashboards; E: training; F: production-hardening). **Every component already
  carries a paired `spec-X.md` + `plan-X.md`** with explicit acceptance criteria (`AC-B12-02`…),
  per-layer test strategies (PyTest / Chainsaw / Playwright), dependency tiers (T0/T1…), waves
  (W1/W2…), and size estimates (S/M/L). These are *build-ready* specs — the factory's intent-crucible
  work (C11/C10) is largely pre-done by agent-os itself.
- **Infra-light vs infra-heavy split matters for the factory.** Many Workstream-A components are
  "install + configure" on a live Kubernetes cluster (need a real or twinned cluster to score).
  But a cluster of Workstream-B components are **pure code with deterministic tests and no cluster
  required** — e.g. **B12 CloudEvent schema registry** (JSON-Schema + Python tooling, PyTest),
  **B3 OPA policy framework** (Rego + `opa test`), **B12/B16** policy/schema content, **B6 Platform
  SDK**, **B9 `agent-platform` CLI**, **A18 audit adapter library** (Python). These are the natural
  *first real builds*: bounded, genuinely useful, and scoreable by held-out scenarios **without**
  standing up the whole platform.

**The load-bearing implication for this plan:** "exercise the factory with real work, not baby
tests" = **point the factory at agent-os's own backlog.** The factory ingests an agent-os
`spec-X.md` (+ `plan-X.md`), builds the component into its own repo, scores it against held-out
scenarios derived from the spec's ACs + test strategy, and gates it through C53. This also surfaces
a real, important finding early: **the factory's digital-twin gap (C44, deferred) directly bounds
how much of agent-os it can build before twins exist** — infra-light B-components are buildable now;
infra-heavy A-components (operators, Helm installs, cluster policy) wait on twins or a real `kind`
cluster. That dependency is itself one of the most valuable things the first weeks will teach us.

> A read-only clone of agent-os is available in the sandbox at `/tmp/agent-os` (subagents may read
> it). The component catalog is `architecture-overview.md` §14; per-component specs live in
> `specs/components/<A–F>/spec-*.md` with paired `plans/components/<A–F>/plan-*.md`.

### A1. Where we are (the assumption that frames everything)
The **25-component "safe self-build backbone"** is assumed **implemented and integrated by end of
this weekend**. Per [the implementer build order](../../implementation-dependencies.md#the-backbone-25-components-but-only-seven-products-to-build),
the backbone is **not 25 separate builds** — it is **seven products**:

1. **Gas City** (adopt + configure the `gc` binary) — delivers 11 backbone components at once
   (C01 substrate, C02 pack ABI, C03 config, C04 sessions, C05 sling/dispatch, C17 tool-node,
   C18 reconciler, C19 bead store, C23 event bus, C41 attribution, C42 rigs).
2. **Claude Code** (adopt) + **model-floor policy** (custom C29) — the worker + cross-family routing.
3. **Spec intake** (custom C08 spec artifact, C09 prompt-template binding).
4. **Bead-type schema** (custom C20 — the authored contract on Gas City's bead store).
5. **Evaluation tier on Inspect AI** (adopt-then-author: C30 scenario store, C31 runner,
   C32 judge, C33 satisfaction) — **the hinge of the whole build**.
6. **The fence** (custom: C34 holdout integrity + C43 boundary-typing half).
7. **Bootstrap** (custom: C51 gene-transfusion predicate, C52 self-bootstrap recursion + human
   design-review gate, C53 the go/no-go milestone).

**Capability this unlocks:** the factory can now **author a spec for one of its own next
components, build it in an isolated rig, have that build scored by a trustworthy satisfaction
signal, and pass it through a human-reviewed go/no-go gate before it deploys.** That apex is the
**C53 bootstrap-validation milestone**. Reaching it is what the next 2–3 weeks are *about*.

### A2. The make-or-break caveat that must be discharged FIRST
Almost every "Gas City does X natively" claim in v4 is **a claim to verify, not a verified fact**.
No one has run `gc` end-to-end against v4's native claims. The literal first practical step of the
whole build is the **Gas City conformance check (C01 AC-2)** — see
[the build order](../../implementation-dependencies.md#gas-city--gc-binary-mit) ("the whole product
rests on the conformance check"). **If the 25 are genuinely "done," conformance presumably passed**
— but one sub-question is *not* settled by "it runs": **prevent vs. detect**
([decision #4](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)).
Does Gas City *physically refuse* an out-of-partition read at tool-call time (prevention), or does
the read go through and an audit catch it afterward (detection)? Holdout integrity (C34) and the
fence (C43) are **strictly weaker if it's detect-only**. This shapes how much we can trust the very
first self-build. Treat re-confirming prevent-vs-detect as a near-zero-cost early action.

### A3. The defect-finding methodology is already designed: the **triangle**
This is the spine of the answer to "what methodology should I use to find the defects."
[ADR-0069 — the spec↔scenarios↔system triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)
(decision D-42/D-43) is v4's **evaluation invariant**:

- The three corners are **Spec** (what we asked for, C08), **Scenarios** (the held-out tests, C30),
  and **System** (what got built). A component is **complete only when all three edges align.**
- **The judge is a *diagnostician*, not a scorer** (C32). On a failure it returns a
  `DiagnosisRecord` whose `root_cause ∈ {judge, spec, scenario, system, none}` — it *localizes*
  every defect to one corner. A failing scenario might mean the *system* is wrong, or the *spec*
  was ambiguous, or the *scenario* itself is broken, or the *judge* mis-scored.
- **100% hold-out pass is necessary but NOT sufficient** (the floor never lowers); tri-alignment
  (`all_scenarios_satisfied = true` AND `root_cause = none`) plus a human-approve verdict plus a
  post-deploy factory-integrity check are the **four conjunctive terms** of the C53 go/no-go
  ([C53 §3.2](../../spec/C53-bootstrap-validation.md)).

**Implication for "how to find defects":** you exercise the factory by feeding it work, and every
divergence the triangle surfaces is *attributable to a corner*. That turns "the factory has bugs"
into "this run had a spec defect / a scenario defect / a system defect / a judge-calibration
defect" — a falsifiable, routable signal. This is the methodology.

### A4. "Formulas" has a precise local meaning — and a useful double meaning
The user asked "what **formulas** should I design to exercise this thing and find the defects."
In v4, **a Formula is a literal artifact: a C12 pipeline file (a TOML DAG)** — the methodology
lives in the *file*, not in agent prompts. Two senses are both in play and both legitimate:

- **Literal formulas (C12 pipeline files):** the workflows you run. The plan should start with a
  minimal **3-step formula** (validate the runner), add the **formula↔DOT translator (C14)** for
  visualization + Mammoth-style linting, then grow to formulas that deliberately exercise each
  principle/seam.
- **"Formulas" as *probe designs* — the scenarios + work items you push through to provoke
  defects.** These are authored in the held-out scenario corpus (C30) and judged by the triangle.

**Methodology-as-config (C55)** is the longer-horizon frame: v3's ten candidate methodologies
become **ten swappable formula files** run over the *same* scenarios + judge, selected *empirically
per kind of work*. **GF-M is registered first only because it is cheapest to stand up — "GF-M first"
means "first experiment," NOT "the winner"** ([C55 INV-3](../../spec/C55-methodology-experiment.md)).
Note: C55 is Phase-3 work (after the eval tier is proven), so it is *horizon*, not week-1.

### A5. The evolution path (how the rest of the 57 components get added)
After bootstrap validation passes, the factory builds its own next pieces — **factory builds
factory** (C52). The **top-10 cost/benefit list** for what to build next is already ranked in
[the build order](../../implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit):
C07 vocabulary glossary (tiny, best ratio), C25 OTLP export (cheap visibility), C10 EARS spec
linter, C11 intent crucible, C40 durable Orders, C56 autonomy ladder, C35 override→rule loop,
C21 CXDB trajectory store (gateway to the back half), C44 digital twin, C12/C13 formula+molecule.
Then the **self-heal chain** (CXDB bridge C24 → anomaly C36 → clustering C37 → diagnosis C38 → fix
closure C39), then **twins** (C44/C45), then the **self-optimization tail** (meta-metrics C46 →
variant-id C47 → A/B stats C48 → promotion gate C50 + the unsolved counterfactual-replay C49) —
which is *genuinely sequential and cannot be compressed by adding people.*

### A6. Hard constraints / known risks the plan must respect
- **The fence before any unattended run.** D-20 / decision #1: the boundary-typing fence (C43) must
  be up before the factory runs unattended; it's cheap (needs only rig partitions). Twins wait.
- **Single Max seat throughput / cost fan-out.** Running candidates × work-types × scenarios through
  the judge is *multiplicative* token cost on one seat; v4's "cost amortizes" claim carries no
  number. Keep experiment fan-out incremental; quantify before any full grid.
- **Objective-drift watcher is unbuilt** (decision #2 / F54). Fine while a human reviews in batches
  (cheap "are the goals still right?" checkpoint); a real detector is a prerequisite *before*
  lights-out, not during.
- **Vocabulary lock-in** (cities, rigs, formulas, molecules, beads, slings) — real cognitive load.
- **Counterfactual replay (C49)** is the hardest unsolved invention; ship the deterministic half,
  keep the LLM-replay half experimental and human-reviewed (decision #3).

### A7. The reader of the FINAL deliverable
The final report is for **jonathan@manton.com** — the human principal who *does not write code* (see
[the plain-English build order](../../../../build-order-plain-english.md)). It must be **plain
language**, no unexplained jargon, every local term translated on first use. Per the
`human-scoped-deliverables` skill: prefer corpus terms over invented jargon; Mermaid diagrams ≤7
elements; **no fabricated quantitative time estimates** — but the user explicitly set a **"next 2–3
weeks"** organizing window, so use that window and order work as *milestones/gates*, not day counts.

---

## Part B — Exemplar draft plan (the format model; authors produce alternatives)

> This exemplar is the lead agent's first-pass spine. It is deliberately the *bootstrap-first*
> reading. Plan authors should treat it as one option to improve on or argue against, not the answer.

**Thesis.** The backbone exists to make *one* thing possible: the first safe self-build of *real*
software. So the next 2–3 weeks should drive straight at the **C53 bootstrap-validation milestone**
using a **small, infra-light, genuinely-useful agent-os component** as the first build — and use the
**triangle** to convert every run into routable defect signal. The work is real (an agent-os
component, shipped to its own repo with passing tests), not a toy; "small" means *low blast radius
and no cluster required*, not *low value*. Everything else (breadth, methodology experiments,
self-heal, twins) is gated behind "can the factory build a real agent-os component and have us trust
the result?"

**Week-by-week spine (milestone-ordered, not day-counted):**

- **Gate 0 — Substrate reality check (first 1–2 days).** Re-confirm the Gas City conformance result
  and, specifically, **prevent vs. detect** (decision #4). Stand up one `claude` worker in a rig,
  confirm attribution flows into beads, confirm a cross-partition read is *refused* (or record that
  it's detect-only and adjust the fence's trust accordingly). **Exit:** a one-page "substrate truth"
  note that turns the riskiest assumption into a fact.

- **Gate 1 — First formula + first scenario, on a real spec (week 1).** Author a minimal **3-step
  C12 formula** (spec-in → build → judge) and a small **held-out scenario set** derived from a real
  agent-os component's acceptance criteria, to prove the eval tier end-to-end: scenario → run (C31) →
  diagnose (C32) → satisfaction (C33). Use **agent-os B12 (CloudEvent schema registry)** or **B3
  (OPA policy framework)** — both are pure code, PyTest/`opa test`-scoreable, no Kubernetes needed,
  with ACs already written. **Exit:** a green end-to-end loop, and the **triangle observed working**
  — deliberately inject a spec defect and a scenario defect; confirm the judge's `root_cause`
  localizes each to the right corner.

- **Gate 2 — The first real self-build (week 1–2).** Take the agent-os **B12** spec+plan as input,
  run it through the factory's intent crucible (C11) → buildable C08 spec → build into its own repo
  (C52), with held-out scenarios (C30) from its ACs + PyTest strategy, and put the result through
  the **C53 four-term gate**. **Exit:** a recorded `go`/`no_go` with evidence and a **real, passing
  agent-os component repo** — the **bet-#3 moment** (does factory-builds-factory work on real work?).

- **Gate 3 — Exercise to find defects, deliberately (week 2).** Push *varied real* agent-os work
  through: an ambiguous-spec component, a component with HARD upstream deps (brownfield-shaped
  integration), an adversarial holdout-leak attempt, and a component that *should* trip the
  twin/cluster gap (an infra-heavy A-component) to confirm the fence/limits hold. The goal is **not**
  feature count — it's **provoking each defect class** and confirming the triangle routes it. Build
  the **defect ledger**: every divergence tagged by corner (spec / scenario / system / judge) with a
  fix owner. **Exit:** a populated defect ledger + the top 3 substrate gaps the factory itself can't
  yet build around (twins almost certainly among them).

- **Gate 4 — Widen, deliberately and safely (week 2–3).** With one self-build proven, run 2–3 more
  infra-light agent-os B-components through the same loop (e.g. **B16** policy content, **B6** SDK,
  **B9** CLI, **B12**'s downstream **B19** approval schemas), each with its own scenarios. Confirm
  the **fence is up before any unattended batch** (D-20). Stand up **C56 autonomy-ladder** language so
  the human-in-the-loop rung is named and the "are the goals still right?" checkpoint rides every
  batch review. **Exit:** 3–4 factory-built agent-os components in their repos, a working
  batched-review rhythm, and a clear-eyed decision on whether to begin the CXDB/self-heal arc or the
  twins build first (driven by what the defect ledger says is blocking agent-os progress).

**Longer horizon (named, not scheduled):** the gating question becomes "what does agent-os need next
that the factory can't yet build?" Almost certainly **digital twins (C44/C45)** — they unlock the
infra-heavy Workstream-A components (operators, Helm installs, cluster policy) *and* complete the
fence's deferred half. Then **CXDB trajectory store (C21/C24) → self-heal chain
(C36→C37→C38→C39)** so the factory diagnoses its own failures building agent-os; then **methodology
experiments via C55** (run GF-M and other v3 formulas as *experiments* to learn which formula best
builds which agent-os workstream); then the sequential **self-optimization tail**
(C46→C47→C48→C50, + C49 kept experimental). The **objective-drift detector** becomes a hard
prerequisite *before* any lights-out rung — especially once the factory is grinding through dozens of
agent-os components unattended.

**Top risks this plan is betting against:** (1) prevent-vs-detect comes back "detect" and the fence
is weaker than assumed; (2) the first bootstrap self-build fails human review (plan: iterate spec,
re-run; if persistent, the factory needs more substrate before Phase 3); (3) judge mis-calibration
makes the triangle's `root_cause` unreliable — mitigated by the human-audited calibration sample
(judge_self_trust) before trusting `tri_alignment`; (4) single-seat cost makes broad exercise slow.

---

## Part C — What each downstream agent must deliver

**Plan authors (Wave 1):** an *alternative* full plan in your assigned lens, written to your
assigned file, same shape as Part B (thesis → milestone-ordered spine → longer horizon → top risks).
Return a ≤15-line receipt: your thesis in one sentence, your 3 biggest *differences* from the
exemplar, your single strongest argument, and your top risk.

**Panel reviewers (Wave 2):** critique the *synthesis* plan (`10-unified-plan.md`). Use the three
verdict tiers — `accept-as-is`, `accept-with-named-amendments`, `reject-with-counter-proposal`.
Ground every objection in a cited fact (this brief, the specs, the decisions doc). Return a ≤15-line
receipt: verdict tier, top-3 named amendments (each with the cited fact), and the single thing the
plan gets *most wrong*.
