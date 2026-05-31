# C36 — Anomaly Detection (numeric)  (Build Plan, canonical track)

> Source / Spec ref: spec/C36-anomaly-detection.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the anomaly seam contract (M1)** — the input contract (which telemetry/quality **metric series**, read via C21 I6/I2; spec/C24:65 = read from C21, not C24), the **anomaly-signal output** contract (I3: metric/series id + **trajectory pointer into C21** + score/severity), and the signal **carrier** (C20 bead type vs C23 event — OQ-2). This is the interface C37/C38 build against. | S | C21 I6/I2 read seam, C24 landing the stream, C37/C38 consumer shape |
| T2 | **Python pack/tool-node skeleton** — package C36 as a **Python** Gas City tool node per C02/C17 ABI; config surface (watched-metric set, detector choice, sensitivity/threshold) per C03 model (README:253 "Python tool node in Gas City pack"). | S | C02/C17 ABI, T1 |
| T3 | **Metric-series read + reduction (I1)** — read the watched telemetry/quality series from C21 (trajectory retrieval/query); reduce them to the numeric vectors the detector takes; exclude malformed values with a counted exclusion (fail-open per value). | M | T2, C21 read seam, C24 stream landed |
| T4 | **Off-the-shelf detector wrap (I2/INV-1)** — wrap **PyOD / Anomalib** (`github.com/yzhao062/pyod` BSD-2; `github.com/openvinotoolkit/anomalib` Apache-2.0; AI-CONTEXT:327) and/or **Prometheus-style threshold rules** (AI-CONTEXT:405) to score series → anomaly verdict + score. **No custom estimator** (the bar). Transfusion from PyOD (README:460). | M | T1, T3, PyOD/Anomalib pinned |
| T5 | **Flagging + sensitivity/threshold (I4)** — apply configured threshold; a value above it is flagged; each detector must point at a specific failure it catches (INV-5, F52). | S | T4 |
| T6 | **Anomaly-signal emit (I3/INV-3)** — emit the typed `anomaly` signal (metric/series id + trajectory pointer into C21 + score/severity) to the loop sink (C37/C38); shape it for downstream consumption. | M | T4, T5, T1 (carrier frozen) |
| T7 | **Fail-open / skip-and-re-derive (INV-4, addresses G33)** — on C21 unreachable or incomplete series (C24 mid-outage), **skip the window without crashing** and **re-score on recovery**; restart re-reads the series (no C36-side durable queue — durability is C24/C21's). | S | T3, T6 |
| T8 | **Cold-start / bad-value honesty** — too-short series → **no** fabricated anomaly ("insufficient data"); malformed value excluded-with-count; never a false flag from noise. | S | T3, T5 |
| T9 | **False-positive discipline + health events (INV-5, F52)** — surface **per-detector false-positive rate** as a first-class signal (the F52-mandated number, F-MODE-COVERAGE:100,170); emit series-scored / flags-emitted / exclusion-count health events for auditability. | S | T5, T6 |
| T10 | **Anomaly-detection pack (AC-1…AC-9)** — synthetic-metric-series harness in C21 (clean / known-anomalous / drift / cold-start / malformed) driving all acceptance tests, especially flag-with-traceable-signal, off-the-shelf-detector, fail-open-over-C21-outage, and FP-rate-surfaced. | L | T3–T9, C21 conformance + C24 integration packs passing |

## 2. Dependency graph

**Must precede C36:**
- **C21** (the CXDB read seam C36 reads metric series from — conformance pack passing; spec/C21 AC-1…AC-8).
- **C24** (the bridge that **lands** the telemetry/metric stream into CXDB — integration pack passing; C36's
  series exist because C24 delivered them, though C36 reads via C21).
- **PyOD / Anomalib** (the detector engines, version-pinned) + **C02/C17** (pack + tool-node ABI to
  package/invoke the Python tool node).

**C36 must precede (its consumers assume the anomaly signal is the canonical heal-loop trigger):**
- **C37** trajectory clustering (embeds + clusters the flagged failures); **C38** diagnosis agent (Healer,
  reached through C37); and through them **C39** fix-task & loop-closure.

**Critical path inside C36:** T1 → T3 → T4 → T6 → T10. The load-bearing task is **T6 (anomaly-signal emit)** —
the one genuinely custom surface (the wiring of detection → downstream that opens the heal loop, README:248) —
but note **T4 (the detector) is *thin*: it wraps PyOD/Anomalib/Prometheus, builds **no** custom estimator, and
owns **no** durable state** (C36 is a read-side detector + router, INV-4). The **G33 handling (T7: fail-open /
skip-and-re-derive)** is deliberately scoped to *avoid* new capability (no C36-side durable queue — durability
is C24/C21's), and **T9 (F52 FP discipline)** is the one piece of explicit discipline the P11 self-healing
surface demands.

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, two thin workstreams fan out concurrently:
- **WS-A (read/score):** T3 (metric read/reduce) → T4 (detector wrap) → T5 (flagging). The detection spine;
  can build against a synthetic metric-series fixture while C24's real landing firms up.
- **WS-B (emit/resilience):** T6 (anomaly-signal emit) → T7 (fail-open / skip-and-re-derive) → T8 (cold-start
  honesty) → T9 (FP discipline + health events). The signal/ops spine; can build against synthetic detector
  output before WS-A's real scoring lands.
- **T10** (anomaly-detection pack) joins both. WS-A and WS-B meet at the T4/T5→T6 handoff (the flagged value
  becoming a signal).

## 4. Interfaces-first / contract milestones

- **M1 — anomaly seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = the watched metric-series read shape (via C21 I6/I2; provenance = C24);
  (b) **output** = the `anomaly`-signal record (metric/series id + trajectory pointer into C21 + score/severity, I3);
  (c) **carrier** = C20 bead type vs C23 event (OQ-2).
  Freezing M1 lets WS-A build against synthetic series and WS-B against synthetic detector output in parallel,
  and lets **C37/C38** stub against the anomaly-signal shape.
- **M2 — detector + thresholds fixed (T4/T5):** PyOD/Anomalib/Prometheus selection per metric class +
  sensitivity/threshold defaults, **off-the-shelf, no custom estimator** (the bar / AC-2), before C37/C38
  reason over the flagged anomalies.
- **M3 — durability inheritance fixed (T7/G33):** fail-open / skip-and-re-derive with **no C36-side queue**
  (durability is C24's inbox-spool + C21's fail-open), before C37/C38 depend on anomaly completeness — and the
  inherited coverage ceiling (C24 inbox/disk bound) is documented (OQ-1).

## 5. Risks & de-risking order

1. **Confirm first — the metric-stream read seam (T1/T3/OQ-1).** Resolve the **C24-vs-C21 boundary** (inventory
   lists both as deps; C24's spec says C36 reads from **C21**, spec/C24:65) and **which metric series** are the
   Sweep-1 watched set (CXDB trajectory-derived telemetry vs the OTLP/metrics path on C25/C26 — the inventory
   points C36 at the CXDB/C24 side). A wrong call here mis-locates C36's input. This retires the highest seam
   uncertainty and fixes C36's scope.
2. **Pin — PyOD / Anomalib (T4/AC-2).** Confirm the detector APIs + which detector fits which metric class
   (lightweight PyOD vs Anomalib/PyTorch vs Prometheus threshold) against the **pinned** versions, so the
   detection contract is reproducible and **no custom estimator creeps in** (the bar / AC-2). Mirrors C21's
   version-pin discipline.
3. **Spike — G33 fail-open / skip-and-re-derive (T7).** Prove C36 **skips a window during a C21/C24 outage
   without crashing** and **re-scores on recovery**, and that a C36 restart re-reads the series (no anomaly
   lost that the series still holds). Confirm **no C36-side durable queue** is added (durability stays C24/C21's),
   and document the inherited ceiling (C24 inbox/disk bound, spec/C24 OQ-4). Validates AC-6.
4. **Confirm — false-positive discipline (T9/INV-5/F52).** Verify every detector points at a specific failure
   it catches and its **FP rate is measurable/surfaced** (F-MODE-COVERAGE:100,170) — the explicit guard against
   the "more controller patches" trap the docs warn P11 is most prone to. The *quantified* FP/recurrence policy
   is sweep-2 (OQ-2).
5. **Confirm — the carrier + downstream contract (T6/OQ-2).** Freeze whether the anomaly signal is a **C20 bead
   type** or a **C23 event**, and that C37/C38 consume it as the canonical trigger, before deep build of the
   emit path.
6. **Confirm — F4 quality-metric scope (OQ-4).** Confirm **which quality series exist** for C36 to watch at
   Phase 3b (defining new quality metrics is out of scope; F4 "quality metric definition is itself a hard
   problem"), so F4 coverage is honestly scoped as Partial.

## 6. Definition of done

**Per-component DoD:** the anomaly-detection pack (T10) passes **AC-1…AC-9** against synthetic metric series in
C21 — detects-anomalies-flags-clean, **off-the-shelf detector** (PyOD/Anomalib/Prometheus, **no custom anomaly
algorithm**), **actionable anomaly signal** carrying the trajectory pointer into C21, **detect-only** (no
diagnosis/fix/values-decision), **read-side / no source-of-truth** (re-derivable), **fail-open / skip-and-re-derive
over a C21 outage** (G33, no C36-side queue), **false-positive rate surfaced per detector** (F52), cold-start /
bad-value honesty, and **simplest-first scope** (no clustering/diagnosis/fix-gen/LLM-trajectory layer). C36 is a
**Python** tool node in a Gas City pack.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C21/C24/C37/C38 owners; sub-streams + downstream can stub against them.
- T3/T8: a synthetic series scores correctly; malformed values excluded-with-count; cold-start yields no false
  flag (AC-1/AC-8).
- T4/T5: anomaly verdict + score produced via **PyOD/Anomalib/Prometheus** (AC-1/AC-2); each detector points at
  a falsifying scenario (AC-7, F52).
- T6: emitted anomaly signal carries the trajectory pointer + score and is consumable by C37/C38 (AC-3).
- T7: AC-6 — C21 down → skip-window/no-crash → re-score on recovery; restart loses no anomaly the series still
  holds; **no custom durable queue** introduced (G33 inherited from C24/C21); ceiling documented (OQ-1).
- T9: per-detector **false-positive rate surfaced** (AC-7); health events visible (series-scored / flags / exclusions).
- T10: full AC suite green; built **after** C21 conformance + C24 integration packs pass; **must pass before
  C37/C38 build on the anomaly signal**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (metric-stream read seam C24/C21
boundary + inherited G33 ceiling + which metric series), OQ-2 (detector selection + signal carrier [C20 bead
vs C23 event] + thresholds + quantified FP/recurrence policy + batch-vs-streamed scoring), OQ-3 (LLM-trajectory
/ semantic anomaly boundary — C36 is the numeric generic base, semantic layer composes *on* it), OQ-4 (F4
quality-metric scope — which quality series exist at Phase 3b).
