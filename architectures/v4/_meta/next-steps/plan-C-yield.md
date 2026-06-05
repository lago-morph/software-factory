# Plan C — Maximize agent-os yield (the production-line lens)

> **Lens.** Measure the next 2–3 weeks in *shipped real agent-os components* — built into their own
> repos, tests green, gated through C53 — not in factory features exercised. The factory is a
> production line; the unit of output is a passing agent-os component. This plan reads the
> [grounding brief](./00-grounding-and-exemplar.md) as fact and improves on its
> [exemplar](./00-grounding-and-exemplar.md#part-b--exemplar-draft-plan-the-format-model-authors-produce-alternatives)
> from a throughput angle.

## 1. Thesis

The backbone's worth is proven by *count of real things it ships*, so the next 2–3 weeks should be
organized as a production line whose output is **shipped agent-os components**. The agent-os
dependency graph and the digital-twin gap ([C44, deferred](../../spec/C44-digital-twin.md)) jointly
dictate the order: build the **infra-light, cluster-free, T0 Workstream-B "code" components first**,
in dependency order, in parallel rigs, with one human batched-review rhythm — and treat every
infra-heavy Workstream-A component as explicitly *blocked* until twins exist. Yield is the metric;
the triangle keeps yield honest by routing each defect to a corner cheaply enough to survive volume.

## 2. The concrete agent-os build-order slice (what actually ships)

The selection rule is mechanical: **buildable now = (a) pure code, (b) deterministic clusterless
tests, (c) all upstreams already present or stubbable, (d) scoreable by held-out scenarios from its
own ACs.** Reading the [agent-os catalog](/tmp/agent-os/architecture-overview.md) §14 and the
per-component plan headers, the unblocked slice, **in dependency order**, is:

1. **B22 — Security threat model design spec** (`tier: T0`, `wave: W0`, `upstream: []`, est. L; see
   `/tmp/agent-os/plans/components/B/plan-B22.md`). *Why unblocked:* it is **design, not code** —
   no Helm, no cluster — and it is the non-blocking fan-out input every later component's security
   ACs reference. Shipping it first means later builds inherit real acceptance criteria. Best *first*
   real build precisely because it has zero upstreams.
2. **B12 — CloudEvent schema registry** (`T0`, `W2`, `upstream: [A4, B8]`, est. M;
   `/tmp/agent-os/specs/components/B/spec-B12.md` §8 says *PyTest applicable; Chainsaw N/A — no CRD;
   Playwright N/A — no UI*). *Why unblocked:* pure JSON-Schema + Python validators; its A4/B8
   upstreams are only *event-name contracts*, stubbable as fixtures. Fully clusterless. ACs
   `AC-B12-01..06` are deterministic CI checks — an ideal held-out scenario set.
3. **B3 — OPA policy library framework** (`T0`, `W1`, `upstream: [A7]`, est. M;
   `/tmp/agent-os/plans/components/B/plan-B3.md`). *Why unblocked:* the framework is Rego + tooling;
   its PyTest and `opa test` Rego-unit layers run with no cluster (only the Chainsaw *ArgoCD-reconcile*
   layer needs one — score the clusterless layers, mark Chainsaw as a twin-gated holdout).
4. **B16 — Initial OPA policy content** (`T0`, `W2`, `upstream: [B3, A1, A6, A5, B13]`, est. L).
   *Why unblocked after B3:* the **admission** Rego only needs B3 + the CRD shapes (schemas, not a
   running operator); author and `opa test` it clusterless. The runtime/egress policies that bind to
   live A1/A6 are a *deferred sub-batch* — split the component at the natural admission/runtime seam.
5. **B6 — Platform SDK** (`T0`, `W2`, `upstream: [A1, A2]`, est. XL). *Why partially unblocked:* B6 is
   explicitly **contract-first** (`plan-B6.md`: "freeze the four surface groups' signatures … as the
   versioned API before deep implementation"). The contract + cross-language contract-test suite
   build against mock LiteLLM/Letta hosts — clusterless. Ship the contract layer; defer live-binding.
6. **B9 — `agent-platform` CLI** (`T1`, `W2`, `upstream: [A1, A2, A5]`, est. L). *Why unblocked:* the
   CLI shell, config, subcommand surface and audit-on-run (`plan-B9.md` TASK-01/02) are a Python
   container with soft-dependency degradation built in — runnable and PyTest-scoreable without the
   platform behind it.

Natural follow-ons once the line is warm (same rule): **B17 agent-profile library** (`T1`, content
overlays), **B2 LiteLLM callbacks** (`T1`, `W1` — *builds against a documented mock LiteLLM hook
host*, `plan-B2.md` TASK-01), and **B18 recommended compositions** (`T2`, `W4`, content).

**Explicitly BLOCKED on twins/cluster** (the C44 gap made concrete): **A1 LiteLLM**, **A5 ARK
operator**, **A6 agent-sandbox + Envoy**, **A7 OPA/Gatekeeper install**, **A23 Kargo fabric**, and
every other Workstream-A install/configure package — they are scored only by a *live* `kind`/twinned
cluster (Chainsaw/Playwright on real CRDs). Also blocked: the *runtime* halves of B16/B6/B2 above,
and **A18's** deployable audit endpoint (its Python adapter *library* is clusterless and buildable;
its endpoint Deployment is not). This split — code-now vs. cluster-later — is itself one of the most
valuable findings the line will produce, and it is `[PROPOSED — not in source]` as a *split-the-
component* tactic: agent-os specs don't pre-cut components at the admission/runtime seam.

## 3. Milestone-ordered spine (gates, not day-counts)

- **Gate L0 — Line calibration.** Re-confirm the substrate truth the brief flags first: Gas City
  conformance and **prevent-vs-detect**
  ([decision #4](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)).
  Stand up *one* rig, run **B22** (design-only, lowest blast radius) through spec→build→judge to
  prove the eval tier end-to-end and to calibrate `judge_self_trust` before any volume. **Exit:** one
  shipped component + a green loop + the triangle observed routing an injected spec defect and
  scenario defect to the right corner ([ADR-0069](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)).
- **Gate L1 — First *code* self-build, gated.** Run **B12** through intent-crucible → C08 spec →
  build into its own repo (C52) → held-out scenarios from `AC-B12-01..06` → the four-term
  [C53 gate](../../spec/C53-bootstrap-validation.md). **Exit:** a recorded `go` and a real passing
  agent-os repo — the bet-#3 moment, on genuinely useful code.
- **Gate L2 — Parallel rigs / first batch.** Light up **multiple rigs** (C42) and push **B3, B16-
  admission, B6-contract, B9-shell** as a *batch*, each with its own scenarios. The fence (C43) is up
  before any unattended rig per [D-20](../../../../decisions-to-make.md#1). **Exit:** 3–4 shipped
  components and a working **batched human review** (one sitting clears the batch, not one PR at a time).
- **Gate L3 — Steady-state cadence.** Establish the repeating rhythm: *fill the batch with unblocked
  next-in-graph components → run rigs in parallel → one batched go/no-go review → harvest the defect
  ledger → refill*. **Exit:** the line sustains a batch per review-cycle, and the ledger names the top
  3 substrate gaps blocking further yield (twins almost certainly #1).

## 4. Finding and fixing defects at production volume

The methodology is the
[triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md): the
judge is a **diagnostician** (C32) returning `root_cause ∈ {judge, spec, scenario, system, none}`, so
every failure is *pre-routed* to a corner — this is what makes volume affordable. The production-line
additions:

- **Defect ledger as a batch artifact, not a per-run one.** Each batch review produces one ledger
  pass: every divergence tagged by corner + owner. Cost stays flat per batch because triangulation is
  free output of the judge, not extra human work.
- **Corner-rate dashboard.** Track defects-per-corner *across* builds. A spike in `root_cause = spec`
  means the intent-crucible needs work; a spike in `scenario` means AC-derivation is weak; a spike in
  `judge` means recalibrate before trusting `tri_alignment`. This turns volume into signal.
- **Cheap-by-construction.** Because the slice is clusterless and deterministic, scenarios are PyTest/
  `opa test` checks — fast, free to re-run, no twin to mock. A 100% held-out floor that *never lowers*
  ([C53 §3.2](../../spec/C53-bootstrap-validation.md)) is enforceable at near-zero marginal cost.

## 5. Longer horizon (named, not scheduled)

Yield growth is gated on substrate the factory can't yet build around. The unlock order, driven by
*what unblocks the most agent-os backlog*: **digital twins (C44/C45)** — they convert the entire
blocked Workstream-A install/configure backlog (A1/A5/A6/A7/A23 …) and the deferred runtime halves of
B16/B6/B2 from un-scoreable to scoreable, and complete the fence's deferred half. Then **CXDB
trajectory store (C21/C24) → self-heal chain (C36→C37→C38→C39)** so the line diagnoses its own build
failures. Then **methodology-as-config ([C55](../../spec/C55-methodology-experiment.md))** used
*pragmatically per work-shape*: an **install+configure formula** for Workstream-A (heavy on
conformance/Chainsaw verification once twins exist) vs. a **custom-Python formula** for Workstream-B
(PyTest/`opa test`, contract-first) — GF-M is merely the cheapest first experiment, not the winner.
Last, the sequential self-optimization tail (C46→C47→C48→C50, C49 kept experimental). The
**objective-drift detector** (F54) becomes a hard prerequisite before any lights-out rung once the
line grinds dozens of components unattended.

## 6. Top 3 throughput risks + mitigations

1. **Single Max-seat is the throughput ceiling.** Candidates × scenarios × judge runs is multiplicative
   token cost on one seat ([brief A6](./00-grounding-and-exemplar.md#a6-hard-constraints--known-risks-the-plan-must-respect));
   v4's "cost amortizes" carries no number. *Mitigation:* keep batch width small and measured; favor
   the cheap clusterless slice (deterministic tests cost no extra judge tokens); quantify per-component
   seat-cost before widening any batch — the line throttles to the seat, not the other way.
2. **The blocked-on-twins backlog starves the line.** Once the ~8 clusterless B-components ship, the
   *next* highest-value work is all twin-gated A-components — yield stalls. *Mitigation:* the
   component-split tactic (ship admission/contract halves now) extends the runway; treat twins (C44) as
   the explicit next factory-build the moment the ledger shows the line is twin-starved.
3. **Volume erodes review quality / drifts objectives.** Batched review can rubber-stamp; the
   drift-watcher is unbuilt ([decision #2](../../../../decisions-to-make.md#2)). *Mitigation:* the
   human go/no-go stays per-batch and mandatory (C53's human term is non-negotiable); ride the "are the
   goals still right?" checkpoint on every batch review until the real detector exists.

## 7. Three biggest differences from the exemplar

1. **The metric is shipped-component count, not loop-correctness.** The exemplar drives at *one*
   bootstrap proof then widens cautiously; this plan treats the whole 2–3 weeks as a production line
   and names a **6-component-plus ordered slice** with a mechanical buildable-now rule, optimizing
   total yield rather than first-proof.
2. **Parallel rigs + batched-review rhythm are the spine, not a late "widen" gate.** The exemplar
   widens at Gate 4; this plan stands up parallel rigs at L2 and makes the *repeating batch cadence*
   (L3) the deliverable — throughput is designed in from the first batch, with the single-seat ceiling
   treated as the explicit governing constraint.
3. **Component-splitting at the admission/runtime seam.** Rather than waiting on twins to build A-/B-
   runtime work, this plan ships the clusterless *halves* now (B16-admission, B6-contract, A18-adapter-
   library) and defers the cluster-bound halves — a `[PROPOSED — not in source]` tactic that the
   exemplar does not use, materially enlarging the buildable-now backlog before twins exist.
