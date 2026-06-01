# C33 — Satisfaction Metric Aggregator  (Build Plan, canonical track)

> Source / Spec ref: spec/C33-satisfaction-metric.md
>
> **Sweep-2 additions (2026-06-01):** Concrete task table updated with sweep-2 deliverables (signatures,
> schema, E/AC tables, diagram, D-36 bead-write). Interface-first milestone M1 updated with frozen fields.
> OQ-1/OQ-2/OQ-4 resolved; task sizes updated to reflect thin-but-concrete surface.

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the metric seam contract (M1)** — the input contract (C32 `ScoreRecord` consumed fields: `score_value float64 [0.0,1.0]`, `scenario_id`, `trajectory_ref`, `independence_level`; D-39 frozen), the population/grouping key (I3, default `spec_revision`), and the **output** contract (`SatisfactionDistribution` schema §3.4: `n`, `mean`, `p10`, `p50`, `p90`, `std_dev`, `rate_above_cutline?`, `excluded_count`, `computed_at`). This is the interface C46/C53/C55 build against. | S | C32 Sweep-2 `ScoreRecord` freeze (D-39), C19 read API |
| T2 | **Pack/tool-node skeleton** — package C33 as a small Go Gas City tool node per C02/C17 ABI; pack TOML config surface (`grouping_key`, `grouping_value`, optional `report_cutline`) per C03 model (README:426 "small Go tool node"); register `satisfaction_metric` bead type with C22 at install (D-3). | S | C02/C17 ABI, T1, C22 `register_bundle` |
| T3 | **Judge-output population read (I1)** — query C19 for a population's judge-output beads by grouping key; collect `score_value` + identity fields; apply E-C33-02 exclusion (absent/OOB score_value → exclude + increment `excluded_count`); surface E-C33-05 on C19 failure. | M | T2, C19 read API, C20 bead type |
| T4 | **Score reduction → distribution + statistics (I2/INV-1)** — wrap v4's named **Inspect AI score reduction** (companion: MLflow tracking, AI-CONTEXT:393) + a thin distribution-summary helper (`[FAITHFUL-FILL]`: v4 names no stats library for C33; scipy is C48's significance engine, README:275) to produce `mean`, `p10`, `p50`, `p90`, `std_dev` over the `score_value` slice. **No custom estimator** (the bar). Handle E-C33-04 saturation signal (std_dev ≈ 0). | M | T1, T3, Inspect AI pinned |
| T5 | **Population/grouping key resolver (I3)** — resolve the trajectory set per spec-revision (default), with optional scenario/cohort slices; surface **sample count** `n` with every result (INV-4); handle E-C33-01 empty-population case (n=0 → degenerate result, no crash) and E-C33-03 (grouping_value not found → same as n=0). | S | T3 |
| T6 | **Threshold-free reporting + optional cutline (INV-3, addresses G09/OQ-1 RESOLVED)** — distribution is well-defined with **no** cutline; a supplied `report_cutline` (validated at pack start per E-C33-06) adds `rate_above_cutline` statistic only, never a pass/fail verdict; no `verdict`/`pass`/`satisfied` field in schema. | S | T4 |
| T7 | **Bead-write (D-36) + metric result output (I4)** — write `SatisfactionDistribution` to C19 as `"softwarefactory.v4.beads:satisfaction_metric"` bead (D-36; D-2 namespace; D-29 `created_by` wire format); emit bead_id + full stats as tool-node declared output for C46/C53/C55 consumption. | S | T4, T5, T6, C19 write API |
| T8 | **Small-n / empty-population honesty (INV-4, E-C33-01)** — n=0 yields explicit degenerate result with stat fields absent; small-n `excluded_count` always surfaced; E-C33-04 saturation event logged. | S | T5, T7 |
| T9 | **FE-5 holistic baseline wiring (addresses FE-5)** — confirm C33 reduces **holistic** judge scores against the existing C08 spec (no C08 change; D-15); leave a clean I2/I3 extension point for per-criterion aggregation iff the integrator rules enumerated-DoD in (OQ-3 RESOLVED: deferred). | S | T4, D-15 |
| T10 | **E-code + AC-code test pack (AC-C33-01…AC-C33-18)** — synthetic judge-output-bead harness on C19 (varied scores incl. malformed/small-n/saturated) driving all acceptance tests; E↔AC cross-references verified; in particular: distribution-not-boolean, threshold-free, n-surfaced, reproducible, bead-written (D-36), off-the-shelf-reducer. | L | T3–T8, C19 test fixture |

## 2. Dependency graph

**Must precede C33:**
- **C32** (the judge-output `ScoreRecord` shape C33 reduces — frozen by D-39; `score_value float64` + fields §3.3).
- **C19/C20** (the bead store + judge-output bead type C33 reads and the `satisfaction_metric` bead C33 writes, D-36).
- **C22** (`register_bundle` for the `satisfaction_metric` bead type, D-3 seam; T2).
- **Inspect AI** (the score-reduction engine, version-pinned) + **C02/C17** (pack + tool-node ABI to package/invoke).

**C33 must precede (its consumers assume the satisfaction metric is the canonical number):**
- **C46** meta-metrics (cost-per-satisfaction / time-to-threshold); **C53** bootstrap-validation gate;
  **C55** methodology-experiment loop.

**Critical path inside C33:** T1 → T3 → T4 → T7 → T10. The load-bearing task is **T4 (reduction →
distribution)** — but note it is *thin*: it wraps Inspect AI score reduction + a stats library, builds **no**
custom estimator, and owns **no** durable state beyond the C19 bead it writes (C33 is a re-derivable view,
INV-5). The **G09 split** (T6: threshold-free metric, cutline deferred to C50/C53/C39) and the **FE-5 holistic
baseline** (T9) are the two decision-bearing tasks, both deliberately scoped to *avoid* new capability (no
verdict in C33; no C08 change).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, two thin workstreams fan out concurrently:
- **WS-A (read/shape):** T3 (population read) → T5 (grouping key). The input spine; can build against a
  synthetic judge-output-bead fixture while C32 firms up. E-C33-02/E-C33-05 paths are in this stream.
- **WS-B (reduce/emit):** T4 (reduction) → T6 (threshold-free reporting) → T7 (bead-write + result output) → T8
  (small-n honesty). The stats spine; can build against synthetic score arrays before WS-A's real read lands.
  E-C33-01/E-C33-04/E-C33-06 paths are in this stream.
- **T9 (FE-5 baseline)** rides on T4 and is independent of the read path.
- **T10** (test pack) joins both; E↔AC cross-references verified at join.

WS-A and WS-B meet at the T3→T4 handoff (the collected score population).

## 4. Interfaces-first / contract milestones

- **M1 — metric seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = C32 `ScoreRecord` consumed fields (`score_value float64 [0.0,1.0]`, `scenario_id`,
  `trajectory_ref`, `independence_level`; D-39 frozen at Sweep-2);
  (b) **population key** = `{grouping_key, grouping_value}` config pair + slice taxonomy stub (I3);
  (c) **output** = `SatisfactionDistribution` schema (§3.4 fields: `bead_id`, `bead_type`, `created_by`,
  `grouping_key`, `grouping_value`, `n`, `mean`, `p10`, `p50`, `p90`, `std_dev`, `rate_above_cutline?`,
  `excluded_count`, `independence_levels?`, `computed_at`).
  Freezing M1 lets WS-A build against synthetic beads and WS-B against synthetic score arrays in parallel, and
  lets **C46/C53/C55** stub against the output schema.
- **M2 — distribution definition frozen (T4/T6/G09):** satisfaction = judge-score distribution + statistics,
  **threshold-free** (INV-3; no verdict field in schema; OQ-1 RESOLVED), before C46/C53/C55 reason over the
  metric. `SatisfactionDistribution.rate_above_cutline` is present only if `report_cutline` is configured.
- **M3 — bead-write and bead-type registration (T2/T7, D-36/D-3):** `satisfaction_metric` type registered
  with C22; C33 writes the result bead to C19 per invocation; bead queryable by C46 via
  `gc bd find --type softwarefactory.v4.beads:satisfaction_metric`.
- **M4 — FE-5 path fixed (T9):** holistic-vs-enumerated **`FE-5 → DEFERRED` (D-15)** confirmed; C33 Sweep-1
  ships holistic only, with a clean extension point for per-criterion aggregation.

## 5. Risks & de-risking order

1. **[RESOLVED] FE-5 path (T9/OQ-3) — D-15 rules holistic only.** No C08 change required; C33's scope
   is fixed. De-risked.
2. **[RESOLVED] G09 threshold ownership (T6/OQ-1) — threshold-free confirmed.** C33 carries no cutline/verdict;
   the schema has no `satisfied` field. De-risked.
3. **Pin — Inspect AI score reduction (T4/OQ-2).** Confirm the reducer's actual reduction primitives + stats
   library (the thin helper behind Inspect AI's per-task reduction for quantiles/spread) against the **pinned**
   Inspect AI version. OQ-2 chose continuous scores + {mean, p10, p50, p90, std_dev} — verify these are
   computable with the pinned version's Python-layer reduction surface without a custom estimator.
4. **[RESOLVED] C32 score scale + ensemble collapse (T3/OQ-4, D-39).** `score_value float64 [0.0,1.0]` frozen.
   C33's normalisation rule (E-C33-02) is pinned. De-risked.
5. **Bead-type registration (T2, D-3/D-36).** Confirm the `register_bundle` seam (C22) accepts a new type
   `satisfaction_metric` without a full bundle re-version; if C22 requires a version bump, coordinate with C22
   owner.

## 6. Definition of done

**Per-component DoD:** the aggregation pack (T10) passes **AC-C33-01…AC-C33-18** against a synthetic
judge-output-bead population — distribution-not-boolean (P6), reads judge outputs from C19 beads, **no model
call / pre-computed verdict**, **threshold-free** (cutline only as an optional reported statistic, INV-3; no
`verdict` field), **n always surfaced** with an explicit insufficient-sample path (E-C33-01), **reproducible**
reduction owning no source-of-truth, **bead written to C19** per invocation (D-36), consumable by C46/C53/C55,
**off-the-shelf reducer** (v4-named Inspect AI score reduction + a thin stats helper [FAITHFUL-FILL]; no custom
stats engine — scipy significance is C48's), and the **FE-5 holistic baseline** computed against the existing
C08 spec with **no C08 change** (D-15). C33 is a small Go tool node in a Gas City pack.

**E↔AC contract verified:** every E-code in §6.1 of the spec is exercised by at least one AC-C33-NN in §8.2.
Missing E↔AC cross-reference = test pack incomplete.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C32/C20/C46 owners; sub-streams + downstream can stub against them.
- T2: pack skeleton starts; `report_cutline` out-of-range triggers E-C33-06 and refuses start.
- T3/T5: a synthetic population reduces correctly; malformed beads excluded-with-count (E-C33-02); E-C33-05 on C19 failure; sample count surfaced (AC-C33-02/AC-C33-05/AC-C33-11).
- T4/T6: distribution + statistics produced via Inspect AI score reduction (AC-C33-01/AC-C33-08/AC-C33-10); threshold-free, optional reported cutline yields no verdict (AC-C33-04/AC-C33-13, INV-3, addresses G09).
- T7: bead written to C19 per invocation (D-36); queryable by C46 (AC-C33-17); emitted to caller (AC-C33-07).
- T8: n=0 → explicit degenerate result (E-C33-01; AC-C33-12); E-C33-04 saturation event logged (AC-C33-18).
- T9: holistic satisfaction against existing C08 spec, **no C08 change** (AC-C33-09); per-criterion extension point left (OQ-3 DEFERRED, D-15).
- T10: full AC suite green; E↔AC cross-refs verified; **must pass before C46/C53/C55 build on the satisfaction metric**.

**Open questions resolved (all OQs settled at Sweep-2):**
- OQ-1 RESOLVED: C33 is threshold-free; schema has no `verdict` field; cutline at C50/C53/C39.
- OQ-2 RESOLVED: continuous scores; stats = {n, mean, p10, p50, p90, std_dev}; batch mode at Phase-2 sizes.
- OQ-3 RESOLVED by D-15: FE-5 holistic-only, per-criterion deferred.
- OQ-4 RESOLVED by D-39: `score_value float64 [0.0,1.0]` from C32; ensemble collapse is C32's.
