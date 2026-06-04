# Panel review 02 — Safety & security hawk

> Reviewer 2 of 6. Angle: AI-agent security, prompt-injection, supply-chain, self-modifying-system
> risk. Target: [`10-unified-plan.md`](../10-unified-plan.md). Grounded in
> [the brief](../00-grounding-and-exemplar.md), [`C43`](../../../spec/C43-isolation-boundary.md),
> [`C34`](../../../spec/C34-holdout-integrity.md), [`C53`](../../../spec/C53-bootstrap-validation.md),
> [`F-MODE-COVERAGE`](../../../F-MODE-COVERAGE.md), [`decisions-to-make.md`](../../../../../decisions-to-make.md).

## 1. Verdict

**`accept-with-named-amendments`.**

The plan's spine is safety-sound and, in two places, *more* honest than the exemplar: it makes judge
calibration a precondition gate (Gate 1), holds `oversight_level = full` until a stated false-green bar
clears, and keeps `tri_alignment` advisory-until-calibrated. That sequencing directly respects the
load-bearing fact that the backbone ships `judge_self_trust = uncalibrated`
([C53 §"oversight_level"](../../../spec/C53-bootstrap-validation.md), L420–421). I cannot accept it
as-is, though, because the plan's treatment of the fence **understates a binding operator decision
made after the parent plans were written** (D-30), and because the blast radius of the first self-build
is not actually bounded by anything the plan names. These are fixable with named amendments, not a
rewrite.

## 2. Top 3 named amendments

**A1 — The fence is a hard PREVENT gate, not a recordable trust annotation. (highest severity)**
*Problem:* the plan treats prevent-vs-detect as something you *record and annotate the `go` with*
(Gate 0 exit "prevent or detect, recorded"; risk #2 "every `go` is annotated with the weaker trust
level", L188–189). *Cited fact:* [`C43 §3.2`](../../../spec/C43-isolation-boundary.md) quotes
**review-log D-30 (ADOPTED 2026-06-01)**: unattended (P2) and self-modification (P3b) **require the
substrate to BLOCK — not merely detect** — out-of-boundary access; "until prevention is established
(native or watcher), unattended operation is blocked (human-in-the-loop)." Detect-only does not
license a weaker-trust unattended run; it **forbids** the unattended run until a blocking watcher is
added. *Fix:* rewrite Gate 5's fence precondition and risk #2 to state that a detect-only spike result
**blocks Gate 5's parallel-rig batches entirely** (work stays at human-in-the-loop) until either native
prevention is confirmed or the D-30 blocking watcher is built — the watcher being a *new build the plan
must surface as a possible Gate-5 blocker*, not a footnote.

**A2 — Bound the first self-build's blast radius with an *owned* post-deploy integrity harness.**
*Problem:* Gate 3 lists "post-deploy factory-integrity" as the fourth C53 term but assumes it exists.
*Cited fact:* [`C53 §"NEW SEAM"`](../../../spec/C53-bootstrap-validation.md) (L786) — the
`IntegrityResult` harness that runs the factory's baseline suite after a self-build integrates is an
**unowned seam ("owner TBD: C52 or a new component")**. A self-modification can break the factory's own
pipeline *after* a provisional `go` (AC-C53-18, L753). On a self-modifying system the rollback trigger
is the blast-radius bound; if no component owns it, Term 4 is paper. *Fix:* make standing up (even a
minimal) integrity-check + rollback harness an explicit Gate-3 exit criterion, before B12 is the first
real code self-build.

**A3 — The holdout probe must cover the WRITE/authoring path, not just the read.**
*Problem:* Gate 2's leak probe only instructs a worker to *read* `scenarios/` (L88–90). *Cited fact:*
[`C34 §1.2`](../../../spec/C34-holdout-integrity.md) (D-44/D-45, E-C34-09) — the anti-gaming property
extends to "worker can't drive its own spec/scenario relaxation"; once C52 self-build loops route
`root_cause ∈ {spec,scenario}` corrections, a worker that can *influence* a correction request degrades
"fix the spec" into "weaken the spec until my output passes." [`C34`'s G21](../../../spec/C34-holdout-integrity.md)
is a *major* gap: read-isolation is "config + discipline," audit is detect-after-the-fact. *Fix:* add a
second Gate-2 probe — a worker attempting to author/influence a `{Spec,Scenario}CorrectionRequest` — and
record whether the correction-provenance audit (E-C34-09) blocks or merely flags it.

## 3. The single highest-severity gap

**The plan's fence treatment contradicts D-30 and so under-protects the exact window the operator
already ruled unacceptable.** The factory is self-modifying and Gate 5 opens *parallel* rigs running
unattended batches. Per [decision #1](../../../../../decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after)
and the binding D-30 escalation, that window demands *prevention*. The plan instead carries a
detect-only outcome forward as an annotation on each `go`. If the D-23 spike returns "detect," the plan
as written would still run Gate 5 — precisely the "we noticed after it happened" failure mode the
operator rejected. This compounds because the first products are **agent-os security components that
themselves encode policy** (B3 OPA/Rego, B16 admission Rego): an uncalibrated judge greenlighting a
mis-built *policy engine* is a second-order trifecta — the factory could ship a permissive Rego default
and route every later build through it. Gate 1's calibration gate mitigates the *judge* half; only a
real PREVENT fence mitigates the *blast-radius* half. They must both hold before Gate 5, conjunctively.

## 4. What the plan gets right on safety (preserve this)

- **Calibration as a precondition gate (Gate 1), not a smoke test**, with explicit **false-green-rate**
  measurement and `oversight_level = full` until a bar clears — this honors
  [`C53`](../../../spec/C53-bootstrap-validation.md) L421 (`uncalibrated` forces `full`) exactly.
- **The all-five-corners human-labelled sample, re-run on every judge-disagreement event** — a
  continuously-rechecked instrument, not a one-time certificate. Preserve this verbatim.
- **Trust sequencing: substrate truth (Gate 0) → calibrate → one nail → line.** The order is the safety
  property; do not let velocity pressure collapse Gate 1 into Gate 3.
- **The objective-drift checkpoint riding every batch review** ([decision #2 option A](../../../../../decisions-to-make.md#2-the-is-it-still-doing-what-i-asked-watcher--build-it-or-just-log-that-its-missing);
  [F54 Partial](../../../F-MODE-COVERAGE.md)) — correct *while* a human reviews in batches; the plan
  rightly names a real detector as a hard prerequisite before any lights-out rung (§4).
