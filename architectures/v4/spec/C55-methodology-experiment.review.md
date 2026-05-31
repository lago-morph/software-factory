# Adversarial review — C55 Methodology-as-Config Experiment Loop (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Bootstrap / Methodology-experiment
Target: spec/C55-methodology-experiment.md (+ plan-faithful/C55-methodology-experiment.md)
Charter: canonical-track posture = attack FIDELITY and COMPLETENESS (not design), PLUS the
capability-for-principle bar (flag hardening-on-existing-capability vs new capability tied to a 12-principle).

## Findings

### RC55-01 — major — "P-methodology-experimentation … v4's single named principle" mislabels the v4 *pivot/Bet-5* as a numbered 12-principle
**Claim.** §1 (L42–44, L134) frames C55 as operationalising "v4's **central inversion and its single named
principle**: **P-methodology-experimentation**", and §2/§6 lean on this "principle" framing.
**Evidence.** The v4 12-principle set is the El Kaim synthesis P1–P12 (P12 = self-optimization; AI-CONTEXT §1/§27,
README Part 4). "Methodology is the variable; substrate is convergent / you don't choose, you experiment" is
v4's **Pivot** (AI-CONTEXT §0 "Pivot summary", §11.1; AI-CONTEXT:462) and **Bet 5** ("Methodologies will emerge
empirically", README:508–512) — **not** a numbered principle, and the string "P-methodology-experimentation"
appears **nowhere** in the corpus. It is a builder coinage. This matters under the capability-for-principle bar:
the bar asks whether an addition is tied to a 12-principle; C55's true warrant is the **pivot/hypothesis** (the
reason the whole runtime exists), not a 12-principle — and the spec itself elsewhere correctly calls it "the v4
hypothesis" and ties cost to "Bet 5" reasoning. The KEEP is still sound (operationalising the pivot is genuine
new capability no component provides); only the *label* overstates provenance.
**Fix (applied).** Re-tagged the principle language to the faithful provenance: C55 operationalises **v4's
central pivot / hypothesis (Bet 5)** — "methodology is the variable, substrate is convergent" — and dropped the
coined "single named principle / P-methodology-experimentation" framing (kept the prose name only as an informal
shorthand, explicitly marked as the pivot, not a 12-principle). Capability KEEP unchanged.

### RC55-02 — major — the "explicit routing ruling" / "binding" for significance→C48 is asserted as a logged decision, but no D-x records it
**Claim.** §1 (boundaries), §6 ("**Routing — A/B significance is C48, not C55 (binding)**" … "the explicit
'route significance testing to C48' ruling"), INV-4, AC-5, and the plan (T7, M3, Risk 2) repeatedly cite "the
routing ruling" as if it were a recorded binding decision in the review-log.
**Evidence.** The review-log's `## Resolved decisions (binding)` lists D-1…D-17; **none** mentions C55, A/B
significance routing, or C48-vs-C55 scope (grep: zero hits for C55 / "routing ruling" / methodology-significance
in review-log.md, and the C55 row is absent from the harvested OQ list). The ruling *is* correct and is binding
**per my dispatch brief** and well-grounded in v4 (C48 inventory: "determines whether a variant was actually
better"; C33 routes significance to C48 identically). But presenting it as an *already-logged* "explicit ruling"
overstates its status — it is a builder-introduced (adversary-confirmed) routing that still needs to be
*recorded* as a decision, exactly the kind of cross-component ruling the review-log exists to hold.
**Fix (applied).** Softened the provenance wording: the significance→C48 routing is stated as **C55's binding
scope boundary (grounded in C48's inventory mandate + the C33 precedent), to be recorded in the review-log** —
not as a pre-existing logged ruling. Content (no C55 stats engine; consult C48; withhold until C48) unchanged;
added an OQ-4 note that the C55→C48 routing should be entered as a numbered decision.

### RC55-03 — minor — threshold cutline owners under-cited vs C33 (C55 names "C50 / operator"; C33 names C50 **/ C53 / C39**)
**Claim.** §6 ("**The threshold … DEFERRED, not C55's**") and OQ-1 route the absolute "good enough" cutline to
"a **C50 promotion gate / operator policy**".
**Evidence.** C33 §1 (its own boundary, L72–76) names the satisfaction-vs-threshold gate as **C50 / C53 / C39**,
and the threshold value itself as "undefined in v4 / deferred (G09)". C55 inheriting C33's threshold-free
posture is faithful, but naming only C50 narrows C33's stated owner-set. Not wrong (C55 selects *relatively*, so
which downstream gate owns the absolute cutline is not C55's to fix), just less complete than its own cited
source.
**Fix (applied).** Broadened the cutline-owner reference to "**a decision-site gate (C50/C53/C39) / operator
policy** — the cutline value is undefined in v4 and deferred (G09)", matching C33's boundary verbatim.

### RC55-04 — minor — C33 "threshold-free" is cited as established; correct, but tag it as the *inherited* posture it is
**Claim.** §1/§6/§7 assert C55 "inherits C33's **threshold-free** posture" as settled fact.
**Evidence.** This is accurate — C33's INV-3 is "threshold-free computation (G09)" and D-15 makes satisfaction
holistic. No correction to the substance. The only hygiene point: C55 should make clear it is *relying on* a
C33 invariant (an upstream property), not independently establishing threshold-freeness — the same "qualify an
inherited/adopted property as such" discipline the C23 review applied.
**Fix (applied).** Minor wording: phrased as "inherits C33's threshold-free invariant (C33 INV-3 / D-15)" at
first use so it reads as an upstream dependency, not a C55-owned guarantee. No semantic change.

### RC55-05 — minor — cost-fan-out gap cited as "G32 / G34"; G34 is throughput/scale, the fan-out cost itself is G32 (+ G13)
**Claim.** §7 Cost and OQ-3 attribute the multiplicative experiment fan-out to "the unmodelled **G32 cost /
G34 throughput** gap".
**Evidence.** Correct and both gaps verify (G32 = cost unmodeled, explicitly citing "cost amortizes across
methodologies, README:512, with no number"; G34 = single-Max-seat throughput ceiling). The pairing is apt —
the fan-out is a *cost* force (G32, and G13 unmodeled token budget) realised *through* the throughput ceiling
(G34). Citation is sound; flagging-not-engineering is correct (→ C46, which is unbuilt/Batch 5, confirmed). No
fidelity defect — noted only to confirm the gap routing is right and the cost is genuinely **flagged**, not
engineered around (bar upheld).
**Fix.** None needed (verification finding). Left as-is.

### RC55-06 — minor — forward-reference hygiene: C48/C46/C57 are all unbuilt; the spec must not read as binding on them
**Claim.** The spec consults **C48** (significance), routes cost to **C46**, and defers the F-mode map to
**C57**.
**Evidence.** Verified on disk: **no** spec files exist for C48, C46, or C57 (all Batch 5 / later) — so all
three are genuine forward references. The spec already marks C48 "unbuilt (Batch 5) … must not block on it"
(good) and gives interim behavior (raw distributions + withheld significance). C46 and C57 are named as owners
without an explicit "unbuilt, do-not-block" note. Low risk (C55 only *defers to* them, never blocks), but for
parity with the C48 treatment they should carry the same forward-ref tag.
**Fix (applied).** Added a one-clause "(C46/C57 are later-batch; C55 names the seam, does not block on them)"
note where C46 (cost) and C57 (F-mode map) are first cited, matching the existing C48 forward-ref discipline.

## Verdict
**accept-with-fixes.** Strong, faithful, tightly-scoped. The G05 resolution is correct and well-argued —
"GF-M first = standing-up *order*, not the winner" is the only reading consistent with README:31/33 ("you don't
choose; you experiment") and AI-CONTEXT:501 ("pick a v3 methodology … wrong question"), and the spec routes the
residual taxonomy to OQ-2 properly. The ruthless bar is held: **no** methodology engine/runner/scorer (reuses
C12 swap + C30/C31/C32/C33), **no** bespoke significance machinery (routed to C48), **no** absolute satisfaction
threshold (inherits C33 threshold-free), per-work-type empirical selection only. Cost fan-out is **flagged**
(→C46/G32), not engineered. All dependency cross-refs (C12 "swaps the formula", C30 "same scenarios", C33
consumer, C31 verdict-blind, C48 significance) verify against the live specs; inventory row, Batch-4 placement,
and every README/AI-CONTEXT line citation check out. Fixes are all the canonical-track pattern — *qualify a
builder-coined or builder-introduced item as the inference/scope-boundary it is, rather than asserting it as an
established v4 principle or logged ruling* (RC55-01 the "single named principle" coinage; RC55-02 the
"binding routing ruling" provenance) plus citation-completeness polish (RC55-03/04/05/06). **Nothing
architectural deferred** — the two material findings (-01, -02) are provenance/label corrections applied in
place; the substantive design is unchanged and the OQs (G05 confirmation, work-type taxonomy, cost quant/C46,
C48 seam) are already correctly mirrored to the review-log.
