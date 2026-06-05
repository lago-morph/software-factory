# Plan B — "De-risk the foundations first" (safety + measurement adversary lens)

> Companion to the [grounding brief + velocity exemplar](./00-grounding-and-exemplar.md). This is the
> *adversarial* alternative: same destination (real agent-os work, semi-autonomous build), but it refuses to
> trust a measurement instrument it has not calibrated, or a substrate guarantee it has not witnessed.

## 1. Thesis

The backbone's apex is a *measurement* event: [C53's four-term go/no-go](../../spec/C53-bootstrap-validation.md)
reads signals from the [spec↔scenarios↔system triangle](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md),
and three of its four terms are produced by an LLM judge and a substrate whose guarantees are **claimed, not
verified** ([A2](./00-grounding-and-exemplar.md#a2-the-make-or-break-caveat-that-must-be-discharged-first)).
A factory that builds real software on top of a lying instrument doesn't fail loudly — it ships defects with a
green verdict. So the first milestones spend cheaply to turn the four riskiest assumptions (prevent-vs-detect,
judge root-cause fidelity, holdout integrity, self-modification blast radius) into *witnessed facts* — and only
then do we point the calibrated instrument at agent-os's real backlog. We still ship real components; we just
refuse to trust the scoreboard before we've checked it against a known-answer game.

## 2. Milestone-ordered spine (gates, not day-counts)

**Gate 0 — Substrate truth, prevention-grade.** *Goal:* witness what Gas City actually enforces, not what v4
claims. *Actions:* re-run the [Gas City conformance check (C01 AC-2)](../../implementation-dependencies.md#gas-city--gc-binary-mit);
then the load-bearing sub-test — attempt a cross-partition read from inside a worker rig and record whether `gc`
**physically refuses it** or lets it through for an after-the-fact audit
([decision #4, prevent-vs-detect](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact)).
Run the same probe against the [holdout partition (C34)](../../spec/C34-holdout-integrity.md) — `scenarios ∉
read_partition(worker)` must hold by *refusal*, not by audit. *Exit:* a one-page "substrate truth" note stating
prevent **or** detect for both fences. If detect-only, every later gate inherits a written trust-downgrade.

**Gate 1 — Calibrate the judge before trusting any reading (the instrument-first gate).** *Goal:* prove the
judge's `root_cause` ∈ {judge, spec, scenario, system, none} localizes correctly *before* it adjudicates real
work. *Actions:* build a **known-answer calibration set** — a handful of builds where we have *deliberately and
secretly* planted exactly one defect in a known corner (one spec-ambiguity, one broken scenario, one system
bug, one clean build that should return `root_cause = none`). Run them through
[C32 `diagnose()`](../../spec/C32-judge-harness.md) and score the judge on *whether it named the corner we
planted*. This discharges the [PF-2 `judge_self_trust` precondition](../../spec/C32-judge-harness.md) with a
**human-audited sample**, not a self-declaration. *Exit:* a confusion matrix of planted-corner vs judge-named
corner; `judge_self_trust = calibrated` is set **only** if it routes cleanly. A judge that confuses *system*
with *spec* defects is recorded as uncalibrated, forcing `oversight_level = full` at C53.

**Gate 2 — First real loop end-to-end, on a real spec, with both defect-injections live.** *Goal:* prove the
eval tier runs end-to-end on real work. *Actions:* author the minimal **3-step C12 formula** (spec-in → build →
judge) over a real agent-os component's acceptance criteria — use the agent-os **B12 CloudEvent schema
registry** (clone at `/tmp/agent-os`) or **B3 OPA policy framework**: pure code, PyTest / `opa test`-scoreable,
*no Kubernetes*
([A0](./00-grounding-and-exemplar.md#a0-the-real-target-product-lago-morphagent-os-this-is-what-the-factory-is-for)).
Re-inject a spec defect and a scenario defect *on this real component* and confirm the now-calibrated judge
still routes them. *Exit:* green loop scenario → C31 runner → C32 judge → C33 satisfaction, with two
correctly-localized injected defects on real agent-os material.

**Gate 3 — Holdout-integrity adversary gate (before the first self-build counts).** *Goal:* prove the agent
*cannot* teach to the test. *Actions:* a red-team probe — instruct a worker to *attempt* to read the held-out
scenarios for B12, and confirm Gate-0's refusal holds end-to-end through the rig partition. Cross-check that the
judge runs in a [separate judge rig (D-38)](../../spec/C34-holdout-integrity.md) with no shared context window.
If Gate-0 came back detect-only, this gate's exit is *conditional*: holdout integrity is audit-grade, and the
first self-build's `go` carries that caveat in its evidence bundle. *Exit:* a recorded leak-attempt result;
holdout strength labeled prevent or detect.

**Gate 4 — The first real self-build through the four-term C53 gate.** *Goal:* the bet-#3 moment, on a
calibrated instrument. *Actions:* take B12's `spec-X.md` + `plan-X.md`, run [C52 self-bootstrap → the C53
four-term gate](../../spec/C53-bootstrap-validation.md#32-milestone-decision-rule-predicate-i3--bar-applied-here-reframed-to-tri-alignment):
**100% hold-out floor** ∧ **tri_alignment = aligned** ∧ **human approve** ∧ **post-deploy factory-integrity
pass**. The fourth term is non-negotiable here — a self-modification can green-light itself and break the
factory's own baseline suite. *Exit:* a recorded `go`/`no_go` with full evidence bundle and a passing,
real agent-os component repo — **and** the factory's baseline suite still green post-integration.

**Gate 5 — Fence up, then deliberately provoke each defect class.** *Goal:* find defects on purpose, safely.
*Actions:* confirm the [boundary-typing fence (C43) is up before any unattended batch (D-20)](../../../../decisions-to-make.md#1-put-the-safety-fence-up-before-the-factory-runs-unattended-or-after);
then push *varied* real agent-os work to provoke each corner: an ambiguous-spec B-component, a hard-upstream-dep
component, and one **infra-heavy A-component that *should* hit the digital-twin gap**
([A0 — twins bound how much agent-os is buildable now](./00-grounding-and-exemplar.md#a0-the-real-target-product-lago-morphagent-os-this-is-what-the-factory-is-for))
to confirm the limit holds rather than silently producing junk. Build the **defect ledger**: every divergence
tagged by corner with a fix owner. Re-run a slimmed judge-calibration spot-check at this gate — drift in the
instrument is itself a defect. *Exit:* populated defect ledger + the witnessed list of agent-os components the
factory *cannot* build until twins exist.

## 3. How defects get found — and how the defect-finder is itself validated

Defects are found by the triangle: every failing scenario is *attributed to a corner*, turning "the factory has
bugs" into a routable signal ([A3](./00-grounding-and-exemplar.md#a3-the-defect-finding-methodology-is-already-designed-the-triangle)).
But the adversarial point is that **the router is itself one of the corners** — a judge that silently mislabels a
*system* bug as a *spec* defect sends the fix to the wrong place and corrupts the whole loop. So `root_cause` is
trustworthy only after Gate 1's known-answer calibration: we *plant* defects in known corners and score the judge
on naming them, producing a confusion matrix that discharges [`judge_self_trust` (PF-2)](../../spec/C32-judge-harness.md)
with human-audited evidence rather than self-attestation. Two further adversarial pressures: (a) the
[same-provider judge (D-1)](../../spec/C34-holdout-integrity.md) shares the coder's blind spots, so the
calibration sample must include defects the coder's family is *prone to* (not just easy ones); (b) re-spot-check
calibration at Gate 5 — a judge trusted in week one can drift. Until the matrix is clean, C53 runs at
`oversight_level = full` and a `go` is never taken on satisfaction alone. What makes `root_cause` trustworthy is
exactly this: a recorded match between *planted* corner and *named* corner, re-checked over time — not the
judge's own confidence.

## 4. Longer horizon (named, not scheduled)

The gating question stays "what does agent-os need next that the factory can't yet build?" — and Gate 5 will
have *witnessed* the answer: **[digital twins (C44/C45)](./00-grounding-and-exemplar.md#a5-the-evolution-path-how-the-rest-of-the-57-components-get-added)**
become a hard prerequisite the moment infra-heavy Workstream-A components (operators, Helm installs, cluster
policy) enter the backlog — and twins complete the fence's deferred half, so they are *also* a safety
prerequisite, not only a capability one. The **[objective-drift watcher (F54)](../../../../decisions-to-make.md#2-the-is-it-still-doing-what-i-asked-watcher--build-it-or-just-log-that-its-missing)**
becomes a hard prerequisite *before any lights-out rung* — fine as a human checkpoint while review is batched,
unacceptable once dozens of agent-os components grind through unattended. Then the
[CXDB/self-heal arc (C21/C24 → C36→C39)](./00-grounding-and-exemplar.md#a5-the-evolution-path-how-the-rest-of-the-57-components-get-added),
[methodology-as-config experiments (C55)](../../spec/C55-methodology-experiment.md) — GF-M is "first experiment,
not winner" — and the genuinely-sequential self-optimization tail (C46→C50, with C49 kept experimental).

## 5. Top 3 risks the velocity exemplar under-weights

1. **The judge is treated as trustworthy from its first gate; calibration is listed as a *mitigation*, not a
   *gate*.** The exemplar's risk #3 names judge mis-calibration but lets the first real loop run before the
   known-answer audit. *Mitigation:* Gate 1 *blocks* — no reading is trusted before the confusion matrix is
   clean, and the [same-provider-judge blind spot (D-1)](../../spec/C34-holdout-integrity.md) is explicitly
   stress-tested.
2. **Prevent-vs-detect is treated as a footnote that adjusts "trust," not a gate that changes what counts as a
   pass.** If [Gas City is detect-only (decision #4)](../../../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact),
   holdout integrity is audit-grade and the agent *could* have read the answers before we noticed. *Mitigation:*
   Gate 0 + Gate 3 make this a *witnessed* property that stamps a caveat onto every downstream `go`.
3. **Single-Max-seat cost fan-out is dismissed as "slow," not as a forcing function for restraint.** Running
   candidates × work-types × scenarios × the calibration sample through one judge seat is
   [multiplicative token cost with no number attached (A6)](./00-grounding-and-exemplar.md#a6-hard-constraints--known-risks-the-plan-must-respect).
   *Mitigation:* keep fan-out incremental; the calibration set is small-and-known by design; quantify cost
   before any full grid at Gate 5.

## 6. The 3 biggest ways this plan differs from the exemplar

1. **A dedicated judge-calibration gate (Gate 1) is inserted *before* the first real loop.** The exemplar
   injects defects only to *observe* the triangle working; this plan *scores the judge on a known-answer set*
   and makes `judge_self_trust = calibrated` a precondition, not a hope.
2. **Substrate truth is reordered into a hard gate whose result rewrites every later exit criterion.** The
   exemplar's Gate 0 produces a note; here the prevent-vs-detect outcome propagates a written trust-downgrade
   into the holdout gate and into the C53 evidence bundle.
3. **An explicit holdout-integrity adversary gate (Gate 3) sits between the first loop and the first counted
   self-build** — the exemplar folds leak-attempts into a later "exercise" gate, *after* the bet-#3 self-build
   has already been trusted.
