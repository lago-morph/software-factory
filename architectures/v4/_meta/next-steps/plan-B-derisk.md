# Plan B — "De-risk the foundations" (safety + measurement adversary)

> Lens: assume the things most likely to lie are (a) the unverified Gas City "native" claims
> (prevent vs detect), (b) the **judge** corner of the triangle, (c) holdout integrity, and
> (d) self-modification blast radius before the fence. Front-load the cheap checks that turn
> assumptions into facts, and **calibrate the measurement instrument before trusting its readings.**
> This plan still ships real [agent-os](../../../../) work — it just refuses to trust a green light
> it has not yet earned the right to read.

## 1. Thesis

The backbone gives us a measurement instrument (the spec↔scenarios↔system
[triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)) and a
go/no-go gate ([C53](../../spec/C53-bootstrap-validation.md)) — but an instrument you have not
calibrated is not evidence, it is a *rumor with a number on it*. The next 2–3 weeks should
**discharge the three unverified foundations first** (substrate prevent-vs-detect, judge
calibration, holdout integrity), *then* drive a real agent-os component through the gate. The
velocity-first exemplar is right that the work must be real and right to drive at
[C53](../../spec/C53-bootstrap-validation.md); it is over-optimistic in treating the judge's
`root_cause` as trustworthy after a single inject-and-confirm, when the `judge_self_trust`
precondition is *undesigned* and ships `uncalibrated` by default.

## 2. Milestone-ordered spine (gates, not day-counts)

### Gate 0 — Substrate truth: prevent vs detect (cheapest, first)
- **Goal.** Replace the single biggest assumption in the design with a fact before any signal is
  trusted ([decision #4](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)).
- **Actions.** Stand up one `claude` worker rig + one judge rig (per
  [D-38 separate-judge-rig](../../spec/C32-judge-harness.md)); attempt a cross-partition read of the
  scenario partition *and* a production-typed action. Record whether each is **physically refused**
  (prevent) or **audited after the fact** (detect). Confirm attribution flows into beads.
- **Exit.** A one-page "substrate truth" note. If **detect-only**, holdout
  ([C34](../../spec/C34-holdout-integrity.md), described as "after-the-fact AUDIT") and the fence
  ([C43](../../spec/C43-isolation-boundary.md)) are *strictly weaker* — every later gate's trust
  level is annotated accordingly, and Gate 2 cannot rely on the holdout to stop teach-to-the-test.

### Gate 1 — Calibrate the judge *before* reading it (the load-bearing gate)
- **Goal.** Earn the right to trust `root_cause` / `tri_alignment`. This is the gate the exemplar
  skips. The backbone ships the judge with `judge_self_trust = uncalibrated`
  ([C32 §3.2](../../spec/C32-judge-harness.md)), and **PF-2 — the mechanism that establishes
  `calibrated` — is explicitly undesigned and deferred to C46**, which is *not in the backbone*
  ([C32 OQ6](../../spec/C32-judge-harness.md)). So "the triangle works" is unproven by construction.
- **Actions.** Build a **judge-calibration sample**: a small fixed set of trajectories with
  *human-authored ground-truth root-cause labels*, deliberately spanning all five corners
  (`judge / spec / scenario / system / none`). Run the judge; compute agreement vs the human labels.
  Cover the high-stakes confusions explicitly — a `system` bug mislabelled `spec`, or a real defect
  mislabelled `none` (a false green). Cross-check against the C32 ACs that already enumerate each
  path ([AC-C32-16..23](../../spec/C32-judge-harness.md)).
- **Exit.** A recorded judge false-positive rate. Until agreement clears a stated bar, the factory
  runs at `oversight_level = full` ([C53 §3.3](../../spec/C53-bootstrap-validation.md)) and **no
  `tri_alignment = aligned` is treated as load-bearing** — it is advisory only. A mis-localizing
  judge silently corrupts the *entire* defect-finding loop, so this is the instrument-calibration
  step that makes every later reading meaningful.

### Gate 2 — Holdout integrity, adversarially (not assumed)
- **Goal.** Confirm the agent cannot teach to the test — the thing that would make every
  satisfaction score a lie. F28 "holdout leakage" is marked *Addressed*
  ([F-MODE-COVERAGE §1](../../F-MODE-COVERAGE.md)) but that rests on the same unverified substrate.
- **Actions.** Author a held-out scenario set from a real agent-os component's ACs (see Gate 3).
  Run a deliberate **leak probe**: instruct a worker to read `scenarios/<component>/`; confirm the
  read is refused (if Gate 0 said *prevent*) or at minimum audited and flagged (if *detect*). Verify
  `scenarios ∉ read_partition(worker)` per [C34](../../spec/C34-holdout-integrity.md).
- **Exit.** A recorded holdout-integrity verdict. If detect-only, add the compensating control named
  in [decision #4 option B](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)
  (post-run audit gate) *before* any score is trusted as un-gamed.

### Gate 3 — First real self-build, gated honestly
- **Goal.** The bet-#3 moment — does factory-builds-factory work on real work? — but read through a
  *calibrated* instrument.
- **Actions.** Take **agent-os [B12 CloudEvent schema registry](../../../../)** (pure JSON-Schema +
  Python, PyTest-scoreable, no cluster — confirmed in `/tmp/agent-os/specs/components/B/spec-B12.md`)
  or **B3 OPA policy framework** (`opa test`) as input. Build into its own repo; score against
  held-out scenarios from its ACs; run the **four-term C53 gate**: 100% hold-out floor ∧
  `tri_alignment = aligned` ∧ human-approve ∧ post-deploy factory-integrity
  ([C53 §3.2](../../spec/C53-bootstrap-validation.md)).
- **Exit.** A recorded `go`/`no_go` with evidence **and** the Gate-1 calibration verdict attached, so
  the `go` is auditable as more than "the judge said so." A passing agent-os component repo.

### Gate 4 — Provoke each defect class; populate the ledger
- **Goal.** Find defects deliberately, and confirm the (now-calibrated) judge routes each to the
  right corner.
- **Actions.** Push varied real agent-os work: an ambiguous-spec component (provoke `root_cause =
  spec`), an infra-heavy A-component that *should* trip the twin gap (confirm the fence/limits hold,
  not a false green), and a re-run of the Gate-1 leak probe under load. Build the **defect ledger**:
  every divergence tagged by corner with a fix owner — and **a fifth column for judge-disagreement
  events** (cases where human review overruled `root_cause`), feeding back into recalibration.
- **Exit.** A populated defect ledger; the top-3 substrate gaps the factory can't yet build around
  (twins near-certainly among them); an updated judge FP rate.

### Gate 5 — Widen only behind the fence
- **Goal.** A safe batched rhythm — never unattended without the fence.
- **Actions.** Confirm the **fence (C43) is up before any unattended batch**
  ([decision #1](../../../../decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after)).
  Run 2–3 more infra-light B-components (B16 policy content, B6 SDK, B9 CLI, B19 approval schemas
  downstream of B12). Stand up [C56](../../implementation-dependencies.md) autonomy-ladder language
  so the human rung is named, and ride the cheap "are the goals still right?" drift checkpoint on
  every batch review ([decision #2 option A](../../../../decisions-to-make.md#2-the-is-it-still-doing-what-i-asked-watcher--build-it-or-just-log-that-its-missing)).
- **Exit.** 3–4 factory-built agent-os components in their repos; a batched-review rhythm; a
  fence-confirmed-before-unattended record.

## 3. How defects get found — and how the defect-finder is itself validated

Defects are found by the [triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md):
every divergence is *attributable to a corner* (spec / scenario / system / judge), routed by the
judge's `DiagnosisRecord.root_cause`. **But the routing is only as trustworthy as the router.** What
makes `root_cause` trustworthy is *not* that the judge emitted it — it is the **Gate-1 calibration
sample**: a human-labelled, all-five-corners ground-truth set, with a measured agreement rate and an
explicit false-green check (`root_cause = none` on a build that actually has a defect). Until that
rate clears the bar, `judge_self_trust` stays `uncalibrated`, oversight stays `full`, and
`tri_alignment = aligned` is advisory, never a deploy authority. The sample is re-run whenever the
ledger logs a judge-disagreement event (Gate 4) — the instrument is *continuously* re-checked, not
certified once. This is the consuming side of [C32 OQ6 / PF-2](../../spec/C32-judge-harness.md): the
seam the backbone names but does not design, which this plan designs a minimal human-audited version
of. `[PROPOSED — not in source]` the exact agreement bar and sample size are operator policy.

## 4. Longer horizon (named, not scheduled)

The gating question becomes "what does agent-os need next that the factory can't yet build, and which
unbuilt safety component has become a *hard* prerequisite?"

- **Digital twins ([C44/C45](../../implementation-dependencies.md)) become a hard prerequisite** the
  moment the backlog turns to infra-heavy Workstream-A components (operators, Helm installs, cluster
  policy) — they cannot be scored without a twinned or real `kind` cluster, and twins also complete
  the fence's deferred half.
- **The objective-drift watcher ([F54](../../F-MODE-COVERAGE.md)) becomes a hard prerequisite
  *before* any lights-out rung** — the cheap human checkpoint
  ([decision #2](../../../../decisions-to-make.md#2-the-is-it-still-doing-what-i-asked-watcher--build-it-or-just-log-that-its-missing))
  suffices only while a human reviews in batches.
- **C46 (judge-FP measurement / calibration harness) becomes a hard prerequisite before
  `oversight_level = sampled`** — relaxing human review *requires* a calibrated judge, and C46 is the
  named owner of the FP-rate trigger for cross-family judging (FE-1).
- Then the **CXDB → self-heal chain** (C21/C24 → C36→C37→C38→C39), **methodology experiments via C55**
  (GF-M is *first*, not *winner*), and the sequential **self-optimization tail** (C46→C47→C48→C50,
  C49 kept experimental per [decision #3](../../../../decisions-to-make.md#3-the-hardest-unsolved-piece--replaying-a-run-with-one-thing-changed)).

## 5. Top 3 risks the velocity exemplar under-weights

1. **The judge is uncalibrated by construction, and the exemplar trusts it after one inject-test.**
   The exemplar's Gate 1 "inject a spec defect and a scenario defect, confirm `root_cause` localizes
   each" is a *two-sample smoke test*, not calibration — it never measures the false-green rate
   (`root_cause = none` on a defective build) and never establishes `judge_self_trust = calibrated`
   ([C32 OQ6](../../spec/C32-judge-harness.md)). **Mitigation:** Gate 1's all-five-corners
   human-labelled sample with a recorded FP rate, gating oversight relaxation.
2. **Holdout integrity is assumed "Addressed," but rests on unverified prevent-vs-detect.** If the
   substrate only *detects*, the agent can read the test answers and you learn it from the audit log
   — every satisfaction score upstream is then suspect. **Mitigation:** Gate 0 + Gate 2 adversarial
   leak probe, with a compensating audit gate if detect-only.
3. **Single-Max-seat cost is multiplicative and the exemplar widens before quantifying it.** A
   judge-calibration sample plus an *ensemble* judge multiplies calls (`n_judges × trajectories`) on
   the seat shared with the coder, with no token-budget model in v4
   ([C32 OQ3](../../spec/C32-judge-harness.md)). **Mitigation:** quantify cost on the Gate-3 single
   build before any Gate-4/5 fan-out; keep fan-out incremental.

## 6. The 3 biggest ways this plan differs from the exemplar

1. **It inserts a dedicated judge-calibration gate (Gate 1) *before* the first self-build** and makes
   `tri_alignment` advisory-until-calibrated — where the exemplar folds calibration into a two-sample
   smoke test inside its first formula gate and trusts the result immediately.
2. **It treats holdout integrity as a thing to *break on purpose* (Gate 2 leak probe), not a property
   to assume** — the exemplar lists holdout-leak as one item in a later "exercise to find defects"
   gate, after it has already trusted the scores.
3. **It quantifies single-seat cost on the first build and gates fan-out on that number**, rather than
   widening to 3–4 components and only noting cost as a residual risk afterward.
