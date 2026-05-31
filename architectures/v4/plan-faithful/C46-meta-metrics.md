# C46 — Meta-Metric Stream  (Build Plan, canonical track)

> Source / Spec ref: spec/C46-meta-metrics.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Define the cost MODEL (M1 — core G32 deliverable)** — the spec-of-record artifact for what cost *is*: the per-run **cost vector {tokens, dollars, wall-clock time}**, the **attribution rule** (cost → trajectory/spec-revision), and the **reduction** to cost-per-satisfaction (vector ÷ C33 term). A **definition/Configuration** artifact (README:269 "Custom … your work … Configuration"), not an engine. | M | C33 satisfaction-term shape, C24 usage-signal shape, C29 price/`cost_tier` ref |
| T2 | **Freeze the meta-metric seam contract (M2)** — the inbound contracts (C33 satisfaction distribution I3; C24/CXDB usage I2; C39/C35 judge-outcome labels I6) and the **logged metric-record schema** (the time-series point: value + provenance + n + timestamp, I4) + the **output read-surface** (I5). This is what C47/C48/C50 build against. | S | T1, C33 distribution-record, C24 read API |
| T3 | **Meta-metric pack/tool-node skeleton** — package C46 as the Gas City **meta-metric pack** (README:470) per C02/C17 ABI; config surface (cost-vector dims, metric set, supplied time-to-threshold cutline, attribution/cohort keys, tracking-store binding) per C03 model ("Configuration", README:269). | S | C02/C17 ABI, C03, T2 |
| T4 | **Cost/usage signal read + cost-vector assembly (I2/INV-3)** — read recorded per-run usage: **token usage + cost are native OTLP metrics** (C25→C26; AI-CONTEXT:172) and/or recovered from CXDB-stored bodies (read via **C21** — the C24 bridge is the *writer*; spec/C24 §1 "consumers read from C21, not C24"); derive dollars = tokens × reference price (C29); assemble + attribute the {tokens,$,time} vector. **Read + derive only** — no metering. *(Metrics-path-vs-bodies source + the C24-vs-C21/C25 dep-edge = OQ-6, integrator call.)* | M | T1, T3, **C21 read API** (CXDB) / C25/C26 metrics; C24 (pinned dep) |
| T5 | **Satisfaction-term read (I3)** — read C33's **holistic** distribution (D-15) for the run/spec-revision; carry sample count n (INV-5). | S | T3, C33 output |
| T6 | **cost-per-satisfaction series (I4)** — cost vector (T4) ÷ C33 term (T5); record as a time-series point via the v4-named **MLflow/Aim/W&B** tracking pack (README:270). **Off-the-shelf store** (INV-6); no custom time-series engine. | M | T4, T5, MLflow/Aim/W&B pinned |
| T7 | **time-to-threshold series (I4/INV-4, addresses G09)** — elapsed time/run-count for a spec-revision's satisfaction (C33) to cross a **supplied** cutline; recorded only when a cutline is configured; **no** "satisfied" verdict (the cutline is C50/C53/C39's). | S | T5, T6 |
| T8 | **judge-FP-rate series (I4/I6)** — (judge-passed-but-later-found-bad) ÷ (judge-passed) from the C39/C35/human label feed; recorded as a **trailing** series over *labelled* outcomes (handles label latency). | M | T3, T6, C39/C35 label feed |
| T9 | **Multi-metric record + output/query (I5/INV-1/INV-2)** — record **all** configured metrics together (no single visible target, F47); surface the series + raw trend for C47/C48/C50. **No** significance test (C48, D-19); **no** promotion decision (C50). | S | T6, T7, T8 |
| T10 | **Signal-honesty + gap handling (INV-5)** — missing satisfaction term → insufficient-sample cost-per-satisfaction (carry n); missing cost dimension → flagged not imputed; trailing FP-rate never presents unlabelled passes as confirmed-true. | S | T6, T8, T9 |
| T11 | **Meta-metric pack acceptance harness (AC-1…AC-9)** — synthetic run-sequence (usage record + C33 distribution incl. small-n + judge-outcome labels incl. later-contradicted passes) driving all acceptance tests, especially multi-metric-time-series, cost-model division, threshold-free-except-supplied-cutline, n+gaps-surfaced, off-the-shelf-store, no-significance/no-promotion. | L | T4–T10, synthetic fixtures |

## 2. Dependency graph

**Must precede C46:**
- **C33** (the satisfaction **term** C46 divides cost by + watches for threshold-crossing — the metric C46 consumes; D-15 holistic).
- **C24** (the telemetry→CXDB bridge — C46's *pinned* dep; it lands the conversation bodies. NB C24 is the **writer**: C46's CXDB *read* seam is **C21** (spec/C24 §1), and token usage + cost are natively **OTLP metrics** on the C25→C26 path (AI-CONTEXT:172). Source-path + dep-edge correction = OQ-6, integrator call.).
- **C29** (the model `cost_tier`/price reference for the dollar dimension — related interface, not a build-blocking dep edge).
- **MLflow/Aim/W&B** (the time-series/experiment-tracking store, version-pinned) + **C02/C17/C03** (pack + tool-node ABI + config to package/run, "Configuration").
- **C39/C35** (the judge-outcome label sources for judge-FP-rate — I6; available in earlier batches by the time C46 builds).

**C46 must precede (its consumers assume the meta-metrics are the canonical "is the factory improving?" signal):**
- **C47** variant identification; **C48** A/B + statistical comparison (which reads C46's series and runs the significance test C46 withholds — D-19); **C50** promotion gate (which reads the **multiple** metrics C46 records — F47).

**Critical path inside C46:** T1 → T2 → T4 → T6 → T9 → T11. The load-bearing task is **T1 (cost-model
definition)** — it is C46's genuine G32 deliverable and the thing the whole corpus deferred to C46 (C29:G32,
C28/C32/C37/C55 cost OQs). But note the *engine* is thin: T6/T7/T8 wrap the **off-the-shelf MLflow/Aim/W&B**
store (INV-6), build **no** custom time-series engine, run **no** significance test (C48), and own **no**
source-of-truth (C46 is a derived view over C24 usage + C33 satisfaction). The **G09 split** (T7:
threshold-consumed-not-owned) and the **multi-metric mandate** (T9: no single target, F47) are the two
decision-bearing tasks, both deliberately scoped to *avoid* new capability (no verdict, no significance, no
custom store).

## 3. Parallelization

Once **T1 (cost model)**, **T2 (seam freeze)**, and **T3 (skeleton)** land, three thin workstreams fan out:
- **WS-A (cost spine):** T4 (usage read → cost vector). Can build against a synthetic usage fixture while C24
  firms up; depends on T1's vector definition.
- **WS-B (satisfaction + cost-per-sat spine):** T5 (satisfaction read) → T6 (cost-per-satisfaction series) →
  T7 (time-to-threshold). The headline-metric spine; T6 meets WS-A at the cost-÷-satisfaction join.
- **WS-C (judge-FP spine):** T8 (judge-FP-rate from the label feed). Independent of the cost/satisfaction
  spines until T9; can build against synthetic labelled outcomes.
- **T9 (multi-metric record/output)** joins WS-B + WS-C; **T10** (honesty) rides on T6/T8; **T11** (acceptance
  harness) joins all three.
WS-A and WS-B meet at the T4→T6 handoff (the assembled cost vector ÷ the satisfaction term).

## 4. Interfaces-first / contract milestones

- **M1 — cost-model definition freeze (T1, the core G32 deliverable):** the per-run **cost vector
  {tokens, $, time}**, the attribution rule, and the reduction to cost-per-satisfaction. Freezing M1 is what
  lets every cost-deferring spec (C29/C28/C32/C37/C55) finally point at a *concrete* cost model, and lets
  C48/C50 know what "cost-per-satisfaction" numerically is. The token + time dimensions are exact; the **dollar
  dimension is a modelled tokens × reference-price** whose price is operator config (OQ-1).
- **M2 — meta-metric seam contract freeze (T2):** the contracts dependents/sub-streams build against:
  (a) **inbound** = C33 satisfaction distribution (I3), C24 usage (I2), C39/C35 labels (I6);
  (b) **logged record** = the time-series point schema (value + provenance + n + timestamp, I4);
  (c) **output** = the read-surface C47/C48/C50 query (I5).
  Freezing M2 lets WS-A/B/C build against synthetic fixtures in parallel and lets **C47/C48/C50** stub against
  the output shape. **Freeze (b) jointly with C33's distribution-record** (the satisfaction term) **and C48's
  compare contract** (the significance consumer) — OQ-4.
- **M3 — G09/threshold + multi-metric posture fixed (T7/T9):** time-to-threshold **consumes** a supplied
  cutline (the cutline is C50/C53/C39's, not C46's — G09 reading (b)); and C46 records the **aggregate of
  multiple** metrics with **no single visible target** (F47), running **no** significance test (C48, D-19),
  before C47/C48/C50 reason over the streams.

## 5. Risks & de-risking order

1. **Define first — the cost model (T1/OQ-1, the core G32 deliverable).** This is the gap the whole corpus
   routed to C46; get the {tokens, $, time} vector + attribution + the cost-÷-satisfaction reduction right
   before deep build. The sharp edge: under a **flat $200/mo Max subscription** (G13) there is **no per-token
   price**, so the **dollar** dimension is a *modelled approximation* (tokens × a reference price) and that
   reference is **operator/integrator policy**, not C46-derivable. Retire this by confirming token + time are
   exact and the dollar reference is config (OQ-1) — a wrong call here would either invent a phantom price or
   block the metric on an underivable number.
2. **Confirm — G09 threshold ownership (T7/OQ-1).** Verify the "satisfied" cutline lives at the **decision
   sites** (C50/C53/C39), not in C46, so time-to-threshold **consumes** a supplied cutline (reading (b),
   inherited from C33) and C46 does not accidentally re-introduce a pass/fail verdict (anti-P6). Mirrors
   C33:OQ-1.
3. **Confirm — the significance boundary (T9/D-19).** Verify C46 records series but runs **no** significance
   test — that is **C48** (scipy/Evidently). A wrong call here would duplicate C48's stats engine inside C46
   (the bar / AC-5). Mirrors C33's identical significance→C48 boundary.
4. **Pin — MLflow/Aim/W&B tracking store (T6/OQ).** Confirm the off-the-shelf tracker's logged-series model +
   retention against the **pinned** version so the meta-metric schema is reproducible and **no** custom
   time-series engine creeps in (the bar / AC-7).
5. **Confirm — judge-FP label source + latency (T8/OQ-5).** Freeze the label sources (C39 loop-closure failure,
   C35 override, human review) and how the **trailing** FP-rate handles label latency before the judge-FP
   series sets — it must not present unlabelled passes as confirmed-true.
6. **Defer — per-criterion meta-metrics (OQ-3/D-15).** C46 reads C33's **holistic** satisfaction at Sweep-1;
   per-criterion meta-metrics are the FE-5/Sweep-2 extension (C46 is FE-5's named "built last" beneficiary).
   Do **not** require enumerated per-criterion DoD at Sweep-1; leave a clean I3/I4 extension point.

## 6. Definition of done

**Per-component DoD:** the meta-metric pack (T11) passes **AC-1…AC-9** against a synthetic run-sequence —
**meta-metrics over time** (cost-per-satisfaction, time-to-threshold, judge-FP-rate as time-series), a
**defined cost model** (per-run {tokens,$,time} vector ÷ C33 term; tokens/time exact, dollars modelled —
addresses G32), **consumes C33's holistic satisfaction** without computing it (G09 input / D-15), **multi-metric
mandatory** with no single visible target (F47), **records-not-decides** (no significance → C48, no promotion →
C50), **threshold-free except a supplied cutline** (G09 reading (b)), **n + gaps surfaced** with an explicit
insufficient-sample path, **off-the-shelf tracking store** (MLflow/Aim/W&B; no custom time-series engine), and
consumable by **C47/C48/C50**. C46 is the Gas City meta-metric pack (README:470); its definitions are
**Configuration** (README:269).

**Per-task DoD:**
- T1: M1 cost-model definition written + agreed (cost vector {tokens,$,time} + attribution + cost-÷-satisfaction
  reduction); the dollar dimension explicitly a modelled tokens × reference-price (operator config, OQ-1). **The
  core G32 deliverable.**
- T2: M2 contracts written + agreed with C33/C24/C48 owners; sub-streams + downstream (C47/C48/C50) can stub
  against them.
- T4: usage read → {tokens,$,time} vector assembled + attributed; **read + derive only**, no metering (AC-2).
- T5/T6: cost-per-satisfaction = cost ÷ C33 holistic term, recorded via the off-the-shelf tracker (AC-1/AC-7);
  consumes satisfaction, computes none (AC-3).
- T7: time-to-threshold recorded **only** against a supplied cutline, no verdict (AC-6, addresses G09).
- T8: judge-FP-rate as a **trailing** series over labelled outcomes (AC-1); label latency handled (OQ-5).
- T9: all configured metrics recorded together (AC-4 multi-metric/F47); **no** significance test, **no**
  promotion (AC-5); consumable by C47/C48/C50 (AC-9).
- T10: missing satisfaction → insufficient-sample (not a fabricated ratio); missing cost dimension flagged
  (AC-8).
- T11: full AC suite green; **must pass before C47/C48/C50 build on the meta-metrics**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G32 cost-model dollar dimension +
operator price reference under flat Max; shared cutline-value with C33:OQ-1), OQ-2 (which meta-metrics beyond
the three — AI-CONTEXT:516 "values question", config-extensible), OQ-3 (per-criterion meta-metrics — FE-5/D-15
beneficiary, Sweep-2 extension), OQ-4 (C46↔C48 compare-contract + C46↔C33 logged-record schema freeze), OQ-5
(judge-FP label source + trailing-rate latency), **OQ-6 (cost-signal telemetry source — OTLP-metrics path
C25/C26 vs CXDB-stored bodies — + the C24-vs-C21/C25 dep-edge correction; architecturally-significant,
integrator call; spec §1/§9).**
