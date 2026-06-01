# Sweep-2 Panel — Self-Modification Skeptic

**Seat:** Self-Modification Skeptic (panel of 5)
**Scope:** the first self-build go/no-go (C53) and the satisfaction signal it trusts (C33 ← C32, D-1).
**Specs read:** C53, C52, C33, C32, C51; decisions D-1, D-15, D-21, D-40 (+ prior-panel PF-2, PF-3).
**Date:** 2026-06-01

## VERDICT: `right-idea-change-X-before-building`

C53 is the right *kind* of artifact. Turning "deploy if it works" (G23) into a recorded, evidence-anchored
go/no-go over held-out scenarios is exactly the discipline the first self-modification needs, and the
conjunction shape (`scenario-set ∧ C51-pass ∧ C33-bar ∧ C52-approve`) is sound at the term level. But the
specific bar that gates the apex of bet #3 has three trust defects that are cheap to fix now and expensive
to discover after the factory has been told it can build itself. None of them is "reject the shape"; all of
them are "change X before building." Two are already-surfaced prior-panel findings (PF-2, PF-3) that C53
does **not** cite — that omission is itself the finding.

---

## FINDINGS

### F1 — The bar reads two statistics and ignores the one that detects the most dangerous failure (variance).
C33 emits `{n, mean, p10, p50, p90, std_dev, rate_above_cutline?}` (C33 §3.4). C53's `decide()` gates on
**only `p10 ≥ T_tail AND mean ≥ T_central`** (C53 §3.2). `std_dev` is computed, carried, and then **thrown
away by the gate** — even though C33 §3.4 explicitly names `std_dev` "the Ashby variety measure" and the
spec's own rationale (C53 §3.1) admits a `mean`-only gate "can pass while a consistent tail of scenarios
systematically fails." That argument cuts against C53's own choice: `p10` catches a *consistent low* tail,
but a **bimodal / high-variance** distribution — half the scenarios excellent, half marginal — can clear
both `p10` and `mean` while signalling that the self-built component behaves *unpredictably*. For the FIRST
self-modification, behavioural unpredictability is the headline risk (it is the seed of F54 drift), and the
two-term predicate is structurally blind to it. The spec hand-waves this ("Adding `std_dev` gates is
optional operator policy") — but for *this one gate*, "optional" is the wrong default. The cheapest
defensible apex bar is **three terms**: tail floor (`p10`), central floor (`mean`), and a **spread ceiling**
(`std_dev ≤ T_spread`). C53 already plumbs `std_dev` into `GoNoGoInput`; adding the term is nearly free.

### F2 — The satisfaction signal is uncalibrated, and the prior panel already said don't trust it yet (PF-2). C53 never cites PF-2.
The bar's correctness term is C33's distribution, which is a reduction of C32 judge scores. Per **D-1** the
judge is the **same provider/family as the coder**, and per **D-15** it grades **holistically** against
C08's free-form prose DoD. Prior-panel **PF-2** flagged exactly this as a possible "hall of mirrors" and
recommended: *"gate the first reliance on satisfaction scores on a judge-FP audit; do not auto-promote on
uncalibrated satisfaction."* C53 is **the** first reliance on satisfaction scores for a self-modification —
and it cites D-15 and D-1 but is **silent on PF-2**. The self-built component is graded by a judge of the
same lineage as the agent that built it, against a prose rubric a self-authored spec could itself shape
(C52 `emit_spec`), with no calibration precondition. That is a closed loop the gate treats as ground truth.
This is the sharpest objection (below). Fix: make a **C46 judge-FP / calibration check a named precondition
term** of C53's rubric (or an INV), not an unstated assumption — so a `go` is impossible on an unaudited
judge. The C53→C46 edge does not exist today; C53 cites C46 only as a peer cutline-owner, not a precondition.

### F3 — Can a self-built component game the signal? Partly yes — and C53's structural backstop is thinner than it reads.
Three of the four conjunction terms are gameable or weak against a self-optimising builder:
- **C51 completeness** is "every operator-named behaviour has ≥1 tagged scenario" (C51 §3.0.1) — coverage,
  not adequacy. One trivial scenario per behaviour satisfies it.
- **C33 correctness** is the holistic same-family judge (F2).
- **C52 human review** is the genuine external anchor — but C53 models it as one boolean conjunction term
  (`ReviewVerdict == "approve"`) with `require_review_approve` **relaxable post-P12** (C53 §3.3). At Phase 2
  it is mandatory and non-bypassable (C52 I2), which is correct. But C53 records the review as a *rubric
  input it reads*, not as a gate with any teeth of its own — and the spec offers no guidance on what makes
  the review more than a rubber-stamp of three green machine signals. When a human sees `p10` green, `mean`
  green, C51 `pass`, the social pressure is to approve. The held-out scenario set (INV-3) is the one real
  anti-overfitting property, and it leans entirely on C34 holdout enforcement (C51 §6 F9) — which is itself
  gated on the unfinished D-23 Gas City prevent-vs-detect spike. So the "real backstop" is: a human looking
  at three signals, two of which (F2, completeness) are weak. That is *better than "looks good"* (G23 is
  genuinely closed at the shape level) but it is **not** a hardened defence against a builder optimising for
  the gate.

### F4 — F54 drift (D-21): one human checkpoint is acceptable for ONE build, but PF-3 already asked for a mechanical tripwire at P3b, and C53 is silent on it.
D-21 makes objective-drift registered-unbuilt with a human checkpoint pre-L5; a real detector is required
before L5. For the *single* bootstrap component (C53 fires once, INV-6) the human checkpoint is a
*defensible* mitigation — the blast radius is one bounded component, reviewed, with recorded provenance
(C20/C41). I do **not** reject C53 on F54. **But** prior-panel **PF-3** explicitly wanted *"a lightweight
drift tripwire at P3b, ahead of the full detector at L5… since drift can begin the moment the factory tunes
itself."* C53 is the recorded checkpoint at precisely that moment and is the natural host for a cheap
mechanical tripwire (e.g. record the bar values + judge identity + distribution shape on the `factory_build`
bead so the *next* self-build can be compared against this baseline). C53 records the decision (INV-4) but
names no drift-baseline comparison and does not cite PF-3. The recorded decision is *latent* drift evidence
that nothing is yet wired to read.

### F5 — `MinScenarios` and small-n honesty: the gate inherits a known-weak input without strengthening it.
C53 §3.2 rejects `n < cfg.MinScenarios`, and C33:INV-4 surfaces n — good. But `MinScenarios` is a bare
operator knob with **no floor and no v4-stated value** (C53 §6 OQ-3 concedes "how many scenarios make the
bet credible is not fixed"). A `go` over `n=3` held-out scenarios for the make-or-break validation of the
entire factory-builds-factory thesis is structurally permitted if the operator sets `min_scenarios=3`.
For *this* gate, the spec should at minimum require the operator to **sign off on `MinScenarios` jointly
with the bar shape** (it is the same class of safety judgment), and flag that a small-n `go` is weak
evidence even when green.

---

## SHARPEST OBJECTION

**The gate trusts a same-family judge as ground truth for whether the factory can safely modify itself, and
the prior panel already told you not to.** The correctness term of the first self-build go/no-go is C33's
distribution; C33 reduces C32 judge scores; C32 is the **same provider/family as the coder** (D-1) grading
**holistically** against a **free-form prose DoD** (D-15) that a self-authored spec helped shape. The
adversarial reviewer that proves the self-built component "behaves like its exemplar and satisfies its DoD"
is the *same lineage* as the builder, reading a rubric from the *same self-authoring loop*. Prior-panel
**PF-2** named this a "hall of mirrors" and recommended gating the first reliance on satisfaction scores on
a judge-FP audit. C53 is that first reliance — and it cites D-1 and D-15 while remaining **silent on PF-2**.
A green `go` from C53 can therefore mean "an Anthropic judge thinks Anthropic-built code is fine, on a prose
spec, scored on as few scenarios as the operator allowed" — and the architecture would read that as "the
factory has proven it can do its own development work" (README:436) and arm Phase 3. The two-term bar (F1)
makes this worse: the one signal that would catch the judge behaving erratically (variance) is computed and
discarded. The human review (C52) is the only out-of-family check, and C53 models it as one boolean it
reads, not a hardened gate. **A self-modification gate whose objective half is a closed same-lineage loop,
explicitly flagged by the last panel and uncited here, is not yet trustworthy enough to ratify bet #3.**

---

## CHANGE-BEFORE-BUILDING (ranked)

1. **(F2 / sharpest — REQUIRED) Make a judge calibration / false-positive precondition a named term of
   C53's rubric.** A `go` MUST be impossible while the satisfaction judge is uncalibrated. Wire the missing
   C53→C46 precondition edge (C46 owns judge-FP-rate, README:269; PF-2 names C46 as the measurer). Cite
   PF-2 in C53 §6. This is an **operator sign-off item** — it is the same-family-judge trust call.
2. **(F1 — operator sign-off) Change the apex bar to three terms:** `p10 ≥ T_tail AND mean ≥ T_central AND
   std_dev ≤ T_spread`. `std_dev` is already in `GoNoGoInput`; the term is nearly free and closes the
   bimodal/erratic-behaviour blind spot the spec's own rationale admits. The *shape* of the first
   self-build gate is the one decision C53 already routes to morning review (C53 §3.1) — the spread term
   belongs in that sign-off, not in "optional operator policy."
3. **(F4 — cheap) Add a drift-baseline record to the `go` decision** (PF-3): persist bar values + judge
   identity + distribution shape on the `factory_build` bead so the next self-build is comparable. C53
   already writes the evidence bundle (INV-4); name the baseline-comparison use and cite PF-3.
4. **(F5 — operator sign-off) Bind `MinScenarios` sign-off to the bar-shape sign-off** and flag small-n
   `go` as weak evidence. Same safety-judgment class as the rule shape.
5. **(F3 — clarifying) State, as an INV, that C52 human review is a hardening gate, not a rubber-stamp of
   the machine terms** — and that at Phase 2 it is non-relaxable regardless of `require_review_approve`.

---

## EXPLICIT RECOMMENDATION ON THE C53 RULE SHAPE

**Do NOT keep `p10 AND mean`.** Change it to **`p10 ≥ T_tail AND mean ≥ T_central AND std_dev ≤ T_spread`**
(three terms: tail floor, central floor, spread ceiling). The two-term predicate is structurally blind to
high-variance / bimodal behaviour, which is the seed risk of the very thing this gate exists to guard
(self-modification drift), and C53 already plumbs `std_dev` so the cost is trivial. **Yes — this is an
operator sign-off item:** C53 §3.1 already flags the rule SHAPE as a mandatory morning-review/safety fork,
and the spread term plus the `MinScenarios` floor (F5) and the judge-calibration precondition (F2/PF-2)
should all be on that same sign-off sheet, because they are the same class of safety/governance judgment —
not mechanical engineering defaults.
