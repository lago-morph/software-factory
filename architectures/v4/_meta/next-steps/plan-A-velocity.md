# Plan A — Velocity / bootstrap-first ("prove the thesis fast")

> Lens: minimize time-to-first-trustworthy-real-self-build. Bias toward the smallest path that
> proves *the factory builds a real `lago-morph/agent-os` component we trust*. Grounded entirely in
> [the shared grounding brief](./00-grounding-and-exemplar.md); this is an *alternative* to its
> [Part B exemplar](./00-grounding-and-exemplar.md#part-b--exemplar-draft-plan-the-format-model-authors-produce-alternatives), not a copy.

## 1. Thesis

The backbone exists to make exactly one thing possible: the first safe self-build of *real* software,
ratified at the [C53 bootstrap-validation milestone](../spec/C53-bootstrap-validation.md). So the next
2–3 weeks should drive a **single load-bearing nail all the way through** — pick **one** infra-light
agent-os component ([B12, the CloudEvent schema registry](../../../../tmp/agent-os/specs/components/B/spec-B12.md)),
build it end-to-end, and pass it through C53's four-term gate. Everything that does not move that nail
(breadth, methodology experiments, autonomy-ladder vocabulary, self-heal, twins) is deferred. The
fastest way to find the factory's real defects is to *try to ship one real thing and watch the
[triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md) route
every divergence to a corner.*

## 2. Milestone-ordered spine (gates, not day-counts)

### Gate 0 — Substrate truth + the eval loop, in one pass
**Goal.** Discharge the make-or-break caveat and prove the eval tier runs — together, because they
share the same first `claude`-in-a-rig setup, so splitting them wastes a gate.
**Actions.** (a) Re-confirm the [Gas City conformance result and prevent-vs-detect](./00-grounding-and-exemplar.md#a2-the-make-or-break-caveat-that-must-be-discharged-first):
does `gc` *physically refuse* an out-of-partition read, or only audit it after? Record the answer —
holdout integrity (C34) and the fence (C43) are strictly weaker if it is detect-only. (b) Author the
minimal **3-step C12 formula** (spec-in → build → judge) and run *one* trivial pass to prove
scenario → run (C31) → diagnose (C32) → satisfaction (C33) is green end-to-end.
**Exit.** A one-page "substrate truth" note (prevent or detect, recorded) **and** a green 3-step loop.

### Gate 1 — Calibrate the judge against the triangle *before* trusting it on real work
**Goal.** The C53 gate's Term 2 is `tri_alignment = aligned`, which requires `root_cause = none`, and
its oversight relaxation is gated on `judge_self_trust = calibrated`
([C53 §3.2](../spec/C53-bootstrap-validation.md)). If the judge mis-localizes defects, every later
verdict is built on sand. So calibrate *first*.
**Actions.** Against B12's already-written acceptance criteria (e.g. AC-B12-02: a non-Canon namespace
must be rejected; AC-B12-03: a schema missing `specversion`/`schemaVersion` must fail), author a small
held-out scenario set, then **deliberately inject one defect per corner**: a spec defect (ambiguous
namespace ownership), a scenario defect (a broken assertion), and a system defect (a stubbed
validator). Confirm the judge's `DiagnosisRecord.root_cause` localizes each to the right corner.
**Exit.** A judge that demonstrably routes all three injected defects correctly — i.e. a defensible
`judge_self_trust = calibrated` precondition — plus the first three rows of the defect ledger.

### Gate 2 — The first real self-build: B12 through C53
**Goal.** The bet-#3 moment: does *factory-builds-factory* work on real work?
**Actions.** Feed the real [B12 spec+plan](../../../../tmp/agent-os/specs/components/B/spec-B12.md)
through the factory: build it into its own repo (C52), with held-out scenarios (C30) derived from
B12's ACs (AC-B12-01..09) and its PyTest test strategy — **no cluster, no Chainsaw, no Playwright
required** (B12 §8: Chainsaw N/A, Playwright N/A). Run it through the
[C53 four conjunctive terms](../spec/C53-bootstrap-validation.md): 100% hold-out floor, tri-alignment,
human-review approve, post-deploy factory-integrity check.
**Exit.** A recorded `go`/`no_go` on the `factory_build` bead with its evidence bundle, **and a real,
passing B12 repo.** On `no_go`: iterate the spec and re-run within `max_attempts`; if it persists, the
honest finding is *the factory needs more substrate before Phase 3* (the plan's accepted fail branch).

### Gate 3 — Provoke each defect class deliberately (still on B12 and its neighbors)
**Goal.** Exercise to *find* defects, not to add features. Coverage of defect *classes* beats count.
**Actions.** Push targeted probes: an **ambiguous-spec** run (B12's R2/R3 — `[PROPOSED]` event-type
names and `platform.capability.changed` payload fields are deliberately under-specified, a real
ambiguity the intent crucible should surface); an **adversarial holdout-leak** attempt (does C34 hold
under whatever prevent-vs-detect reality Gate 0 found?); and a **should-fail** run against an
infra-heavy A-component to confirm the [digital-twin gap (C44, deferred)](./00-grounding-and-exemplar.md#a0-the-real-target-product-lago-morphagent-os-this-is-what-the-factory-is-for)
*correctly bounds* what the factory can build. Tag every divergence in the ledger by corner.
**Exit.** A populated defect ledger and a named list of the top substrate gaps (twins almost certainly
among them) — the input to "what does the factory need to build next?"

## 3. How defects get found and fixed — the triangle + a routed ledger

Defects are found by *trying to ship B12* and reading every divergence through the
[spec↔scenarios↔system triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md).
The judge is a **diagnostician, not a scorer** (C32): on a failure it returns a `DiagnosisRecord` with
`root_cause ∈ {judge, spec, scenario, system, none}`. That turns "the factory has bugs" into a
*routable* signal. The **defect ledger** has one column = one corner, each entry a fix owner:

| Corner | What it means | Fix owner |
|---|---|---|
| **spec** | C08 intake was ambiguous/wrong | spec-intake (C08/C09) — tighten the artifact |
| **scenario** | the held-out test was broken | scenario authoring (C30) — repair the probe |
| **system** | the build is wrong | the build loop (C52) — re-run |
| **judge** | the judge mis-scored | judge calibration (C32) — re-audit the sample |
| **none** | aligned — necessary, not sufficient; still needs human approve + integrity | — |

Calibrating the judge in **Gate 1** *before* the real build is the load-bearing move: a `judge`-corner
defect discovered during Gate 2 would invalidate the very verdict that ratifies bet #3.

## 4. Longer horizon (named, not scheduled)

The gating question becomes *"what does agent-os need next that the factory can't yet build?"* The
ledger from Gate 3 answers it empirically. Almost certainly **[digital twins (C44/C45)](../implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit)**
— they unlock the infra-heavy Workstream-A components (operators, Helm, cluster policy) *and* complete
the fence's deferred half. From the [ranked top-ten](../implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit),
grab the near-free wins *as* breadth resumes (C07 glossary, C25 OTLP, C10 EARS linter). Then the
**CXDB trajectory store (C21/C24)** opens the back half — self-heal (C36→C37→C38→C39). Only then
**[methodology-as-config (C55)](../spec/C55-methodology-experiment.md)**: run GF-M and other v3
formulas as *experiments* to learn which formula best builds which agent-os workstream — "GF-M first"
means *cheapest to stand up*, not *the winner*. The **objective-drift detector (F54)** is a hard
prerequisite *before* any lights-out rung, once the factory grinds through agent-os components
unattended.

## 5. Top 3 risks my lens accepts

1. **Single nail = single point of failure.** Betting the whole window on B12 means a B12-specific
   quirk could stall everything. *Mitigation:* B12 is chosen precisely because it is the lowest-blast-
   radius real build (pure JSON-Schema + Python, PyTest-only, no cluster); if it stalls on a *spec*
   ambiguity rather than a factory defect, that is itself the most valuable early finding, and B3 is
   the held-in-reserve fallback (deferred only because its AC-B3-10 needs ArgoCD/Gatekeeper reconcile).
2. **Deferring breadth hides systemic defects that only appear across varied work.** A single build can
   pass while the factory is brittle. *Mitigation:* Gate 3 deliberately injects *varied* probe shapes
   (ambiguous spec, holdout-leak, should-fail infra-heavy) against B12's neighborhood — class coverage
   without paying for full breadth.
3. **Prevent-vs-detect comes back "detect."** Then C34/C43 are weaker than assumed and the first
   self-build is less trustworthy than the `go` implies. *Mitigation:* Gate 0 records this as a fact,
   not an assumption; if detect-only, the fence's trust is explicitly downgraded and the human-review
   term of C53 stays at `oversight_level = full` regardless of judge calibration.

## 6. The 3 biggest differences from the exemplar

1. **One nail, not a fan-out.** The exemplar widens to 3–4 components (B16/B6/B9/B19) in Gate 4 inside
   the window; I **cut Gate 4 entirely** and spend the saved time hardening *one* trustworthy build.
   Breadth is longer-horizon, not in-window.
2. **Calibrate the judge BEFORE the real build, as its own gate.** The exemplar treats judge
   mis-calibration as risk #3 and seeds defects *alongside* the first loop. I make judge calibration a
   *precondition gate* (Gate 1) — because [C53 Term 2 + `judge_self_trust`](../spec/C53-bootstrap-validation.md)
   make an un-calibrated judge fatal to the very verdict that ratifies bet #3.
3. **Commit to B12 and explicitly defer B3 + C56.** The exemplar hedges B12/B3 and stands up C56
   autonomy-ladder language in-window. I pick **B12** outright (B3's AC-B3-10 cluster-reconcile is not
   infra-light) and **skip C56** for the window — naming the human-in-the-loop rung is ceremony that
   does not move the nail; `oversight_level = full` already covers it.
