# Unified plan — exercising and evolving the v4 factory on real `agent-os` work

> **What this is.** The synthesis of three competing Wave-1 plans
> ([A — velocity](./plan-A-velocity.md), [B — de-risk](./plan-B-derisk.md),
> [C — yield](./plan-C-yield.md)) into one candidate, written against
> [the shared grounding brief](./00-grounding-and-exemplar.md). It is the artifact the expert panel
> reviews. **Horizon:** the 2–3 weeks *after* the 25-component "safe self-build backbone" is built.
> **Scope:** v4 only; the real workload is `lago-morph/agent-os`.
> **Note on links:** `agent-os` lives in a sandbox clone outside this repo, so its files are cited as
> plain paths (e.g. `/tmp/agent-os/specs/components/B/spec-B12.md`), not repo-relative links.

## 0. The one-paragraph version

The backbone hands us two things: a **measurement instrument** (the spec↔scenarios↔system
[triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md), where the
judge *diagnoses* a `root_cause` corner) and a **go/no-go gate**
([C53](../../spec/C53-bootstrap-validation.md)). The fastest *honest* path to value is: **calibrate the
instrument, then drive one real `agent-os` component through the gate, then open a production line** —
in that order. The reason the order matters is a fact the backbone makes uncomfortable: the judge ships
`judge_self_trust = uncalibrated`, and the mechanism that would make it `calibrated` (PF-2) is deferred
to C46, which is **not in the backbone** ([C32 OQ6](../../spec/C32-judge-harness.md)). So "the triangle
works" is unproven by construction. We earn the green light before we read it; then we ship real
software (`agent-os` B-series components) and let the triangle route every defect to a fixable corner.

## 1. The three convergences (high confidence) and the one reconciliation

All three independent plans agreed on these — treat them as settled:

- **Substrate truth comes first.** Re-confirm Gas City conformance and, specifically,
  **prevent-vs-detect** ([decision #4](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)).
  Holdout integrity ([C34](../../spec/C34-holdout-integrity.md)) and the fence
  ([C43](../../spec/C43-isolation-boundary.md)) are *strictly weaker* if the substrate only detects.
- **The triangle is the methodology; the defect ledger is the artifact.** Every divergence is routed
  by `root_cause ∈ {judge, spec, scenario, system, none}` to a corner with a fix owner.
- **The real workload is `agent-os`, and the first builds are its infra-light B-components** — they
  score with PyTest / `opa test`, need **no Kubernetes cluster**, and have acceptance criteria already
  written. The **digital-twin gap** ([C44, deferred](../../implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit))
  bounds how much of `agent-os` is buildable before twins exist — and discovering exactly where that
  line falls is one of the highest-value outputs of these weeks.

**The reconciliation (velocity vs. yield).** Plan A says "drive one nail"; Plan C says "run a
production line." These are not in conflict once trust is sequenced: **one trustworthy nail first
(it validates the instrument *and* the gate), then the line.** Plan B is right that the nail is
worthless if the instrument behind it is uncalibrated — so calibration is a *precondition gate*, not a
smoke test folded into the first build.

## 2. The milestone-ordered spine (gates, not day-counts)

> The "2–3 weeks" is the operator's window; work is ordered as gates with exit criteria, not day
> estimates (per [the grounding brief on effort](./00-grounding-and-exemplar.md#a7-the-reader-of-the-final-deliverable)).
> Roughly: Gates 0–2 are week 1; Gates 3–4 span week 1–2; Gate 5 is week 2–3.

### Gate 0 — Substrate truth + first end-to-end loop (on a design-only target)
- **Goal.** Turn the riskiest assumption into a fact, and prove the eval tier runs end-to-end — in one
  pass, because they share the same first rig setup.
- **Actions.** Stand up one `claude` worker rig + a **separate judge rig** (cross-family judge per the
  [model-floor policy](../../spec/C29-model-floor-stylesheet.md) and the separate-judge-rig discipline
  in [C32](../../spec/C32-judge-harness.md)). Attempt a cross-partition read of the scenario partition
  and a production-typed action; record **prevent vs. detect** for each. Confirm attribution flows into
  beads. Then run a **trivial first pass** through `spec → build → judge → satisfaction` using
  **`agent-os` B22 (security threat-model *design spec*)** as the target — chosen because it is
  *design, not code*, has **zero upstream dependencies**, and is the lowest-blast-radius real thing the
  factory can produce (`/tmp/agent-os/plans/components/B/plan-B22.md`).
- **Exit.** A one-page **"substrate truth" note** (prevent or detect, recorded) **and** a green
  end-to-end loop **and** one shipped real artifact (a B22 draft) — proving the pipe works on something
  real before we ask it to write code.

### Gate 1 — Calibrate the judge (the load-bearing gate)
- **Goal.** Earn the right to trust `root_cause` / `tri_alignment`. The backbone ships the judge
  `uncalibrated` and the calibration mechanism (PF-2) is deferred to C46, outside the backbone
  ([C32 OQ6](../../spec/C32-judge-harness.md)) — so this gate designs a **minimal human-audited**
  version of it.
- **Actions.** Build a **judge-calibration sample**: a small fixed set of trajectories with
  *human-authored ground-truth root-cause labels* spanning **all five corners**
  (`judge / spec / scenario / system / none`). Run the judge; measure agreement against the labels —
  and explicitly measure the **false-green rate** (`root_cause = none` on a build that actually has a
  defect), the most dangerous error. Cross-check against the per-path C32 acceptance criteria
  ([AC-C32-16..23](../../spec/C32-judge-harness.md)).
- **Exit.** A recorded judge false-positive / false-green rate. **Until it clears a stated bar,
  `oversight_level = full` ([C53 §3.3](../../spec/C53-bootstrap-validation.md)) and
  `tri_alignment = aligned` is advisory only — never a deploy authority.** The bar value and sample
  size are operator policy `[PROPOSED — not in source]`.

### Gate 2 — Holdout integrity, adversarially
- **Goal.** Confirm the agent cannot teach to the test — otherwise every satisfaction score is a lie.
  F28 "holdout leakage" is marked *Addressed* ([F-MODE-COVERAGE §1](../../F-MODE-COVERAGE.md)) but on
  the same unverified substrate.
- **Actions.** Author the held-out scenario set for the first *code* build (B12, Gate 3) from its ACs.
  Run a deliberate **leak probe**: instruct a worker to read `scenarios/<component>/`; confirm it is
  refused (if Gate 0 found *prevent*) or at least audited and flagged (if *detect*), per
  [C34](../../spec/C34-holdout-integrity.md).
- **Exit.** A recorded holdout-integrity verdict. If detect-only, the **post-run audit gate**
  ([decision #4 option B](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact))
  is wired in *before* any score is trusted as un-gamed.

### Gate 3 — The first real *code* self-build: B12 through C53 (honestly gated, cost-measured)
- **Goal.** The **bet-#3 moment** — does factory-builds-factory work on real work? — read through a
  *calibrated* instrument.
- **Actions.** Take **`agent-os` B12 (CloudEvent schema registry)** as input — pure JSON-Schema +
  Python, PyTest-scoreable, **Chainsaw/Playwright N/A, no cluster** (`spec-B12.md` §8). Run it through
  the intent crucible ([C11](../../spec/C11-intent-intake.md)) → buildable [C08 spec](../../spec/C08-spec-artifact.md)
  → build into its own repo ([C52](../../spec/C52-self-bootstrap.md)) → held-out scenarios from
  `AC-B12-01..06` → the **four conjunctive C53 terms**: 100% hold-out floor ∧ `tri_alignment = aligned`
  ∧ human-approve ∧ post-deploy factory-integrity ([C53 §3.2](../../spec/C53-bootstrap-validation.md)).
  **Quantify the single-seat token cost of this one build** (judge runs are multiplicative on one Max
  seat — [C32 OQ3](../../spec/C32-judge-harness.md)).
- **Exit.** A recorded `go`/`no_go` on the `factory_build` bead with its evidence bundle **and the
  Gate-1 calibration verdict attached** (so the `go` is auditable as more than "the judge said so"),
  **a real passing B12 repo**, and a **per-component cost number** that governs how wide Gate 5 can go.
  On `no_go`: iterate the spec and re-run within `max_attempts`; if it persists, the honest finding is
  *the factory needs more substrate before Phase 3* (the accepted fail branch).

### Gate 4 — Provoke each defect class deliberately; populate the ledger
- **Goal.** Exercise to *find* defects, not to add features — coverage of defect *classes* beats count.
- **Actions.** Push varied real `agent-os` probes: an **ambiguous-spec** component (provoke
  `root_cause = spec` — B12's own `[PROPOSED]` event-name gaps are a real source); an **infra-heavy
  A-component** (e.g. A1 LiteLLM) that *should* trip the twin gap, to confirm the fence/limits hold and
  produce a *correct* block rather than a false green; and a **leak probe under load**. Build the
  **defect ledger**: one column per corner + a fix owner, **plus a fifth column for judge-disagreement
  events** (human review overruled `root_cause`) that feeds recalibration.
- **Exit.** A populated defect ledger; the **top-3 substrate gaps the factory can't yet build around**
  (twins near-certain #1); an updated judge FP rate.

### Gate 5 — Open the production line (widen, only behind the fence)
- **Goal.** A sustained, safe batched rhythm whose output is *shipped `agent-os` components*.
- **Actions.** Confirm the **fence (C43) is up before any unattended batch**
  ([decision #1](../../../../decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after)).
  Light up **multiple rigs** ([C42](../../spec/C42-rig-partitioning.md)) and push the dependency-ordered
  clusterless slice as a **batch**: **B3** (OPA framework, score the `opa test`/PyTest layers; mark the
  Chainsaw ArgoCD-reconcile layer twin-gated) → **B16-admission** (admission Rego only) → **B6-contract**
  (SDK contract + cross-language contract tests vs mocks) → **B9-shell** (CLI shell). Establish the
  **corner-rate dashboard** (defects-per-corner across builds: a `spec` spike means tighten the
  crucible; a `scenario` spike means AC-derivation is weak; a `judge` spike means recalibrate). Stand up
  the [C56 autonomy-ladder](../../implementation-dependencies.md) *language* so the human rung is named,
  and ride the cheap "are the goals still right?" drift checkpoint on every batch review
  ([decision #2 option A](../../../../decisions-to-make.md#2-the-is-it-still-doing-what-i-asked-watcher--build-it-or-just-log-that-its-missing)).
- **Exit.** 3–4 more factory-built `agent-os` components in their repos; a batched-review cadence that
  sustains one batch per review cycle; a fence-confirmed-before-unattended record; and a clear,
  evidence-backed answer to *"what does the factory need to build next to keep agent-os moving?"*

## 3. How defects get found — and how the finder is validated

The methodology is the triangle. The crucial addition the synthesis insists on: **the router is only as
trustworthy as its calibration.** `root_cause` is trustworthy not because the judge emitted it but
because the **Gate-1 human-labelled, all-five-corners sample** measured its agreement and false-green
rate. Until that clears the bar, oversight stays `full` and `tri_alignment` is advisory. The sample is
**re-run whenever the ledger logs a judge-disagreement event** — the instrument is continuously
re-checked, not certified once. This is the consuming, minimal-now version of the PF-2/C46 seam the
backbone names but defers.

| Corner | What a defect here means | Fix owner |
|---|---|---|
| **spec** | the C08 intake was ambiguous/wrong | spec intake ([C08](../../spec/C08-spec-artifact.md)/[C11](../../spec/C11-intent-intake.md)) — tighten the artifact |
| **scenario** | the held-out test was broken | scenario authoring ([C30](../../spec/C30-scenario-store.md)) — repair the probe |
| **system** | the build is wrong | the build loop ([C52](../../spec/C52-self-bootstrap.md)) — re-run |
| **judge** | the judge mis-diagnosed | judge calibration ([C32](../../spec/C32-judge-harness.md)) — re-audit the sample |
| **none** | aligned — *necessary, not sufficient*; still needs human-approve + integrity | — |

## 4. Longer horizon (named, not scheduled)

The gating question becomes *"what does `agent-os` need next that the factory can't yet build, and which
unbuilt component has become a hard prerequisite?"* — answered empirically by the Gate-4/5 ledger.

- **Digital twins ([C44/C45](../../implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit))
  become a hard prerequisite** the moment the backlog turns to infra-heavy Workstream-A components
  (operators, Helm installs, cluster policy). Twins convert the entire blocked A-backlog
  (A1/A5/A6/A7/A23 …) and the deferred runtime halves of B16/B6/B2 from un-scoreable to scoreable, and
  complete the fence's deferred half. This is almost certainly the **next factory-build after the first
  agent-os wave.**
- **C46 (judge-calibration / FP-measurement harness) becomes a hard prerequisite before
  `oversight_level = sampled`** — relaxing human review *requires* a calibrated judge.
- **The objective-drift watcher ([F54](../../F-MODE-COVERAGE.md)) becomes a hard prerequisite before any
  lights-out rung** — the cheap human checkpoint suffices only while a human reviews in batches.
- Then the **CXDB trajectory store → self-heal chain** ([C21/C24](../../implementation-dependencies.md) →
  C36→C37→C38→C39) so the line diagnoses its own failures; **methodology experiments via
  [C55](../../spec/C55-methodology-experiment.md)** used *per work-shape* (an install+configure formula
  for Workstream-A once twins exist; a custom-Python/contract-first formula for Workstream-B) — GF-M is
  the *cheapest first experiment, not the winner*; and finally the sequential **self-optimization tail**
  (C46→C47→C48→C50, with counterfactual replay C49 kept experimental per
  [decision #3](../../../../decisions-to-make.md#3-the-hardest-unsolved-piece--replaying-a-run-with-one-thing-changed)).

## 5. Top risks the unified plan carries (and its bets)

1. **The judge can't be calibrated cheaply.** If the human-labelled sample shows a stubborn false-green
   rate, `tri_alignment` stays advisory and the factory is stuck at `oversight_level = full` — slower,
   but *honest*. Bet: full oversight on infra-light builds is affordable for these weeks.
2. **Prevent-vs-detect comes back "detect."** Then C34/C43 are weaker than the design assumes; the
   compensating audit gate (Gate 2) is the mitigation, and every `go` is annotated with the weaker
   trust level.
3. **The clusterless backlog runs out and the line starves on twins.** After ~6–8 B-components, the
   highest-value `agent-os` work is twin-gated. Bet: that starvation point is exactly the signal that
   makes twins (C44) the unambiguous next factory-build — a *good* problem that the ledger surfaces.
4. **Single-Max-seat cost throttles the line.** Mitigation: Gate 3 measures per-build cost; Gate 5
   fan-out width is governed by that number, not by ambition.

## 6. Provenance (what each parent plan contributed)

- **From [A — velocity](./plan-A-velocity.md):** drive one trustworthy nail first; B12 as the first
  code build; calibration as a *precondition*, not an afterthought.
- **From [B — de-risk](./plan-B-derisk.md):** the rigorous all-five-corners judge-calibration gate and
  the PF-2/C46-gap finding; the adversarial holdout leak probe; quantify cost before fan-out;
  `tri_alignment` advisory-until-calibrated.
- **From [C — yield](./plan-C-yield.md):** B22 (design-only, zero upstreams) as the very first run; the
  dependency-ordered clusterless slice (B3 → B16-admission → B6-contract → B9-shell); parallel rigs +
  batched-review cadence; the corner-rate dashboard; component-splitting at the admission/runtime seam.
