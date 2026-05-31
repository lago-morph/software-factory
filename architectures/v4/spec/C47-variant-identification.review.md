# Adversarial review — C47 Variant Identification (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Optimization (P12)
Target: spec/C47-variant-identification.md (+ plan-faithful/C47-variant-identification.md)
Charter: canonical track → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (flag any custom optimizer / search algorithm; the keep is variant-space
declaration + C46-objective wiring + C48 variant-set hand-off).

## Findings

### RC47-01 — minor — DSPy's second v4 capability ("statistical comparison (prompt-programs)", AI-CONTEXT:377) was quoted in evidence but never reconciled with the hard "all stats = C48" boundary
**Claim.** §1 boundaries assert flatly that the statistical-comparison engine is **C48** and "C47 builds no
p-value/CI/regression machinery" (D-19), while the source header quotes AI-CONTEXT:377 verbatim — "**DSPy |
L6 variant identification + L6 statistical comparison (prompt-programs)**" — as support for the
variant-identification reading. **Evidence.** AI-CONTEXT:377 (verified) assigns DSPy *two* L6 slots; the spec
exercises only the variant-ID half and elides any treatment of the stats half, leaving the one v4 line that
attaches a stats-adjacent capability to DSPy in slight, unaddressed tension with the clean "all
self-optimization significance → C48" split. The split itself is correct: **D-19** (verified in review-log)
routes self-optimization significance to C48, and **C48's own spec** (§1 lines 57–60) claims significance
determination as its load-bearing capability and never invokes DSPy for it. The gap is completeness, not
correctness — an unaddressed v4 statement, not an invented one. **Fix (applied).** Added a reconciling note to
the "NOT the statistical-comparison engine" bullet: DSPy is used only for the variant-identification half; all
significance (including over prompt-program variants) is C48 per D-19; if C48 elects DSPy's prompt-program
comparison it is a C48 engine choice, not a C47 surface.

### RC47-02 — minor — OQ-2's "candidate-list-only vs candidate-list-plus-experiment-design" was left as a fully-open two-way seam, but C48's spec has already claimed the experiment/routing design
**Claim.** OQ-2 (spec §9; mirrored plan §5 item 3 + §6) leaves open "does C47's set carry only the candidate
list, or also the experiment design (sample size / which scenarios / replay plan) that C48 routes?" as if
unresolved by v4. **Evidence.** C48's on-disk spec already owns the experiment design: §3 I1 binds the variant
set to a **routing strategy** (flag-split vs bandit) + decides the **arm→variant mapping**, and §4
"Experiment / routing binding" lists routing strategy, arm-mapping, and significance test/α as **C48-owned
state**. So the faithful reading is settled in C48's favour — C47 emits the candidate list; the
experiment/routing design is C48's — and leaving it as a two-way seam over-states the openness and risks the
two specs drifting on ownership. **Fix (applied).** Narrowed OQ-2 in the spec to state the faithful reading
(C47 = candidate list; experiment/routing design = C48, citing C48 §3/§4) and reframe the residual as "how
much provenance/metadata C47 attaches per candidate," not "who owns the design." Mirrored the narrowing into
the plan's de-risking spike (§5 item 3).

### RC47-03 — minor (no fix) — "review-log D-19 routes **all** self-optimization significance to C48" is a faithful paraphrase, slightly stronger than D-19's literal text
**Claim.** §1 and INV-2 paraphrase D-19 as routing "**all** self-optimization significance" to C48.
**Evidence.** D-19's literal scope is *methodology* significance (C55 → C48); its generalization to *all*
P12 significance is an inference (well-supported: C33 and C55 both carry the identical significance→C48
boundary, and C48's inventory mandate is "determines whether a variant was actually better"). The inference is
correct and is exactly the canonical split, so this is not a defect — but it is a paraphrase one notch firmer
than the logged decision's wording. **No fix applied** — the reading is right and the spec already cites the
supporting inventory mandate alongside D-19; flagging only so the orchestrator sees the paraphrase is an
inference, not a verbatim D-19 quote. Not worth body churn.

### RC47-04 — minor (no fix) — confirmed clean: citations, license cite placement, no-Gxx honesty, F47 split, D-6 framing
**Claim/Evidence (verification, no defect).** Spot-checked the load-bearing items the brief flagged:
- **Citations verbatim-correct.** README:269–278, 315–317, 470, 499 and AI-CONTEXT:354–357, 377, 418–419,
  642–643 all match the v4 source docs exactly (row text + line numbers). Unlike the C36 sibling (whose
  PyOD/Anomalib license rows were mis-cited to AI-CONTEXT §10 instead of README "Part 5"), C47's license cite
  ("README §Part 5 … line 315 DSPy | MIT | Clean") is **correctly attributed** — README:315–317 verified.
- **No-Gxx honesty (the brief's check).** Inventory C47 Key-gaps = "—" (verified, line 59). §6 states this
  honestly and homes the adjacent threads upstream/downstream: **G09** + **G32** are owned at **C46**
  (inventory C46 gaps = "G09, G32", verified) — *not* at C47; **G32**'s variant-replay-cost half is also at
  C48 (inventory C48 gap = G32, verified). Correctly placed.
- **F47 (Goodhart) split.** C47 owns the *upstream half* (keep the objective multi-metric, INV-5); the
  *enforcing gate* is **C50** — confirmed: C50's spec + inventory ("Statistical, multi-metric gate … guards
  Goodhart") own the F47 promotion gate (F-MODE-COVERAGE:103 verified). C47's "the gate is C50" is correct.
- **C55 boundary cite.** C55 spec line 111 verbatim: "discovery (DSPy/Optuna) is **C47**" — accurately cited.
- **D-6.** Neither C47 doc frames itself as "Track A / faithful track"; no D-6 violation.
- **C36 parity claims** (cold-start "insufficient signal", C20-bead-vs-C23-event carrier OQ, version-pin) are
  all real C36 features — parity invoked legitimately.

## Verdict
**accept-with-fixes.** High-fidelity, well-traced spec+plan; every load-bearing v4 citation verified verbatim.
The capability-for-principle bar is correctly held — **no custom optimizer / search algorithm** is introduced
(prompt = DSPy, hyperparameter = Optuna/Ray Tune; INV-1/AC-2), the kept custom surface is exactly
variant-space declaration + C46-objective wiring + the C48 variant-set hand-off, and the dropped list (custom
search, A/B routing, significance, promotion gate, replay, meta-metric definition, methodology/topology) is
correctly homed at C48/C49/C50/C46/C55. No-Gxx is stated honestly and the G09/G32 threads are homed upstream.
The two applied fixes are completeness tightenings (reconcile DSPy's dual v4 capability; align OQ-2 with C48's
already-claimed experiment-design ownership). No fidelity blockers; nothing architecturally significant
deferred.
