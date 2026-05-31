# Adversarial review — C33 Satisfaction Metric Aggregator (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Evaluation & Judge
Target: spec/C33-satisfaction-metric.md (+ plan-faithful/C33-satisfaction-metric.md)
Charter: canonical/Track-A posture → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (flag any addition that hardens existing-stack capability rather than
delivering new capability tied to a 12-principle).

## Findings

### RC33-01 — major — `numpy/scipy/pandas` is presented as C33's v4-named reduction engine, but v4 names ONLY "Inspect AI score reduction" (with "MLflow tracking") for aggregation; the stats stack is an unmarked architectural fill — and scipy is specifically C48's engine
**Claim.** The spec repeatedly asserts the reduction is "**Inspect AI score reduction** + numpy/scipy/pandas"
/ "Inspect AI score reduction plus a stats library (numpy/scipy/pandas)" as if v4 names that stack (§1
"Reduce…", §1 boundary "NOT a custom statistics engine", I2, table-row Reduction engine, INV/the-bar, AC-8;
plan T4). **Evidence.** v4 names the C33 aggregation engine as exactly **"Inspect AI score reduction"** and
nothing else (README:188 table cell; AI-CONTEXT:302 "Satisfaction aggregation | Inspect AI score reduction";
AI-CONTEXT:373 "…+ aggregation"). The one v4 line that pairs aggregation with a *second* tool pairs it with
**"MLflow tracking"**, not a stats library (AI-CONTEXT:393 "Aggregation: Inspect AI score reduction, MLflow
tracking" — which the spec's own Source header quotes in full, then silently swaps for numpy/scipy/pandas in
the body). **`numpy` and `pandas` appear NOWHERE in any of the four v4 source docs.** `scipy` *is* named in
v4 — but specifically as the **C48** "Statistical comparison / was variant better?" engine (README:275;
AI-CONTEXT:360/421; inventory C48 "scipy/Evidently"), the exact significance box the spec correctly says is
NOT C33's. Pulling scipy (+ numpy/pandas) into C33 as "the stats library" therefore (a) asserts a stack v4
does not name for C33 as if it were fact (a fidelity violation under the canonical posture), and (b) is
mildly self-contradictory — the same section forbids "a custom statistics engine / no bespoke estimator"
while bolting on a general-purpose stats stack v4 reserves for C48. This is precisely the danger the bar
warns about. **Fix (applied).** Re-tagged the stats stack as a `[FAITHFUL-FILL]` — v4 names only "Inspect AI
score reduction" (companion: MLflow tracking) for C33's aggregation; a thin stats helper *behind* Inspect
AI's reduction (for quantiles/spread) is the minimal inference, NOT a v4-stated engine, and is explicitly
**not** the scipy significance machinery v4 assigns to C48. Softened the "+ numpy/scipy/pandas" assertions to
"Inspect AI score reduction (the v4-named engine) + a thin stats helper for distribution summaries
[FAITHFUL-FILL]" across §1/I2/§6/AC-8/§2-table and plan T4, and noted MLflow as v4's named companion. The
*substance* (off-the-shelf reduction, no bespoke estimator, significance is C48) is correct and kept.

### RC33-02 — minor — INV-2 cites "Mirrors C31 INV-4 'verdict-blind'", but C31:159 names C32/C33 as the verdict owners — the analogy is to the *runner* boundary, not a claim C33 renders a verdict
**Claim.** INV-2 says C33 mirrors "C31 INV-4 'verdict-blind' on the producer side." **Evidence.** C31 INV-4
(spec/C31:157-159) reads "C31 emits the trajectory + status; it computes **no** satisfaction score and
renders **no** pass/fail verdict — **that is C32/C33**." So C31 hands the *scoring/verdict layer* to C32/C33;
C33 then (correctly, INV-3) defers the *pass/fail cutline* further to C50/C53/C39. The phrase "verdict-blind"
in C31 is about the runner not scoring at all, whereas C33 *does* reduce scores but renders no pass/fail —
two different senses. As written the cross-reference is sound (both refuse a pass/fail verdict) but could be
misread as "C31 says C33 is verdict-blind," which C31 does not say. **Fix (applied).** Clarified INV-2's
parenthetical to "(C33 reduces scores but, like the C31 runner, renders no pass/fail verdict — INV-3; the
cutline is C50/C53/C39's)" so the analogy is to the *no-pass/fail* property, not a claim C31 delegates
verdict-blindness to C33. No substantive change.

### RC33-03 — minor — I3 / §1 attribute a verbatim quote to "C08 §observability" that paraphrases rather than quotes C08:112
**Claim.** §1 (I3 responsibility) and the I3 row quote C08 as: 'a spec revision is the unit a satisfaction
metric (C33) … are computed *against*' and tag it "C08 §'observability'". **Evidence.** C08:112 (in §7
Cross-cutting → Observability) actually reads: "A spec revision is the unit a satisfaction metric (C33) and
meta-metrics (C46) are computed *against*…". The C33 rendering elides "and meta-metrics (C46)" with an
ellipsis (fine) and labels the section "observability" (correct — it is the Observability bullet of C08 §7).
The quote is faithful; the only nit is the section is C08 **§7** (Cross-cutting/Observability), not a
top-level "§observability". **Fix (applied).** Changed the two "C08 §obs / §'observability'" tags to "C08 §7
obs" so the citation points at the real section number. Quote content unchanged (it is accurate).

### RC33-04 — minor — §1 "NOT the trajectory store…" says the judge-output bead shape is "C20's schema over C19" and trajectories are "C21 (CXDB)"; consistent with v4+inventory, but the C21 edge is asserted slightly beyond C33's named deps
**Claim.** §1 boundary + §4 table state trajectories live in **C21 (CXDB)** and the judge-output bead type is
**C20's** schema over **C19**. **Evidence.** Inventory C33 depends on **C32, C19** only (line 45) — C20 and
C21 are *referenced* (not dependency edges), which the spec mostly flags ("referenced, not read" for C21;
"owned by C20/C19" for the bead). This matches how C32 handles the same situation (C32 marks its C21/C19
trajectory read a `[FAITHFUL-FILL]` because inventory names only C30/C29). C33's §4 row for the trajectory is
labelled "(referenced, not read)" which is the right hedge; the C20 ownership claim is backed by D-3 (C20
authors bead-type payload schemas) and is correct. No fidelity error — but the C20/C21 references would read
more cleanly as explicitly *non-dependency* references (as the §2 table already does for C02/C17). **Fix
(applied).** Added a half-clause to the §4 "Judge-output beads" and "Trajectory" rows noting these are
*referenced* schemas/stores (C20/C21), not C33 dependency edges (deps are C32/C19 per inventory), mirroring
the §2 C02/C17 "related interface, not a dependency edge" treatment. Minor hygiene; no substance change.

### RC33-05 — minor — "satisfaction-rate-above-an-operator-supplied-cutline" listed inside the default statistic set risks reading as an always-on stat, in slight tension with INV-3/AC-4 (cutline optional)
**Claim.** §1 (I2 responsibility) lists the summary statistics as "(mean/median, spread, quantiles,
**satisfaction-rate-above-an-operator-supplied-cutline**, sample count)" — presented inline with the
always-computed stats. **Evidence.** INV-3 and AC-4 are emphatic that the cutline is **optional** and a
supplied cutline only adds an *additional* statistic; the metric is well-defined with no cutline. Listing
rate-above-cutline in the same breath as mean/median/quantiles (which are unconditional) slightly undercuts
the "optional, additive-only" framing the rest of the spec is careful about. Not a contradiction (the phrase
"operator-supplied" signals conditionality) but it is the one place the optionality is not explicit. **Fix
(applied).** Reworded the §1 I2 stat list to "(count, mean/median, spread, quantiles; and — *only if* an
optional reporting cutline is configured — rate-above-cutline)" matching the conditional framing already used
in §5 step 3 and I2's own table row. Consistency fix.

### RC33-06 — minor (no-op / confirm) — D-6 canonical-track framing, D-1 irrelevance, and the FE-5 holistic finding are all correct as written
**Claim/Evidence.** Spot-checks the binding decisions: (i) the doc titles itself "(Spec, canonical track)"
and cites **D-6**, never "Track A / faithful track" against a live Track B — compliant with D-6. (ii) §7
states D-1 (same-provider judge) is "irrelevant to C33" because C33 makes no model call — correct (C33 is
model-free; D-1 governs C32's judge identity, not a reducer). (iii) The FE-5 "load-bearing finding" (§6) —
that C08 adopted Reading A, ships no Definition-of-Done in its acceptance contract (AC-1…AC-5 =
format/renderability/versioning/lint/loop-closure), and its body is free-form Markdown prose — is **verified
accurate** against C08 §1 OQ-1, §4 [FAITHFUL-FILL], §6 F18, and §8 AC-1…AC-5, and against the FE-5 bucket
entry ("a DoD can attach to the Reading-A collapsed spec; does NOT require C08's standalone-bundle split").
No fix needed; recorded for the integrator's FE-5 ruling.

## FE-5 view (for the integrator)
**Holistic is the sound Sweep-1 baseline; P5 does NOT *require* enumerated per-criterion DoD now.** A graded
LLM judge over the free-form C08 prose *is* "satisfaction not test-pass" (P6), and the population distribution
of those holistic scores already delivers the P5 variety-of-outcomes measure C33 exists for — at zero C08
cost. Per-criterion DoD buys finer Ashby variety + per-criterion attribution (a real P5 capability), but it
is a coordinated C08+C32+C33 change the brief forbids C33 to make unilaterally, and its principal beneficiary
(per-criterion meta-metrics) is C46, which is built last (Batch 5). Recommend the integrator ship
holistic-only for Sweep-1 and keep per-criterion as the clean I2/I3 sweep-2 extension the spec already
scopes (OQ-3) — pull it in only if/when C46's per-criterion attribution need is real.

## Verdict
**accept-with-fixes.** Strong, faithful, and well-traced — every load-bearing README/AI-CONTEXT citation
(181/188/269/426/440; AI-CONTEXT 36/302/373/393) verifies verbatim; the C30/C31/C53/C55/C08 cross-references
are accurate; the three bar-prohibited surfaces (custom significance engine → C48, built-in "satisfied"
verdict → C50/C53/C39 via G09 reading (b), trend/cost → C46) are all correctly refused; G09 is correctly
split (definition resolved, threshold deferred); FE-5 is correctly flagged to the integrator, not
unilaterally resolved. The one **major** is a fidelity slip, not a design flaw: numpy/scipy/pandas is
asserted as C33's v4-named engine when v4 names only "Inspect AI score reduction" (+MLflow) and reserves
scipy for C48 — fixed in place by demoting the stats stack to a flagged `[FAITHFUL-FILL]`. Remaining findings
are minor citation/consistency hygiene, all applied. Nothing architectural deferred beyond the
already-flagged FE-5 (OQ-3) and G09-threshold (OQ-1) integrator calls.
