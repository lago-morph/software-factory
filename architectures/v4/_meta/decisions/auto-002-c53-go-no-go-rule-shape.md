# auto-002 — C53 first-self-build go/no-go rule shape

**Status:** Round-2 pending · **flagged as a MORNING-REVIEW item (operator sign-off required before the C53 milestone is armed).** · **REFRAMED 2026-06-02 by the spec–scenarios–system triangle (D-42 / D-43 / ADR-0069): this go/no-go rule is now understood as the *H↔I edge* within a larger *tri-alignment* completion criterion — see the "## Update" section below. The C′ statistics become diagnostic *evidence*, not the gate; the binding gate is the four conjunctive tri-alignment terms in C53 §3.1.**
**Author:** Lead agent, autonomous-run 2026-06-01. **Owner of the decision:** operator (jonathan@manton.com).
**Context:** [`C53-bootstrap-validation.md`](../../spec/C53-bootstrap-validation.md) §3.1; [`C33-satisfaction-metric.md`](../../spec/C33-satisfaction-metric.md) (the `SatisfactionDistribution` C53 reads); panel verdict [`panel-sweep2/VERDICT.md`](../panel-sweep2/VERDICT.md).

## Question

What is the **decision-rule SHAPE** of the bootstrap-validation milestone — the predicate over C33's satisfaction distribution that, together with the human design-review verdict, decides go/no-go for the **first component the factory builds for itself**? (The threshold *values* are operator policy and not in scope here — only the shape: *which* statistics gate the apex of bet #3.)

This is a genuine operator-judgment / safety-governance fork, not a mechanical engineering choice: a `mean`-only rule and a `p10 + mean + std_dev` rule both have defensible arguments, but only one is in force at the first self-modification checkpoint.

## Alternatives (≥3 named)

- **A — `mean ≥ T_central` only.** Simplest. *Rejected:* a consistently bad tail passes (Goodhart/F47); ignores failure concentration.
- **B — `p10 ≥ T_tail AND mean ≥ T_central` (the C53 builder's default).** Guards both a bad tail and central tendency using two of C33's statistics. *Defensible, but* structurally blind to spread/bimodality.
- **C — `p10 ≥ T_tail AND mean ≥ T_central AND std_dev ≤ T_spread`, with a `MinScenarios` floor and a judge-FP-rate (PF-2) precondition (RECOMMENDED).** Adds a spread ceiling (catches erratic/bimodal behaviour — the seed of F54 drift) and two preconditions: a minimum evidence base, and a check that the same-provider judge (D-1) isn't an uncalibrated "hall of mirrors" before its scores are trusted.
- **D — defer the rule shape entirely to the operator with no recommended default.** *Rejected:* freezes the spec; the autonomous-run discipline is to pick a defensible default + flag, not freeze.

## Decision

~~**Round-1: Adopt C** — `p10 ≥ T_tail AND mean ≥ T_central AND std_dev ≤ T_spread` + `MinScenarios` + judge-FP precondition.~~ **Superseded by Round 2 below (Adopt C′).** (Round-1 reasoning preserved under "Reasoning" for traceability.)

**Round-2 (final, pending operator sign-off): Adopt C′** — `p10 ≥ T_tail AND mean ≥ T_central AND (p90 − p10) ≤ T_spread`, with: a `MinScenarios` floor; the rule **shape FROZEN** (only the `T_*` thresholds are operator knobs — the shape itself is not, to deny a Goodhart escape); a judge-trust precondition discharged by a **human-audited judge sample** (≥N human-rated scenarios), not a cold-start-uncomputable statistical FP rate; and a **mandatory post-deployment factory-integrity term** (the factory's own baseline scenario suite must still pass after the new component is deployed, before `go`). The human design-review verdict (C52) remains a mandatory conjunctive term — satisfaction alone never deploys.

## Update (2026-06-02) — reframed by the spec–scenarios–system triangle (D-42 / D-43 / ADR-0069)

This brief asked "*which statistics gate the apex of bet #3?*" — framed as a predicate over C33's satisfaction distribution. The operator-adopted **triangle evaluation invariant** (D-42 / [ADR-0069](../../../../docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)) supplies the missing structure: this brief's go/no-go is **one edge — H↔I — of a three-edge triangle**, not the whole completion test. The reframe does NOT overturn C′; it relocates it:

- **The H↔I edge** (hold-out scenarios pass against the system, judged independently by C32) is exactly what this brief gated. Under the triangle, the strictest reading of that edge is **100% hold-out pass** (every scenario `satisfied`) — and that is now the **floor pinned at 1.0** in `C53 MilestoneConfig`, never an operator knob (per D-42: "*the 100% floor never lowers; what relaxes as the judge earns calibrated trust is the human-review/judge-trust oversight, not the pass rate*").
- **The C′ statistics** (`p10`, `mean`, `p90 − p10`, `MinScenarios`) are **no longer the gate**. They become **diagnostic evidence** surfaced to the judge's diagnosis (C32 `DiagnosisRecord`) and to human review — they describe the *shape* of the H↔I evidence, but they do not decide go/no-go. A distribution that is 100% `satisfied` but erratic is now caught by the judge's **root-cause attribution + tri_alignment** verdict, not by a `std_dev`/`p90−p10` threshold.
- **Completion = tri-alignment**, realized in `C53 §3.1` as four conjunctive `go` terms: (1) 100% hold-out pass (`all_scenarios_satisfied`), (2) `DiagnosisRecord.tri_alignment = aligned` (no unresolved spec/scenario/judge defect), (3) the human `ReviewVerdict`, (4) the post-deploy factory-integrity check. The **post-deploy factory-integrity term** this brief's Round-2 added is preserved as Term 4. The **judge-trust precondition** (PF-2, the human-audited judge sample) becomes the relaxable `judge_self_trust` oversight knob, NOT a precondition on the pass rate.

**Net:** C′'s *conservatism* survives and is strengthened (the spread/erraticism concern is now handled by the diagnostician rather than a brittle cold-start threshold), and C′'s *frozen-shape* property survives (the four-term shape is frozen; only `T_*`-equivalent oversight knobs relax). The morning-review ask below is unchanged in substance — the operator still sets the oversight/judge-trust knobs — but the pass-rate floor is no longer a knob at all. See [`review-log.md` D-42/D-43](../review-log.md) and [`HANDOFF.md` §0★](../HANDOFF.md).

## Reasoning

- The C53 builder proposed **B** independently; the self-modification-skeptic panelist independently recommended upgrading to **C** because `std_dev` is *already* in C53's `GoNoGoInput` (so the spread term is near-zero cost) and a mean+p10 rule is "structurally blind to bimodal/erratic behaviour, which is the seed of F54 drift."
- The PF-2 precondition (don't trust an uncalibrated same-family judge) was a standing expert-panel follow-up; the apex gate is the right place to make it binding.
- This is the first irreversible-ish trust handoff (factory modifying factory); the conservative shape is cheap and the downside of under-gating is high.

## Downstream impact

C53 §3.1/§3.4 (`decide()` predicate + `MilestoneConfig` knobs), C33 (already emits `std_dev`), C46 (FP-rate, non-spine — the precondition names it). No architectural change; the spec already carries **B** as the in-force default with the operator-judgment flag, so nothing is blocked pending sign-off.

## Adversarial review

**Round 1 = the 5-persona opus panel** (see [`VERDICT.md`](../panel-sweep2/VERDICT.md); the self-modification skeptic `02` is the on-point reviewer, with the security hawk `01` and integration adversary `04` corroborating the safety framing). This exceeds the ≥3-real-adversaries-per-round bar. **Honest note (context-budget consolidation):** rather than spin a separate first wave of brief-only reviewers, the lead used the already-mandated opus panel over the apex as Round 1 — the panel reviewed the C53 spec directly, which is the artifact under decision. **Round 2** (a tight ≥3-adversary wave on *this* revised recommendation, option C) is dispatched separately; its findings will be folded in below before the operator reviews. The operator's morning sign-off is the effective final ratification regardless.

### Round-2 findings (3 real adversaries, read the revised brief cold; all `accept-with-named-amendments`)

- **Simplicity/YAGNI:** `std_dev ≤ T_spread` and the statistical judge-FP precondition have a **cold-start problem** — on attempt 1 there's no run data to calibrate `T_spread` or compute an FP rate; a mis-set spread ceiling is asymmetrically dangerous (blocks a bimodal-but-good build). Amendment: make the spread term + judge-trust check **calibrate-after-first-run** (or discharge judge-trust by human audit), don't hard-require an uncalibratable threshold on the first build.
- **Statistical rigor:** **replace `std_dev` with the interquantile spread `p90 − p10`** — both fields are already emitted, it's scale-invariant on the bounded [0,1] score domain, and threshold-stable across runs where `std_dev` is not (skew/bimodality). The conjunctive `AND` form + `MinScenarios` are fine; confidence-interval machinery correctly stays in C48, not C53.
- **Safety/governance:** (a) **add a mandatory post-deployment factory-integrity term** — the gate scores the *built component* but never verifies the factory still works *after* the component is deployed into it (a self-modification can break the factory's own pipeline post-`go`); (b) **freeze the rule shape** (only thresholds are operator knobs — leaving the shape itself adjustable re-opens the Goodhart hole C was meant to close); (c) discharge the judge-trust precondition with a **human-audited sample** (≥10 human-rated scenarios), not a bare statistical FP rate.

These three converge: use a calibration-free-er spread measure (`p90 − p10`), don't hard-gate on uncalibratable cold-start thresholds, freeze the shape, add the post-deploy integrity check, and discharge judge-trust by human audit. Folded into **C′** above.

## Morning-review ask (one decision for the operator)

**Approve the C′ rule shape** (or pick B/another), and set the threshold values (`T_tail`, `T_central`, `T_spread`, `MinScenarios`, the human-audit sample size). The C53 spec currently carries **B** (`p10 AND mean AND MinScenarios`) as the in-force, flagged default, so nothing is blocked; on approval, C′ is a single-section edit to `C53 §3.1/§3.2` `decide()` + `MilestoneConfig` (+ the post-deploy term, which is the one genuinely new gate). Lead recommendation: **adopt C′.**

## Rewind point

The C53 spec carries default **B** with operator knobs; this brief recommends **C**. If the operator prefers B (or another shape), edit `C53 §3.1` `decide()` + `MilestoneConfig` — a single-spec, single-section change. Revert this brief to undo the recommendation. No other spec depends on the rule shape (C33 is threshold-free; the thresholds are config).
