# Adversarial review — C45 Twin contract & fidelity verification (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Digital Twins (C45)
Target: spec/C45-twin-fidelity.md  (+ plan-faithful/C45-twin-fidelity.md)
Charter: canonical/faithful posture → attack **fidelity + completeness** (not design), **plus** the
capability-for-principle bar (HANDOFF §2): flag any rebuilt stack tooling; the KEEP is only the fidelity
**bar definition + verification wiring**.

## Summary of attack outcome

The core deliverable holds. **G22's "how close is close enough" bar is a real, falsifiable predicate**, not
vibes: §4.1 + §3.1 fix it as a *per-service predicate over named dimensions* — (a) checked dimensions
(contract-conformance + behavioural-match), (b) per-dimension tolerance (exact set: status/error-taxonomy/
schema/auth; bounded set: latency/ordering/numeric/omission), (c) the C30 probe corpus it is evaluated over,
(d) a pass rule that combines into a `fidelity_pass | fidelity_fail` verdict — with the concrete tolerance
*values* + dimension *catalog* honestly deferred to Sweep-2 (OQ-C45-1). The single-global-threshold reading is
correctly rejected (§6 G22 Reading B, binding). The over-build bar is respected: the "no-engine-rebuild
invariant" and the §1/§2 "Explicitly NOT a new contract-testing/schema-diff/mocking engine" framing keep the
custom surface to *predicate + combine-and-gate wiring* only. The C44→C45 seam is consistent with C44's own
spec (C44 defers the fidelity bar to C45, exposes the I8 fidelity-observation hook + declares the I2 cloned
surface; C45 reads exactly those). The C30 seam (fidelity-probe corpus as Inspect-AI scenarios) is consistent.
All four README/AI-CONTEXT/F-MODE citations I spot-checked (README:195/199/200/201/468/499/520;
AI-CONTEXT:343/344/347/487/620; F-MODE §4 F12/F33/F44/F56; SURVIVOR-PASS #02/#07) are accurate **except** the
two tooling mis-attributions below, which matter precisely *because* C45's bar is "invoke the right off-the-
shelf tool, don't rebuild."

## Findings

### RC45-01 — major — Prism is mislabeled as the OpenAPI-**conformance/contract-verification** tool; it is an OpenAPI-driven **mock** (AI-CONTEXT:343), so the usage-vs-promises half cites the wrong stack tool (and edges toward circularity)
**Claim.** Across ~6 sites (§1 lines 54–55, §1 FAITHFUL-FILL line 65, Responsibilities line 85, §3 interface 2
line 167, §4.3 table line 245, §5 line 268) the spec names **"Prism for OpenAPI-conformance"** /
**"OpenAPI-conformance checking (Prism, AI-CONTEXT:343)"** as the tool for the *contract* half
(twin-usage-vs-service-promises). **Evidence.** AI-CONTEXT:343 is literally `OpenAPI-driven mock | Prism,
Stoplight | Apache 2.0/various | Mature` and README:199–200 list Prism only as a *mock server* — the **same
role C44 uses Prism for inside the twin** (C44 §3 I5 "OpenAPI-driven mock … Prism/Stoplight"). Prism is **not**
a contract/conformance *verifier*. The capability v4 actually names "Contract verification — Verify usage
matches service promises" is **Pact + schemathesis** (README:201; AI-CONTEXT:344), and schemathesis is
specifically the OpenAPI **conformance/property** tester. Citing a *mock* as the *verifier* both mis-attributes
the stack tool and is near-circular under C45's own bar: running Prism (a mock) "against the twin" to "verify
conformance" mocks the contract rather than checking the twin against it. **Fix (applied).** Re-attributed the
contract/usage-vs-promises half to **Pact / schemathesis** (the AI-CONTEXT:344 "Contract verification" row,
schemathesis = OpenAPI conformance); removed Prism from the *verifier* role and, where Prism is mentioned,
re-cast it as what v4 says it is — an **OpenAPI-driven mock** that belongs to C44's twin construction (a
potential *subject* of verification), not a C45 conformance checker. The contract half's stack-tool citation is
now AI-CONTEXT:344 / README:201, not AI-CONTEXT:343.

### RC45-02 — major — "record/replay **diff** tooling" overstates VCR/go-vcr (README:199 = capture-and-replay, not diff) and quietly contradicts the spec's own thesis that the diff is the DIY KEEP (AI-CONTEXT:347)
**Claim.** §1 FAITHFUL-FILL (line 65 "HTTP record/replay **diffing** (VCR/go-vcr)"), §1 NOT-list (line 111
"HTTP record/replay **diff** tooling are mature OSS"), §3 invariant (line 198–199 "record-replay **diff**"),
and §4.3 (line 246 "**record/replay diff** (VCR/go-vcr/polly)") present the *behavioural diff/compare* as
off-the-shelf. **Evidence.** README:199 lists VCR.py/go-vcr/polly.js as **"Capture and replay HTTP traffic"** —
these are record/replay **fixture** libraries; they supply the *recorded reference* + replay, **not** a
diff/compare engine. v4 is explicit that the *fidelity diff* is the unsolved part: AI-CONTEXT:347
`Behavioral fidelity testing | None turnkey | DIY | Manual diff tooling`. So labelling VCR/go-vcr as "diff
tooling" (a) mis-cites README:199 and (b) undercuts C45's own (correct) claim that the **tolerance-scored
behaviour diff is the custom KEEP** — the spec elsewhere says exactly this (§4.3 "C45's custom part = the
tolerance scoring", AC-8). The record/replay tools provide the **reference capture + replay**; the
**golden-compare/diff-against-tolerance is C45's DIY surface** (AI-CONTEXT:347), not VCR's. **Fix (applied).**
Re-worded the behaviour-half citations so VCR/go-vcr/polly (README:199) are credited only for **record/replay
reference capture**, and the **diff/compare** step is attributed to C45's DIY "manual diff tooling"
(AI-CONTEXT:347) — i.e. the diff is *part of the KEEP*, not a third off-the-shelf engine. The "no-engine-
rebuild invariant" is preserved (C45 still builds no schema-diff *library*; it scores a compare over recorded
fixtures), and the §1 thesis is now internally consistent with §4.3/AC-8.

### RC45-03 — minor — `Prism … (README:201/AI-CONTEXT:343–344)` bundles a mock row and two verification rows under one citation, blurring which tool does which half
**Claim.** §3 interface 2 (line 167) and §4.3 (line 245) cite "`README:201/AI-CONTEXT:343–344`" as one
provenance blob for the contract check, sweeping the OpenAPI-mock row (343) and the contract-verification row
(344) together. **Evidence.** 343 (mock) and 344 (Pact/schemathesis) are *different capabilities* with
*different stack tools*; the range citation lets the RC45-01 conflation read as sourced. **Fix (applied).**
Folded into the RC45-01 fix — the contract half now cites **AI-CONTEXT:344 + README:201** (verification), and
any residual Prism mention is separately tagged to AI-CONTEXT:343 **as the mock row it is** (C44's surface),
so the two capabilities no longer share one citation.

### RC45-04 — minor — `OQ-C45-N` numbering diverges from the harvested review-log convention `C45:OQ-n` (cosmetic; not corrected to avoid churn)
**Claim.** §9 + plan §6 use `OQ-C45-1..4`; the review-log harvests sibling OQs as `C45:OQ-n` (e.g. C44/C30/C31
rows). **Evidence.** Pure nomenclature; the spec maps each to "→ review-log" and is internally consistent with
its own plan. The collector normalizes on harvest. **Fix.** **DEFERRED (cosmetic)** — left as-is; not worth
edit churn, and the collector reconciles the label. Flagged only so the orchestrator isn't surprised by the
two spellings.

## Verdict

**accept-with-fixes.** The G22 deliverable is genuinely discharged at sweep-1 altitude: the fidelity bar is a
falsifiable, per-service predicate (named dimensions + probe corpus + pass rule → `fidelity_pass|fidelity_fail`)
with tolerances honestly deferred to Sweep-2, the two-sided invariant is real, the over-build bar is held, and
the C44/C30 seams are consistent. The two `major` findings are **fidelity mis-attributions of off-the-shelf
tooling** (Prism mislabeled as a conformance verifier; VCR/go-vcr mislabeled as diff tooling) — both fixed in
place by re-citing the correct stack tool per half (Pact/schemathesis = contract verification; record/replay =
reference capture, the diff = C45's DIY KEEP). No architectural change; nothing of significance deferred (one
cosmetic OQ-numbering nit left for the collector). No blockers.
