# Panel review 3 — ML evaluation / measurement-science lens

> Reviewer angle: LLM-as-judge, eval design, calibration, Goodhart, statistical validity.
> Plan under review: [`../10-unified-plan.md`](../10-unified-plan.md). Grounding:
> [`../00-grounding-and-exemplar.md`](../00-grounding-and-exemplar.md).

## 1. Verdict

**`accept-with-named-amendments`.**

The plan's sequencing instinct is *measurement-correct*: it refuses to trust `root_cause` until the
judge is calibrated, keeps `tri_alignment` advisory, and holds `oversight_level = full`
([Gate 1 exit](../10-unified-plan.md#gate-1--calibrate-the-judge-the-load-bearing-gate);
[C53 §3.3](../../spec/C53-bootstrap-validation.md)) — faithful to
[C32 OQ6](../../spec/C32-judge-harness.md), where the `judge_self_trust` seam is *named but not designed*
(sample size, agreement bar, and who writes the state are "NOT designed here … deferred to the C46
calibration harness"). But the *calibration measurement itself* is under-specified to the point of being
non-falsifiable, leaving statistical-validity holes that let an uncalibrated judge masquerade as calibrated.
Fixable by amendment, not rewrite — hence accept-with-amendments.

## 2. Top 3 named amendments

**A1 — "Clears a stated bar" is hand-wavy; specify the estimator, not just the threshold.**
*Problem:* Gate 1 gates on "a stated bar" whose "value and sample size are operator policy
`[PROPOSED — not in source]`"
([Gate 1](../10-unified-plan.md#gate-1--calibrate-the-judge-the-load-bearing-gate)). A bar on a *point
estimate* from a tiny all-five-corners sample is meaningless: a 5-class confusion matrix over ~20
trajectories puts ~4 per corner, so one mislabelled `none`-corner trajectory swings the false-green rate by
25 points. *Cited fact:* the only quantified bar in the corpus is
[C32 OQ1](../../spec/C32-judge-harness.md) (">15% FP rate" triggers FE-1) — a bare point threshold, no n,
no interval. *Fix:* report a **Wilson/Clopper–Pearson interval on the false-green rate and gate on its
*upper* bound**; pin a minimum-n *per corner* so the rare `none`-with-defect and `judge` corners are
estimable; report per-corner recall, since one aggregate "agreement" number hides exactly the false-green
class the plan calls "the most dangerous error."

**A2 — Who calibrates the calibrator? The human labeller is an un-audited single point of truth.**
*Problem:* The edifice rests on "human-authored ground-truth root-cause labels"
([Gate 1](../10-unified-plan.md#gate-1--calibrate-the-judge-the-load-bearing-gate)), but attribution across
{judge, spec, scenario, system, none} is *itself* the hard judgement
[ADR-0069](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md) calls a
"non-specific alarm … caused by a defect in *any* corner." A single fallible labeller has no measured
reliability, so "judge agrees with human" conflates judge error with label error. *Cited fact:* ADR-0069
names "judge fallibility … a first-class, named defect source" but is silent on *labeller* fallibility;
C32 OQ6 punts the human-agreement bar. *Fix:* require **≥2 independent labellers on a subset with an
inter-rater statistic (Cohen's/Fleiss' κ) reported alongside the judge bar**, and exclude
human-disagreement trajectories from the judge's denominator (you cannot score a judge against contested
ground truth). Without this, `calibrated` is unfalsifiable.

**A3 — Scenarios derived from a component's OWN acceptance criteria are not independently held-out.**
*Problem:* Gate 2 and Gate 3 author the held-out scenario set "from its ACs" / "from `AC-B12-01..06`"
([Gate 2](../10-unified-plan.md#gate-2--holdout-integrity-adversarially);
[Gate 3](../10-unified-plan.md#gate-3--the-first-real-code-self-build-b12-through-c53-honestly-gated-cost-measured)).
*Cited fact:* [ADR-0069 Decision table](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)
requires the S↔H edge be owned by "the **scenario builder working with the spec builder**" — independent of
the implementer — and the [C32 anti-gaming routing](../../spec/C32-judge-harness.md) (I10) bars the worker
from driving scenario/spec correction. Deriving H mechanically from the same ACs the System is built to
satisfy collapses S↔H and S↔I into one source: a spec ambiguity propagates *identically* into both the build
and the test, so the held-out set cannot detect it and `root_cause = spec` becomes structurally invisible.
*Fix:* name an **independent scenario-authoring step** (a separate rig/role, never the build worker) and
require scenarios that probe *beyond* the literal ACs (negative cases, boundary behavior the ACs don't
enumerate) — otherwise "held-out" means only "unread," not "independent."

## 3. The single biggest measurement-validity flaw

**The calibration step measures the judge against a sample too small and too single-sourced to support the
binary `calibrated` claim it gates on — it has no statistical power against the very error (false-green) it
exists to bound.** A 5-class confusion matrix with class imbalance (the dangerous `none`-with-hidden-defect
and `judge` corners are rare and hardest to author) over an unstated, almost-certainly-tiny n, scored
against a single un-audited labeller, cannot distinguish "judge is calibrated" from "we got lucky on four
trajectories." [C32 OQ6](../../spec/C32-judge-harness.md) admits the mechanism is undesigned; the plan
inherits the gap and dresses it as a gate. Compounding it: under [D-1](../../spec/C32-judge-harness.md) the
Phase-0 judge is **same-provider** (Claude judging Claude, F48 shared-distribution residual *Partial*), so
the most likely judge errors are *correlated* with the coder's — exactly what a small same-family
calibration sample is least able to surface. The plan should state plainly that until A1–A2 are discharged,
`calibrated` is *unreachable* and the factory stays at `oversight_level = full` — the conservative default it
already chose.

## 4. What the plan gets right on measurement (preserve)

- **Calibration as a hard *precondition gate*, not a smoke test**, with the explicit advisory-until-calibrated
  posture for `tri_alignment` ([Gate 1](../10-unified-plan.md#gate-1--calibrate-the-judge-the-load-bearing-gate)).
  Faithful to [C53 §3.3](../../spec/C53-bootstrap-validation.md) (`judge_self_trust = uncalibrated` forces
  `oversight_level = full`) — the single most important measurement decision in the plan.
- **Self-consistency of the 100% floor + a probabilistic judge.** The plan does *not* threshold a distribution:
  [C53](../../spec/C53-bootstrap-validation.md) makes the floor a **boolean** (`all_scenarios_satisfied`, pinned
  1.0, never lowered) while the satisfaction distribution is demoted to *diagnostic evidence*; only oversight
  relaxes. (Residual: the boolean derives from a per-scenario `score_label` cutline that is a
  [FAITHFUL-FILL placeholder in C32 §3.2](../../spec/C32-judge-harness.md) — the floor is only as crisp as that
  undocumented threshold.)
- **The judge-disagreement column feeding recalibration** ([Gate 4](../10-unified-plan.md#gate-4--provoke-each-defect-class-deliberately-populate-the-ledger))
  — continuous re-checking, not certify-once: the right anti-drift posture.
- **The corner-rate dashboard as a Goodhart tripwire** ([Gate 5](../10-unified-plan.md#gate-5--open-the-production-line-widen-only-behind-the-fence)):
  a `spec`/`scenario`/`judge` spike is read as *tighten the instrument*, not relax the bar — consistent with
  [ADR-0069](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)'s rejection of
  threshold-lowering as the Goodhart release valve. The cross-family judge requirement is correctly *preserved
  as FE-1*, not dropped; keep naming it as the trigger when same-family bias is measured material.
