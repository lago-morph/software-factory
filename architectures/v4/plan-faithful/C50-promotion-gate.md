# C50 — Promotion gate  (Build Plan, canonical track)

> Source / Spec ref: spec/C50-promotion-gate.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the gate seam contract (M1)** — the **promotion rule** (I1: C48 significance-better ∧ C46 metric panel coherent ∧ Goodhart guard "no guard metric materially regressed"), the **decision-record** shape (I4: `promote`/`hold` + evidence bundle = C48 verdict ref, C46 panel + guard check, C12 variant id + replaced incumbent, sample count), and the **inputs it reads** (C48 significance verdict, C46 metric panel, C12 challenger id, C56 autonomy level). This is the contract C12/C03 (default reference) + the run tier build against. | S | C48 verdict shape (D-19), C46 metric-panel output, C12 default-reference, C56 autonomy read |
| T2 | **Control-loop artifact skeleton + config surface** — package C50 as the Batch-5 self-optimization-pack gate; config (the **metric panel + which metrics are guard metrics**, the **satisfaction + guard cutline values + decision rule**, the **C56 autonomy gate** for auto-flip) per C03 model. **No model call / no stats engine** (the bar; D-19 routes significance to C48). | S | C02/C17 ABI, C03 config model, T1 |
| T3 | **Significance-verdict intake (I5/INV-2, D-19)** — read the **C48** "was the variant actually better?" verdict + its sample/effect statistics. Pure read of a pre-computed verdict; **no significance computation**. Absent/inconclusive/not-significant ⇒ feeds `hold`. | S | T1, C48 verdict |
| T4 | **Metric-panel + satisfaction read (I1/INV-3)** — pull the **C46 metric panel** (cost-per-satisfaction, time-to-threshold, judge-FP-rate, the C33 satisfaction summary) for **both** challenger and incumbent. Pure read of pre-computed metrics; surface n (sample-honesty, inherits C33:INV-4 via C46). | M | T1, C46 panel, C33 summary |
| T5 | **Multi-metric rule + Goodhart guard (I1/I2/INV-1 — the genuine KEEP)** — evaluate the **conjunction**: C48 significant ∧ panel coherent ∧ **no guard metric materially regressed**. **Apply the satisfaction + guard cutlines here** (the cutlines C33 defers to this decision site, D-15/G09). Cutline **values + guard set** = config/operator policy (OQ-1), not hard-coded. **Reject a single-metric promotion** (F47/B78). | M | T2, T3, T4 |
| T6 | **Default-flip on promote (I3/INV-4/INV-5)** — on `promote`, **update the default formula reference** (C12/C03) to the challenger; on `hold`, **no-op on the default**. Subject to the **C56 autonomy gate** (auto-flip vs. surface-for-ratification). **Retain the prior default** for reversibility. | M | T5, C12/C03 default reference, C56 autonomy gate |
| T7 | **Decision record emit (I4/INV-4)** — write **`promote`/`hold`** + the **evidence bundle** to a bead (C20/C19), attributed (C41), auditable + **reversible** (records the prior default it can revert to). | S | T5, T6, C20 slot, C19 write, C41 attribution |
| T8 | **Recurrence wiring (INV-6)** — re-invoke the gate for **each** challenger that clears C48; a promoted formula becomes the incumbent the next challenger is measured against. (Distinct from C53 one-time; owns **no** C39 fix-loop policy.) | S | T6, T7 |
| T9 | **Promotion-gate harness (AC-1…AC-10)** — synthetic promote/hold driver: seed a **C48 verdict** (significant/not/inconclusive/absent), a **C46 panel** (all-up; satisfaction-up-but-cost-up = the Goodhart case; thin-sample), a **C12 challenger id**, a **C56 level** (auto-flip/ratify); drive all ACs — **multi-metric conjunction + Goodhart guard**, **significance consumed not recomputed**, **bars applied here + configurable**, **promote flips default / hold no-op**, **recorded + reversible**, **recurring**, **no fix-loop policy**, **no second stats/metric engine**. Headline assertion = the **Goodhart case** ⇒ `hold`. | L | T3–T8, synthetic input fixtures |

## 2. Dependency graph

**Must precede C50:**
- **C48** (A/B routing + statistical comparison) — supplies the **significance verdict** C50 consumes (D-19); C50 runs no stats.
- **C46** (meta-metric stream) — supplies the **metric panel + cost model** C50's multi-metric rule + Goodhart guard read.
- **C33** (satisfaction metric) — the **threshold-free** distribution whose cutline routes to **C50** (C33 §6); reachable via C46.
- **C12** (formula) — the **variant** being promoted *is* a formula; C50 flips the **default formula reference** (with C03 config).
- **C49** (counterfactual replay) — reaches C50 only *transitively via C48* (**not** a C50 dependency edge — C50's inventory deps are C48/C12); it produces the comparable variant evidence C48's significance verdict is computed over (G19, the hard unsolved invention the whole P12 batch waits on).
- **C20/C19** (bead schema + store the decision is recorded on) + **C41** (attribution) + **C02/C03** (pack + config to host/configure the gate).
- **C56** (autonomy ladder) — the policy seam gating auto-flip vs. human ratification (not a hard inventory dep; parity with C39's L5 ship-auth).

**C50 must precede (its promotion changes the live default):**
- **C18 reconciler / C05 dispatch** — subsequent work instantiates the **new** default formula once C50 flips the reference (effect, not an owned interface).

**Critical path inside C50:** T1 → T3/T4 → T5 → T6 → T7 → T9. The load-bearing task is **T5 (multi-metric
rule + Goodhart guard)** — the genuine KEEP — but note it is *thin*: it composes pre-computed signals
(C48 verdict + C46 panel), applies **configurable** cutlines (no hard-coded number, OQ-1), builds **no**
stats engine (D-19), and owns **no** durable state beyond the decision record + the default-reference flip
(C50 is a re-derivable decision over upstream signals). The **G18-contribution + F47-closing** tasks are
**T5 (multi-metric rule/guard)** + **T6 (default-flip, reversible)** + **T7 (recorded decision)** — together
they make the promotion loop terminate each cycle in a **recorded, multi-metric, Goodhart-guarded** verdict;
all three are deliberately scoped to *avoid* new capability (no significance engine — C48; no metric
definitions — C46; no variant generator — C47; no fix-loop policy — C39/XC-3).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton + config)** land, two thin workstreams fan out concurrently:
- **WS-A (evidence read):** T3 (C48 significance verdict) + T4 (C46 metric panel + C33 satisfaction). The
  input spine; can build against **synthetic** C48 verdicts / C46 panels / C33 summaries while those
  upstreams firm up.
- **WS-B (decide/flip/record):** T5 (multi-metric rule + Goodhart guard) → T6 (default-flip, autonomy-gated,
  reversible) → T7 (decision record) → T8 (recurrence). The decision spine; can build against **synthetic**
  evidence bundles before WS-A's real reads land.
- **T9 (harness)** joins both. WS-A and WS-B meet at the T4 → T5 handoff (the collected challenger-vs-incumbent
  evidence bundle).

## 4. Interfaces-first / contract milestones

- **M1 — gate seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **promotion rule** = the conjunction terms (C48 significance / C46 panel coherence / Goodhart guard) + the decision rule;
  (b) **decision record** = `promote`/`hold` + evidence bundle (a **C20 schema-slot request**);
  (c) **inputs** = C48 verdict ref, C46 panel, C12 challenger id + the default-reference it flips, C56 level.
  Freezing M1 lets WS-A build against synthetic evidence and WS-B against synthetic bundles in parallel, and
  lets **C12/C03** agree the default-reference-update seam the flip targets.
- **M2 — multi-metric rule + Goodhart guard fixed (T5/F47/G09):** the promote/hold is a **multi-metric
  conjunction with a Goodhart guard** with the **satisfaction + guard cutlines applied at C50** (configurable
  values + guard set, OQ-1), before any default-flip. This is the **F47 close + C50's G18 contribution** at
  sweep-1 altitude (the promotion loop's recorded stopping rule).
- **M3 — default-flip + decision slot agreed (T6/T7):** the **default-formula-reference update** mechanism is
  reconciled with **C12/C03** (who owns the reference; how a flip is applied + reverted), and the
  `promote`/`hold` decision slot is agreed as a **C20 schema-slot request** (parity with C39/C53's
  record-on-bead), before any flip or bead-write.

## 5. Risks & de-risking order

1. **Confirm first — G09 cutline ownership + values + guard set (T5/OQ-1).** Verify the satisfaction (and
   guard-metric) cutlines are **applied at C50** (D-15 reading), not pushed into C33 (which stays
   threshold-free), and that their **values + which metrics are guards** are operator/integrator policy (the
   "values question", AI-CONTEXT:516; shared with C33:OQ-1, C53:OQ-1, C51:OQ-C51-3). A wrong call here
   mis-places a values-decision inside the metric (anti-P6) or hard-codes a number v4 deliberately leaves
   open. Highest shared-policy uncertainty.
2. **Confirm — the C48 significance seam (T3/D-19).** C50 **consumes** C48's "was it actually better?"
   verdict and must **not** re-run statistics (D-19 routes significance to C48). Pin the verdict contract
   (verdict + sample/effect stats) *before* deep build so C50 stays a decision-over-signals, not a second
   stats engine. (C48 is a Batch-5 peer not yet on disk — build against a synthetic verdict; freeze the
   contract when C48 is authored.)
3. **Confirm — the multi-metric rule shape (T5/OQ-2).** How "**moving coherently**" / "**materially
   regressed**" is operationalised over C46's statistics (per-metric bar vector? Pareto-dominance? weighted
   composite under a no-regression constraint?) is unfixed. Pin the *requirement* (it MUST stay multi-metric
   + guard-checked, INV-1/F47); defer the exact rule to sweep-2 with C46/C48. **Do not** let it collapse to a
   single metric (the whole F47 point).
4. **Confirm — default-flip + reversibility seam (T6/OQ-3).** The flip updates the **C12/C03 default
   reference**; reversibility requires retaining the prior default. Pin who owns the reference + how a flip is
   applied/reverted; decide manual-vs-automated rollback at sweep-2 (do not build a rollback engine at
   sweep-1 — the bar).
5. **Confirm — C56 autonomy gate on the flip (T6/OQ-4).** Whether a `promote` **auto-flips** or **surfaces
   for ratification** is gated on C56 (README:498 "required until P12 is mature and trusted"; parity with
   C39's L5 ship-auth). Pin the seam; defer the level threshold to sweep-2 with C56.
6. **Measure — Goodhart honesty.** C50 makes the promotion **multi-metric + recorded + reversible**; it does
   **not** eliminate Goodhart ("applies recursively to meta-metrics", F-MODE-COVERAGE:63). Keep the artifact
   thin and the residual honest (the recursive-Goodhart + objective-drift residual lives at C57 + the F54
   audit pack, G35).

## 6. Definition of done

**Per-component DoD:** the promotion-gate harness (T9) passes **AC-1…AC-10** against a synthetic
promote/hold decision — a **multi-metric conjunction with a Goodhart guard** (C48 significant ∧ C46 panel
coherent ∧ no guard metric regressed), **never single-metric** (F47/B78), **significance consumed from C48
not recomputed** (D-19), the **satisfaction + guard cutlines applied at C50** with **configurable values +
guard set** (D-15/G09), a `promote` that **flips the default formula reference** (C12/C03, autonomy-gated via
C56) and a `hold` that is a **no-op on the default**, the **decision recorded + reversible** on a bead (retains
the prior default), **recurring** (fires per challenger; distinct from C53 one-time; owns **no** C39 fix-loop
policy, XC-3), and **engine-reuse** (composes C48 + C46 + C33 over a C12 variant; no second
significance/metric/variant-gen/replay/registry engine). C50 is a thin gate-shaped control-loop, not a
measurement loop.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C48/C46/C33/C12/C03/C56 owners; sub-streams can stub against them.
- T3: C48 verdict read as a **pre-computed verdict**; no significance computation; absent/non-significant ⇒ `hold` (AC-2).
- T4: C46 panel + C33 satisfaction read for challenger **and** incumbent; n surfaced (AC-1 inputs).
- T5: rule evaluates as a **multi-metric conjunction with a Goodhart guard** (AC-1/AC-6); **cutlines applied here**, configurable values + guard set (AC-3); single-metric promotion **rejected**.
- T6: `promote` **flips** the default formula reference (autonomy-gated, AC-10); `hold` leaves the incumbent **unchanged** (AC-4); prior default **retained** for reversibility.
- T7: `promote`/`hold` + evidence bundle **recorded** on a bead, attributable, **reversible** (AC-5).
- T8: gate fires for **each** challenger clearing C48; promoted formula becomes the next incumbent (AC-7); owns **no** fix-loop policy (AC-8).
- T9: full AC suite green; **headline = the Goodhart case** (satisfaction up + cost-per-satisfaction up ⇒ `hold`, AC-1/AC-6).

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G09 promotion cutline values +
guard-metric set + cutline ownership at C50, shared C33/C53/C51), OQ-2 (multi-metric decision-rule shape —
must stay multi-metric, F47), OQ-3 (reversibility / regression-triggered rollback policy), OQ-4 (C56 autonomy
gate on the default-flip, parity with C39 L5 ship-auth).
