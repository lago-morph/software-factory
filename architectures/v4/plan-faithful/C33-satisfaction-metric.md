# C33 — Satisfaction Metric Aggregator  (Build Plan, canonical track)

> Source / Spec ref: spec/C33-satisfaction-metric.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the metric seam contract (M1)** — the input contract (judge-output bead shape from C32/C20: per-trajectory **score** + run/scenario identity), the population/grouping key (I3, default per spec-revision), and the **output** contract (satisfaction distribution + statistics + population identity, I4). This is the interface C46/C53/C55 build against. | S | C32 judge-output shape, C20 bead type, C19 read API |
| T2 | **Pack/tool-node skeleton** — package C33 as a small Go Gas City tool node per C02/C17 ABI; config surface (population default, score-normalisation rule, optional reporting cutline, statistic set) per C03 model (README:426 "small Go tool node"). | S | C02/C17 ABI, T1 |
| T3 | **Judge-output population read (I1)** — query C19 for a population's judge-output beads by grouping key; collect scores + identities; exclude malformed/missing beads with a counted exclusion (fail-open per record). | M | T2, C19 read API, C20 type |
| T4 | **Score reduction → distribution + statistics (I2/INV-1)** — wrap **Inspect AI score reduction** + numpy/scipy/pandas to produce the distribution + summary statistics (count, central tendency, spread, quantiles). **No custom estimator** (the bar). | M | T1, T3, Inspect AI pinned |
| T5 | **Population/grouping key resolver (I3)** — resolve the trajectory set per spec-revision (default), with optional scenario/cohort slices; surface **sample count** with every result (INV-4). | S | T3 |
| T6 | **Threshold-free reporting + optional cutline (INV-3, addresses G09)** — distribution is well-defined with **no** cutline; a supplied reporting cutline adds a rate-above-cutline statistic only, never a pass/fail verdict. | S | T4 |
| T7 | **Metric result output (I4)** — emit distribution + statistics + population identity (incl. n) as the tool-node declared output; shape it for C46/C53/C55 consumption. | S | T4, T5, T6 |
| T8 | **Small-n / empty-population honesty (INV-4)** — n=0 yields an explicit insufficient-sample result; small-n is legible as small-n (underwrites F60 aggregate-vs-single-cycle). | S | T5, T7 |
| T9 | **FE-5 holistic baseline wiring (addresses FE-5)** — confirm C33 reduces **holistic** judge scores against the existing C08 spec (no C08 change); leave a clean I2/I3 extension point for per-criterion aggregation **iff** the integrator rules enumerated-DoD in (OQ-3). | S | T4, FE-5 integrator ruling (gate, not blocker) |
| T10 | **Aggregation pack (AC-1…AC-9)** — synthetic judge-output-bead harness on C19 (varied scores incl. malformed/small-n) driving all acceptance tests, especially distribution-not-boolean, threshold-free, n-surfaced, reproducible, off-the-shelf-reducer. | L | T3–T8, C19 test fixture |

## 2. Dependency graph

**Must precede C33:**
- **C32** (the judge-output score shape C33 reduces — the input contract).
- **C19/C20** (the bead store + judge-output bead type C33 reads "judge outputs from beads", README:426).
- **Inspect AI** (the score-reduction engine, version-pinned) + **C02/C17** (pack + tool-node ABI to package/invoke).

**C33 must precede (its consumers assume the satisfaction metric is the canonical number):**
- **C46** meta-metrics (cost-per-satisfaction / time-to-threshold); **C53** bootstrap-validation gate;
  **C55** methodology-experiment loop.

**Critical path inside C33:** T1 → T3 → T4 → T7 → T10. The load-bearing task is **T4 (reduction →
distribution)** — but note it is *thin*: it wraps Inspect AI score reduction + a stats library, builds **no**
custom estimator, and owns **no** durable state (C33 is a re-derivable view, INV-5). The **G09 split** (T6:
threshold-free metric, cutline deferred to C50/C53/C39) and the **FE-5 holistic baseline** (T9) are the two
decision-bearing tasks, both deliberately scoped to *avoid* new capability (no verdict in C33; no C08 change).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, two thin workstreams fan out concurrently:
- **WS-A (read/shape):** T3 (population read) → T5 (grouping key). The input spine; can build against a
  synthetic judge-output-bead fixture while C32 firms up.
- **WS-B (reduce/emit):** T4 (reduction) → T6 (threshold-free reporting) → T7 (result output) → T8 (small-n
  honesty). The stats spine; can build against synthetic score arrays before WS-A's real read lands.
- **T9 (FE-5 baseline)** rides on T4 and is independent of the read path; **T10** (aggregation pack) joins both.
WS-A and WS-B meet at the T3→T4 handoff (the collected score population).

## 4. Interfaces-first / contract milestones

- **M1 — metric seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = judge-output bead shape (score + run/scenario identity), with C32/C20;
  (b) **population key** = grouping default (per spec-revision) + slice taxonomy stub (I3);
  (c) **output** = satisfaction distribution + statistics + population identity (I4).
  Freezing M1 lets WS-A build against synthetic beads and WS-B against synthetic score arrays in parallel, and
  lets **C46/C53/C55** stub against the output shape.
- **M2 — distribution definition frozen (T4/G09):** satisfaction = judge-score distribution + statistics,
  **threshold-free** (the cutline is C50/C53/C39's, not C33's), before C46/C53/C55 reason over the metric.
- **M3 — FE-5 path fixed (T9):** holistic-vs-enumerated **`FE-5 → orchestrator/integrator decision`** ruled
  before any C08/C32 per-criterion coordination; C33 Sweep-1 ships holistic, with a clean extension point.

## 5. Risks & de-risking order

1. **Confirm first — FE-5 path (T9/OQ-3).** Surface the **holistic vs enumerated-per-criterion** decision to
   the Batch-3 integrator *before* deep build: the recommended **holistic** baseline needs **no C08 change** and
   is the cheap path; the enumerated path is a coordinated C08 + C32 + C33 change C33 must **not** make
   unilaterally. This retires the highest-coordination uncertainty and fixes C33's scope.
2. **Confirm — G09 threshold ownership (T6/OQ-1).** Verify the "satisfied" cutline lives at the **decision
   sites** (C50/C53/C39), not in C33, so C33 stays a **threshold-free** distribution (reading (b)) and does not
   accidentally re-introduce test-pass (anti-P6). A wrong call here would mis-place a values-decision inside a
   metric.
3. **Pin — Inspect AI score reduction (T4/OQ-2).** Confirm the reducer's actual reduction primitives + the
   distribution representation (continuous vs binned) against the **pinned** Inspect AI version, so the stats
   contract is reproducible and no custom estimator creeps in (the bar / AC-8).
4. **Confirm — judge-output score model + ensemble collapse (T3/OQ-4, C32 boundary).** Freeze the per-trajectory
   **score scale** and how a **multi-judge ensemble** collapses to one score against C32's real output before
   the normalisation rule (I2) sets.
5. **Measure — population scale (OQ-2).** Confirm numpy/pandas reduction is fine at L5-volume populations, or
   whether incremental/streamed reduction is needed at sweep 2 (no bespoke scaling machinery at Sweep-1).

## 6. Definition of done

**Per-component DoD:** the aggregation pack (T10) passes **AC-1…AC-9** against a synthetic judge-output-bead
population — distribution-not-boolean (P6), reads judge outputs from C19 beads, **no model call / pre-computed
verdict**, **threshold-free** (cutline only as an optional reported statistic), **n always surfaced** with an
explicit insufficient-sample path, **reproducible** reduction owning no source-of-truth, consumable by
C46/C53/C55, **off-the-shelf reducer** (Inspect AI + numpy/scipy/pandas, no custom stats engine), and the
**FE-5 holistic baseline** computed against the existing C08 spec with **no C08 change**. C33 is a small Go
tool node in a Gas City pack.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C32/C20/C46 owners; sub-streams + downstream can stub against them.
- T3/T5: a synthetic population reduces correctly; malformed beads excluded-with-count; sample count surfaced (AC-2/AC-5).
- T4/T6: distribution + statistics produced via Inspect AI score reduction (AC-1/AC-8); threshold-free, optional
  reported cutline yields no verdict (AC-4, addresses G09).
- T7: emitted metric consumable by C46/C53/C55 (AC-7).
- T8: n=0 → explicit insufficient-sample; small-n legible (AC-5).
- T9: holistic satisfaction against existing C08 spec, **no C08 change** (AC-9); per-criterion extension point
  left for the integrator's FE-5 ruling (OQ-3).
- T10: full AC suite green; **must pass before C46/C53/C55 build on the satisfaction metric**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G09 threshold value + ownership at
C50/C53/C39), OQ-2 (distribution representation + statistic set + population-scale reduction), OQ-3
(**`FE-5 → orchestrator/integrator decision`**: holistic-only vs enumerated-per-criterion DoD), OQ-4 (C32 score
model + ensemble collapse before the normalisation rule freezes).
