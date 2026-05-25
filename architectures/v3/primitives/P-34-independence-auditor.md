# P-34 — Independence auditor

**Claimed by:** [D7-U-1 (Falsification-Topology Factory)](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §1 substrate primitive #4.
**Dispatch-tier:** per-primitive.
**Buildability verdict:** **research-grade-uncertainty** — on the *structural* concern (auditor recursion). The *construction* of the auditor itself is `designed-system`.

## Contract restatement

A Patrol-tier (cross-cycle, distributional) deterministic anomaly detector that consumes the [P-28 FC-store](P-28-typed-object-store.md) log and flags two failure shapes structurally:

1. **Collusion patterns** — the same opposing-side identity (provider/family/role tuple from `FalsificationCommitment.opposing-side.identity` per [D7-U-1 §1 FC schema](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md)) is accepting (returning `verdict.outcome == survived`) too many FCs of a given `artifact-kind`, relative to the population of opposing sides operating on that artifact-kind across cycles. "Too many" is measured against an expected distribution.
2. **Correlation patterns** — opposing-side verdicts correlate suspiciously across cycles: two nominally independent opposing sides agree at a rate inconsistent with their declared `independence-evidence`. This is the F46 / F27 / F48 cascade as a measurable distributional property.

The auditor's output is an FC-on-an-FC-batch: a typed flag entered back into the FC store so that downstream compounding via the [P-29 compounding gate](P-29-policy-mediator.md) can refuse to advance artifacts whose surviving FCs were rubber-stamped by a colluding judge population.

## Construction path

The auditor is itself a substrate-side deterministic batch job (Patrol-tier per D-6 watchdog tier mapping), not an LLM. It runs at cycle-aggregation cadence over a windowed slice of the FC log.

- **Collusion test (per opposing-side × artifact-kind cell):** `scipy.stats.binomtest` on observed survived/refuted ratio vs. expected ratio (where expected is the population marginal across all opposing sides on that artifact-kind). Flag cells with p < threshold after Bonferroni correction. *Integration sentence:* the FC log is materialised as a pandas DataFrame keyed on `(opposing-side.identity, artifact-kind, cycle)`; `scipy.stats.binomtest` returns a p-value per cell which the auditor writes back as an `IndependenceAuditFinding` typed envelope into the same P-28 store.
- **Correlation test (per opposing-side pair):** `scipy.stats.fisher_exact` on the 2×2 contingency of joint verdicts on FCs that both opposing sides judged. *Integration sentence:* for every pair of opposing-side identities that judged the same artifact within a window, the auditor builds a 2×2 table (survived/survived, survived/refuted, refuted/survived, refuted/refuted) and runs Fisher's exact test; significant positive association above the baseline shared-distribution rate is the collusion signal.
- **Distributional outlier sweep:** `sklearn.ensemble.IsolationForest` over per-cycle feature vectors `(acceptance rate, mean budget-utilisation, mean survival-window declared, opposing-side-identity-diversity)`. *Integration sentence:* outlier cycles are surfaced for higher-tier review even when no individual statistical test trips, catching novel patterns the binomial/Fisher tests are blind to.

Prior art: ledger-anomaly detection in financial fraud detection (chi-squared on transaction populations, isolation forests on transaction graphs); detector-of-detectors in adversarial ML (cf. CaMeL's deterministic-checker chains, OpenHands §7).

## Auditor recursion engagement (load-bearing OQ-1)

D7-U-1 OQ-1 names the structural concern verbatim: *"Independence is measured, not declared — what if the measurement itself colludes?"* and notes the corpus *"does not name a 'recursion-stopping' rule."* Three options, each with consequences:

- **Option A: deterministic-ness IS the assurance.** The auditor is itself a deterministic batch job (scipy/sklearn pipeline with frozen thresholds), so it has no LLM-distribution shared with the judge population it audits. Determinism breaks the F27/F46/F48 distributional-collusion mechanism at the auditor layer because there is no distribution to share. *Consequence:* the auditor can only detect what its frozen tests are shaped to detect — F49 (discussion-as-amplification) and novel collusion patterns the test suite was not designed against slip through; the auditor has Ashby-deficient variety against a probabilistic agent population (F51). The deterministic-ness is real assurance against *correlated-error* recursion but not against *coverage* gaps.
- **Option B: auditor-of-the-auditor (turtles).** A higher-tier auditor reviews the first auditor's findings on cross-cycle batches. *Consequence:* infinite regress; cost scales with depth; the corpus explicitly notes no recursion-stopping rule exists. Honest assessment: this only buys variety if the second-tier auditor uses a structurally different mechanism (e.g., the second-tier auditor IS a cross-family LLM panel + human-of-record), in which case it is Option C in disguise.
- **Option C: human-of-record at audit cadence.** The independence auditor's `IndependenceAuditFinding` envelopes are queued for human review at a fixed cadence (per [F58](../failure-modes-v3.md#f58--runtimedesign-time-compliance-split) runtime-compliance shape; per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap) board-visibility shape). The human reviews the *distribution of findings*, not each FC. *Consequence:* re-introduces an F5/F42 cognitive-ceiling/escrow surface at the audit layer (the very surface D7-U-1's substrate explicitly declines to promote); requires a methodology-layer attention-design pattern for the auditor-review queue; the human becomes a substrate-named role (operator-of-record per FC opposing-side kind).

## Research-grade-uncertainty section

The *construction path* of the auditor is well-understood (designed-system; scipy/sklearn batch job). The *structural* question — *who audits the auditor, and how is the recursion terminated* — is unresolved in the corpus and is D7-U-1's own load-bearing open question. None of A/B/C dominates: A leaves coverage gaps; B is infinite regress unless it degenerates to C; C re-introduces F42 at a higher level. This is what makes the primitive research-grade-uncertainty at the structural level even though the implementation is buildable.

## Falsifiability

The claim "the independence auditor adds value above no-auditor" is falsified if, on a held-out FC corpus seeded with known collusion patterns (synthetic same-family judge pairs forced to agreement-bias), the auditor's true-positive rate is statistically indistinguishable from a coin flip at the configured threshold, OR if the false-positive rate exceeds the cost-budget for human review (Option C) / for re-falsification work (Options A/B). A 24-cycle bench with N synthetic-collusion injections and a measured `(precision, recall)` curve is the falsification harness.

## Corpus-why citation

- **D7-U-1 OQ-1** (load-bearing) — auditor-recursion is the candidate's own named open question.
- **[F1](../failure-modes-v3.md#f1--hallucination-loop) / [F27](../failure-modes-v3.md#f27--circularity--same-model-builds-and-validates) / [F46](../failure-modes-v3.md#f46--single-model-review-blindspot) / [F48](../failure-modes-v3.md#f48--tacit-collusion-via-shared-context) cascade** — distributional collusion / shared-prior agreement is the substrate's primary detection target; D7-U-1 §2 names this cascade as the FC primitive's reason to exist; the auditor is what makes that detection *measured rather than declared*.
- **[F47](../failure-modes-v3.md#f47--visible-metric-drift-goodhart-on-tokens)** — opposing-side gaming (Goodhart) is what an auditor on the FC log specifically catches at distribution scale.
- **[F51](../failure-modes-v3.md#f51--ashby-deficient-probabilistic-guard)** — a deterministic auditor against probabilistic judges is the Ashby-variety argument for why this primitive is substrate-side rather than another LLM judge.
- **[F57](../failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes)** — Patrol-tier distributional review is the structured-reporting surface that catches eligibility-classification drift.

## Buildability verdict

**research-grade-uncertainty** is the honest verdict at the *structural* level: D7-U-1's own OQ-1 about auditor recursion is unresolved; none of the three termination options is corpus-grounded as load-bearing. The *implementation* itself is `designed-system` (named tools + integration paths exist).
