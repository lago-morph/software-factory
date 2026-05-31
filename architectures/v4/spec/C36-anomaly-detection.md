# C36 — Anomaly Detection (numeric)  (Spec, canonical track)

> Source: README §"Principle 11 — Self-healing loop" (line 248 "Observability → anomaly → diagnosis → fix →
> ship, without human intervention"; line 253 table row "**Anomaly detection (numeric) | Detects unusual
> patterns | PyOD, Anomalib | BSD / Apache 2.0 | Python tool node in Gas City pack**"; line 261 "PyOD +
> sentence-transformers + HDBSCAN handle clustering; the diagnosis agent is the focused work"; Phase 3b lines
> 459–466 "**Anomaly detection pack (transfusion from PyOD)**" + "**Build the simplest first (anomaly
> detection)**; save the diagnosis agent for after the substrate is proven"); AI-CONTEXT §"12 principles"
> (line 41 "Self-healing loop | Observability → anomaly → diagnosis → fix, no human"), §"Layer 4 — self-healing
> loop (P11)" (line 327 "**Numeric anomaly detection | PyOD, Anomalib | BSD-2/Apache 2.0 | Mature generic**";
> line 328 "LLM-trajectory anomaly | None turnkey | DIY | **Compose on generic**"), §Phase-1 (line 397 "CXDB
> substrate ready for **P11 anomaly clustering**"), §Phase-3b (lines 403–406 "Anomaly detection: **Anomalib
> (PyTorch), PyOD, Prometheus alerting patterns**"), §10 license table (line 310 "PyOD | BSD-2-Clause | Clean";
> line 311 "Anomalib | Apache 2.0 | Clean"), §15.2 repos (line 647 "PyOD: `github.com/yzhao062/pyod`"; line 648
> "Anomalib: `github.com/openvinotoolkit/anomalib`"); component-inventory C36 row (line 48 "Detects unusual
> patterns on telemetry/quality metrics (PyOD/Anomalib); **first/simplest P11 piece**"; maps A56/B33; depends
> **C24, C21**; gap **G33**; foundational no) + Batch-4 note (line 113 "Anomaly→cluster→diagnose→fix
> loop-closure … This is 'factory builds factory'"); spec/C21 §2 (line 81 "C36 Anomaly detection … reads …
> over trajectories stored in C21"), §3 I6 (line 103 "Replay / trajectory retrieval … C36/C37/C38/C49
> consume"), §6 (G33 fail-open at the store); spec/C24 §1 boundary (line 65 "C36/C37/C38/C49 read from C21, not
> from C24"), §6 (G33 retain-in-inbox at the bridge); F-MODE-COVERAGE §3 (F4 quality-teardown, **F22 zombie
> agents "Anomaly detection on session liveness (PyOD on telemetry)"**, F40/F57/F24/F7 drift-detection),
> §"Layer 3" F8 (line 85 "Healer's anomaly detection includes knowledge-store freshness"), §11 F54 (line 93
> "CXDB content-addressed history + Healer anomaly detection on objective shift"), F52 caution (line 100 the
> "more controller patches" trap); ambiguities-and-gaps G33; review-log D-6 (canonical track).
> Inventory ID: C36   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C36 is the factory's **numeric anomaly detector**: a **Python tool node in a Gas City pack** that **reads the
factory's telemetry / quality-metric streams and flags statistically unusual values**, emitting an
**anomaly signal** that opens the self-healing loop (README:253; AI-CONTEXT:327). It is the **first and
simplest piece of Principle 11** — "Observability → **anomaly** → diagnosis → fix → ship, without human
intervention" (README:248) — and v4 is explicit that it is built first, *before* the harder P11 pieces, "so
the substrate is proven" (README:466). Where C37 (clustering) and C38 (the Healer diagnosis agent) reason
about *which failures are alike* and *why*, C36 sits at the very front of that chain and answers only the
narrow numeric question: **"is this metric value abnormal?"** — and, when yes, **routes a signal downstream**.

C36 is **deliberately thin and almost entirely off-the-shelf**: the detection itself is **PyOD / Anomalib**
(BSD-2 / Apache-2.0), which v4 names as **"Mature generic"** numeric anomaly detection (AI-CONTEXT:327), and
**Prometheus alerting patterns** for threshold-style alarms (AI-CONTEXT:405). C36 introduces **no bespoke
anomaly algorithm**. The factory's *genuine* contribution — the only load-bearing custom surface — is the
**wiring**: (a) **which** metric streams are watched and how they are shaped into the numeric series these
detectors consume, and (b) **what an anomaly *means downstream*** — the contract by which a flagged anomaly
becomes a signal that opens the heal loop (a candidate `anomaly` record / event that C37/C38 pick up).

**Responsibilities (what C36 is the spec-of-record for):**
- **Read the telemetry / quality-metric series (I1).** Pull the numeric metric streams the detector scores —
  the per-run/per-session telemetry and quality metrics the factory records. The metric *substrate* is **CXDB
  trajectories landed by C24** (read via C21's retrieval/query seam, C21 I6/I2; spec/C21:81,103) plus any
  metric series already materialised by the observability tier. C36 owns *which series are watched and how
  they are reduced to the numeric vectors the detectors take* — not the storage.
- **Run off-the-shelf numeric anomaly detection (I2).** Score the series with **PyOD / Anomalib** (the
  v4-named "Mature generic" detectors, AI-CONTEXT:327) and/or **Prometheus-style threshold alerting**
  (AI-CONTEXT:405). C36 selects + configures the detector and feeds it the series; it **does not implement an
  estimator**. The output is an **anomaly verdict + score** per series/window.
- **Emit the anomaly signal (I3).** When a value is flagged, produce the **anomaly signal** that opens the
  heal loop: a typed `anomaly` record / event carrying *what* was anomalous (which metric/series, which
  run/trajectory), the *score/severity*, and the pointer back to the offending trajectory in C21. This signal
  is the **trigger** C37 (clustering) and C38 (diagnosis) consume — the one piece of wiring v4 leaves to the
  factory (README:248 "anomaly → diagnosis").
- **Be configured for the watched-metric set + thresholds (I4).** Which streams, which detector(s), what
  sensitivity/contamination/threshold — all **pack configuration**, not code (the bar: capability lives in
  PyOD/Anomalib/Prometheus; C36 supplies the wiring + config).
- **Run as a pack tool node (I5).** Packaged + invoked per the pack/tool-node ABI (C02/C17), as a **Python**
  tool-node binary in a Gas City pack (README:253 "Python tool node in Gas City pack").

**Explicitly NOT (boundaries):**
- **NOT a custom anomaly algorithm.** The detector is **PyOD / Anomalib / Prometheus** off-the-shelf
  (AI-CONTEXT:327, 405). C36 introduces **no bespoke statistical estimator, no novel detector, no hand-rolled
  scoring math** — per the bar, that capability already exists in the named stack and any reimplementation is
  DROPPED (§6, the-bar note). C36's custom surface is *selection + wiring + the downstream signal*, nothing more.
- **NOT clustering / "which failures are alike".** Embedding trajectories (sentence-transformers) and grouping
  similar failures (HDBSCAN) is **C37** (README:255; inventory line 49). C36 flags *individual* anomalous
  values; it does **not** group them. C36 *feeds* C37, it does not cluster.
- **NOT diagnosis / root-cause ("why").** LLM root-cause analysis over failures (the Healer, Tracker
  Diagnose/Audit/Doctor transfusion) is **C38** (README:256; inventory line 50). C36 says *that* something is
  abnormal, never *why*. The "why" is C38's, downstream of the anomaly signal.
- **NOT fix-task generation / loop-closure.** Turning a diagnosis into a `fix_task` bead that re-enters the
  build flow, and proving the fix worked (the termination/escalation contract), is **C39** (inventory line 51;
  README:257,259). C36 owns neither the fix nor the proof-of-fix; it only opens the loop.
- **NOT the LLM-trajectory anomaly composer.** v4 distinguishes **numeric** anomaly detection (PyOD/Anomalib,
  "Mature generic", **C36**) from **LLM-trajectory anomaly** ("None turnkey / DIY / **Compose on generic**",
  AI-CONTEXT:328). C36 is the **numeric** detector that the LLM-trajectory layer *composes on* — it is the
  "generic" base, not the composed semantic detector. The semantic/LLM-trajectory layer is a later P11 surface
  (a future-track item; it composes *on* C36, OQ-3), not C36's Sweep-1 scope.
- **NOT the telemetry store or the ingest bridge.** Trajectories live in **C21** (CXDB); the telemetry→CXDB
  **bridge** is **C24** (write-side). C36 is a **read-side consumer** — it reads metric series via C21 and does
  not store, ingest, or own the metric record's schema. (spec/C24:65 "C36 … read from C21, not from C24".)
- **NOT the metric *definition* for quality.** *What "quality" means* as a metric is a hard, separate problem
  (F4 "quality metric definition is itself a hard problem", F-MODE-COVERAGE:42); C36 detects anomalies in
  *whatever numeric quality/telemetry series the factory already emits*, it does **not** define the quality
  metric. (The satisfaction metric itself is **C33**; C36 may watch C33's output series but does not compute it.)
- **NOT the threshold/values decisions on drift.** Where v4 says "Healer monitors gate-relaxation /
  acceptance-threshold / classification-threshold drift … **surface to operator**" (F24/F7/F57), the *detection
  of drift* in those numeric series is C36's, but the **decision** about whether the drift is acceptable is a
  values question deferred to the operator / the Healer-governance surface (F57 "can detect drift, cannot
  decide"). C36 detects + surfaces; it does not adjudicate.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (metric substrate, landed) | **C24** Telemetry → CXDB bridge | C24 is the write-side bridge that **lands** the factory's telemetry/trajectories into CXDB; C36's metric streams exist *because C24 delivered them*. Inventory C36 `depends on C24`. **But C36 reads from C21, not C24** (spec/C24:65) — the C24 edge is a *data-provenance* dependency (the stream is there), the read happens through C21. *(Boundary nuance → OQ-1.)* |
| Upstream (read seam) | **C21** CXDB trajectory store | The content-addressed store C36 **reads** metric series from, via replay/retrieval + HTTP/JSON query (C21 I6/I2; spec/C21:103 "C36/C37/C38/C49 consume"). C21 fails *open* on outage (spec/C21 §6); C36 inherits that posture (§6, G33). Inventory C36 `depends on C21`. |
| External (detector engines) | **PyOD / Anomalib** (`github.com/yzhao062/pyod` BSD-2; `github.com/openvinotoolkit/anomalib` Apache-2.0) | The v4-named "Mature generic" numeric anomaly detectors C36 wraps (AI-CONTEXT:327; README:253; AI-CONTEXT:647–648). Engine reuse — **not** custom code. |
| External (alerting pattern) | **Prometheus alerting patterns** | Threshold/rate-style alarms v4 names for the same layer (AI-CONTEXT:405). Pattern reuse for simple threshold alarms alongside the PyOD/Anomalib statistical detectors. |
| Downstream (clustering) | **C37** Trajectory clustering | Consumes C36's anomaly signal — embeds + clusters the flagged failures (README:255; inventory line 49). C37's inventory `depends on C21`; the **anomaly→cluster trigger seam is C36's signal (I3)**. |
| Downstream (diagnosis) | **C38** Diagnosis agent (Healer) | The LLM root-cause analysis the anomaly signal ultimately drives (README:248 "anomaly → diagnosis"; inventory line 50). C38 reads clustered failures (via C37), so C36 reaches C38 **through** C37 in the canonical chain. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C36 is a **Python** tool node in a Gas City pack (README:253), invoked via the tool-node protocol. *(Related interface, not a dependency edge; mirrors how C24/C33 name C02/C17.)* |

**Position in the system.** C36 is **Batch-4** (component-inventory line 113), built in **Phase 3b** as the
**first** P11 component — "build the simplest first (anomaly detection); save the diagnosis agent for after the
substrate is proven" (README:466; AI-CONTEXT:459–461). It is **not foundational** (inventory C36: Foundational?
= no) — nothing upstream contracts against it; it is a leaf reader that opens a loop. It is, however, the
**front door of the self-healing loop**: the anomaly signal it emits is the trigger the rest of P11 (C37→C38→
C39) is wired to. It is **feature-flag-gated** with the self-healing pack (it exists only when P11 is enabled,
and only once the CXDB substrate + the C24 bridge are standing — README:397 "CXDB substrate ready for P11
anomaly clustering").

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete detector signatures / the metric-series schema / the
`anomaly`-signal record shape / the exact watched-metric set defer to sweep 2 (and the trajectory-read wire to
C21, the detector API to PyOD/Anomalib).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Telemetry / quality-metric read** | inbound (read) | Read the numeric metric series C36 scores — per-run/per-session telemetry + quality metrics — from **CXDB trajectories (via C21 I6/I2)** (and any already-materialised metric series). C36 owns the reduction of trajectories/telemetry into the numeric vectors the detectors take; the **store/retrieval** is C21's, the **landing** is C24's. | C36 (this); **C21** (read seam), **C24** (provenance) |
| I2 | **Numeric anomaly scoring** | internal | Score the series with **PyOD / Anomalib** (AI-CONTEXT:327) and/or **Prometheus-style threshold alerting** (AI-CONTEXT:405); produce an **anomaly verdict + score** per series/window. Engine = the v4-named detectors; **no custom estimator** (the bar). | C36 (this); **PyOD/Anomalib** (engine) |
| I3 | **Anomaly signal (loop trigger)** | outbound (data/event) | When a value is flagged, emit the **anomaly signal** that opens the heal loop: *what* (metric/series + run/trajectory pointer into C21), *score/severity*, *when*. The **trigger** C37/C38 consume (README:248). This is C36's load-bearing custom surface — the wiring of detection → downstream. | C36 (this); **C37/C38** (consumers) |
| I4 | **Watched-metric + detector config** | input (config) | The set of watched metric streams, the chosen detector(s), and the sensitivity/contamination/threshold params — **pack TOML**, not code. | C02/C03 (model); C36 (binding) |
| I5 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as a **Python** Gas City tool node (C02/C17 ABI); configured via pack TOML; operated with the self-healing pack in Phase 3b (README:253,459). | C02/C17 (ABI); C36 (config) |

**Invariants C36 must uphold:**
- **INV-1 (off-the-shelf detection — the bar).** The anomaly scoring is **PyOD / Anomalib / Prometheus**
  (AI-CONTEXT:327,405). C36 contains **no bespoke anomaly algorithm**; the custom surface is *only* metric
  selection + the downstream signal. This is the load-bearing "keep-minimal" property (§6).
- **INV-2 (detect-only — no fix, no judgement of cause).** C36 emits *that* a value is anomalous; it renders
  **no diagnosis (C38), no fix (C39), and no values-decision** on drift (F57 "cannot decide"). It is a pure
  detector + router.
- **INV-3 (signal is actionable — carries provenance).** Every anomaly signal carries enough to **open the
  loop**: the metric/series identity, the **pointer back to the offending trajectory in C21**, and a
  score/severity — so C37/C38 can pick up the thread without re-deriving it. An anomaly that cannot be traced
  to a trajectory is of no use to the loop.
- **INV-4 (read-side, owns no source-of-truth).** C36 **reads** metric series and **emits** signals; the
  metrics live in C21 (landed by C24), the loop state lives on beads/CXDB downstream. C36 holds **no durable
  store of its own** beyond detector state/baselines (re-derivable from the series).
- **INV-5 (every guard points at a scenario — F52 discipline).** Per the F52 "more controller patches" caution
  (F-MODE-COVERAGE:100,170), **every detector C36 runs must point at a specific failure it catches, with a
  measurable false-positive rate** — no anomaly rule without a falsifying scenario. This is the explicit guard
  against C36 becoming discipline-without-purpose (the Tempting-Wrong-Hybrid trap the docs warn P11 is most
  prone to).

## 4. Data model / state

C36 **owns the watched-metric wiring + the anomaly-signal contract**, not durable source-of-truth data. The
**trajectory/metric series** is C21's (landed by C24); the **downstream loop state** is C37/C38/C39's. State
C36 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Anomaly signal** | The emitted trigger: metric/series id + run/trajectory pointer (into C21) + score/severity + timestamp. The component's *output*, consumed by C37/C38 (I3). | Emitted as a typed `anomaly` record / event (a candidate C20 bead type or an event on C23 — **OQ-2**); re-derivable by re-scoring the same series. | C36 (shape); **C37/C38** (consumers); **C20** (iff bead-typed) |
| **Detector config** | Watched metric set, chosen detector(s) (PyOD/Anomalib/Prometheus), sensitivity/contamination/threshold params. | Pack TOML (C02/C03 model). | C02/C03 (model); C36 (binding) |
| **Detector state / baseline** | Fitted model / rolling baseline the detector scores against (PyOD model, Anomalib model, Prometheus rule window). Owned by the **detector engine**, not custom; re-derivable from the metric series. | Detector-managed (in-pack); re-fittable from C21. | **PyOD/Anomalib** (engine); C36 (lifecycle) |
| **Metric series (read-only input)** | The telemetry/quality numeric series C36 scores. **Owned by C21** (landed by C24), read-only to C36. | CXDB (C21). | **C21** (store), **C24** (landing) |

> [FAITHFUL-FILL] v4 specifies the *capability* ("numeric anomaly detection, PyOD/Anomalib", AI-CONTEXT:327;
> "detects unusual patterns", README:253) but not C36's persisted state. The minimal faithful set is **none
> that is source-of-truth**: the detector state is the engine's (re-fittable from the series), and the anomaly
> signal is a derived record re-computable by re-scoring. So C36 holds no independent store. The exact
> **metric-series schema**, the **`anomaly`-signal record shape**, the **canonical watched-metric set**, and
> **whether the signal is a C20 bead type or a C23 event** are **sweep-2** (frozen with C37/C38, the principal
> consumers, and C20/C23 as the carriers — OQ-2).

**Consistency / lifecycle.** C36 stands up in **Phase 3b** with the self-healing pack (README:459), once the
**CXDB substrate + the C24 bridge** are standing (README:397). It owns no durable truth: the **metric series**
survive in C21, the **loop state** downstream — so a re-run of C36 over the same series re-derives the same
anomaly verdicts (modulo detector-baseline state, which is itself re-fittable). C36 is therefore a
**stateless-by-design read-side detector + router** — exactly what "wrap a mature detector + emit a signal"
implies, which is why the bar keeps it thin (no store, no custom estimator; §6).

## 5. Behavior

**Stand up (Phase 3b).** The self-healing pack is installed; the Python tool node is configured with the
watched-metric set, the chosen detector(s) and their sensitivity/threshold params, and the anomaly-signal
sink (C37/C38). It is wired downstream of the metric substrate (C21, landed by C24) and upstream of C37/C38.

**Detect path (steady state).**
1. **Read metric series (I1):** pull the watched telemetry/quality series from C21 (trajectory retrieval /
   query, C21 I6/I2), reducing them to the numeric vectors the detector takes.
2. **Score (I2):** run the configured **PyOD / Anomalib** detector (and/or Prometheus-style threshold rule)
   over the series/window; obtain an **anomaly verdict + score** per series. No bespoke math (INV-1); no
   diagnosis (INV-2).
3. **Decide flagged-or-not:** apply the configured sensitivity/threshold; a value above it is *flagged*. Each
   flag must trace to a specific failure the detector is configured to catch (INV-5, F52 discipline).
4. **Emit anomaly signal (I3):** for each flag, emit the typed `anomaly` signal — metric/series id + the
   **trajectory pointer into C21** + score/severity + timestamp (INV-3) — to the loop sink (C37/C38).
5. **No flag → nothing downstream:** a clean window opens no loop (the loop is event-driven on anomalies, not
   a constant drip).

**Re-computation.** Because C36 owns no source-of-truth (INV-4), the same series re-scored yields the same
verdicts (the detector baseline is re-fittable from C21). There is no checkpoint to recover and nothing
load-bearing to lose on restart — a restarted C36 re-reads the series and resumes detection.

> The exact detector selection per metric class, the scoring signatures, the `anomaly`-signal record schema,
> the watched-metric reduction rules, and whether windows are batch-scored or streamed are **sweep-2+** (frozen
> with C37/C38 + C20/C23). Whether the LLM-trajectory/semantic anomaly layer *composes on* C36 here or is a
> separate later component is a sweep-2 boundary (OQ-3). C36 runs **no** LLM call and builds **no** custom
> estimator.

## 6. Failure modes & handling

C36 carries the **G33** gap assigned at this component (shared with its deps C24/C21).

**G33 (major) — partial/cascading failure of the OSS stack; here: data durability/availability of the
*metric stream* C36 reads. NOTED + DEFERRED to the deps that own it (C24/C21), with C36's own fail-open
posture stated.** G33 asks "what happens when CXDB is down mid-run?" and, for the broader stack, when a
Python tool node OOMs (F-MODE-COVERAGE/ambiguities G33). For C36 the faithful handling is a **read-side
inheritance**, not a new mechanism:
- **The metric stream's durability is *already owned upstream*, not by C36.** **C24** discharges the
  durability obligation (retain-in-inbox + idempotent re-post — spec/C24 §6 AC-6/AC-7), and **C21** fails
  *open* on outage (spec/C21 §6 reading (a), AC-7). C36 is a **downstream consumer** of that resolved
  contract; it neither buffers the stream nor re-implements durability. Inventing a C36-side durable queue
  would duplicate C24's inbox-spool and exceed faithful scope (the bar — DROP).
- **C36's own posture: fail-open / skip-window, re-derive on recovery.** If C21 is unreachable (or the metric
  series is incomplete because C24 is mid-outage), C36 **skips the unavailable window and re-scores it when
  the data lands** (the metric series is re-readable from C21, INV-4; the loop is not lost, only delayed). A
  C36 OOM/crash (the F-MODE-COVERAGE G33 "Python tool node OOMs" case) is **safe by construction**: C36 owns
  no source-of-truth, so a restart re-reads the series and resumes — *no anomaly is permanently lost as long
  as the underlying series survives in C21* (which is C24/C21's guarantee, within their inbox/disk bound).
- **The honest residual (→ OQ-1).** C36's anomaly coverage is therefore **only as complete as the metric
  stream C24/C21 actually retained**: if a CXDB outage exceeds C24's inbox capacity (spec/C24 OQ-4, the disk
  bound), the lost-trajectory window is also un-scorable by C36 — a *known, inherited* limitation, not a new
  C36 failure. v4 prescribes no in-store HA, so C36 records this as **inherited from G33 at C24/C21** and
  **defers** any stronger durability to those owners + the integrator. *[FAITHFUL-FILL]: v4 places G33's
  durability seam at the bridge/store; C36 as a reader inherits it — fail-open/skip-and-re-derive is the
  minimal honest reader posture, mirroring C21's own reading (a).]*

**Other failure cases.**
- **Detector false positive (the F52 trap).** A spurious anomaly opens the loop needlessly. Mitigation is
  INV-5 + the F52 discipline: **every detector points at a specific failure it catches, with a measured
  false-positive rate, reviewed periodically** (F-MODE-COVERAGE:100,170). Sensitivity/threshold is tunable
  config (I4). The *quantified* recurrence/false-positive policy is sweep-2 (OQ-2). *[FAITHFUL-FILL]: the F52
  caution is v4-stated and explicitly aimed at the P11 self-healing surface C36 sits at — surfacing FP rate as
  a first-class signal is the minimal faithful guard.]*
- **Empty / too-short series (cold start).** A metric series with too few points to fit a detector → emit
  **no** anomaly (do not fabricate one from noise); surface "insufficient data" rather than a false flag.
  *[FAITHFUL-FILL]: minimal honest choice; mirrors the small-n discipline in sibling metric components (C33).]*
- **Malformed / missing metric value** → exclude from the scored series + record the exclusion; one bad value
  must not poison the detector. *[FAITHFUL-FILL]: fail-open-per-value, mirrors C24's quarantine-and-continue
  and C33's per-record exclusion posture.]*
- **Quality-metric definition is itself unsolved (F4).** C36 detects anomalies in *whatever* quality series
  the factory emits, but F4 warns "quality metric definition is itself a hard problem" (F-MODE-COVERAGE:42) —
  so C36's quality-anomaly coverage is **Partial by construction** (it cannot detect drift in a quality
  dimension the factory does not yet measure). C36 surfaces this boundary; defining the quality metric is **not
  C36's** (boundary, §1).

> F-mode applicability is owned by **C57** (coverage map). C36 underwrites the **numeric-detection half** of
> several P11 modes — **F22** (zombie agents: "anomaly detection on session liveness (PyOD on telemetry)",
> F-MODE-COVERAGE:44 — the mode most directly named to C36), **F4** (code-quality teardown: anomaly detection
> on quality metrics, Partial per F4), **F8** (stale-knowledge: anomaly detection on knowledge-store freshness,
> F-MODE-COVERAGE:85), and the **drift-detection** inputs to **F24/F40/F57/F7** (gate-relaxation / shipping-rate
> / classification-threshold / acceptance-threshold drift — C36 *detects* the numeric drift; the *Healer
> response + the values-decision* are C38/operator, so these stay **Partial**, F-MODE-COVERAGE:43,46–48). It
> also feeds the **F54** objective-drift detector ("Healer anomaly detection on objective shift", Partial,
> F-MODE-COVERAGE:93). C36 is the *detector*, not the *resolver*, of all of these, and defers the canonical
> F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C36 is held to *only* the P11-tied wiring (which metrics,
what triggers the downstream signal) plus selection/config of the v4-named detectors. **Dropped / refused as
non-principle or already-in-the-stack:** (1) **any custom anomaly algorithm** — statistical estimators,
outlier math, threshold detectors are **PyOD / Anomalib / Prometheus** off-the-shelf (AI-CONTEXT:327,405); a
hand-rolled detector is the textbook DROP for this component; (2) **a C36-side durable queue / buffer** for the
metric stream — durability is C24's inbox-spool + C21's fail-open (G33 lives at the bridge/store), so C36
duplicating it is DROPPED (§6); (3) **clustering / diagnosis / fix-generation** — those are C37 / C38 / C39 and
are explicitly later, harder P11 pieces (README:466); (4) **the LLM-trajectory / semantic anomaly composer** —
v4 marks it "None turnkey / Compose on generic" (AI-CONTEXT:328); C36 is the *generic numeric base* it composes
*on*, not the composed layer (OQ-3). What is **kept**: the **watched-metric wiring** and the **anomaly-signal
contract** (the trigger that opens the heal loop, README:248) — the one genuinely load-bearing custom surface,
plus the detector selection/config the off-the-shelf engines need.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C36 reads **numeric metric series** (telemetry/quality numbers), far less sensitive than the
  raw request/response bodies on C24's path; it inherits C21's read access posture and adds no new exposure.
  It performs **no model call** (unlike C38), so no judge/LLM-provider credential is needed. The anomaly
  signal it emits carries trajectory pointers, not payloads.
- **Cost.** A Python tool node running PyOD/Anomalib over metric series — **modest compute, no model tokens, no
  managed store**. Anomalib (PyTorch) is the heavier of the two; for simple numeric streams the lightweight
  PyOD detectors (and Prometheus-style threshold rules) are the cheaper default, with Anomalib reserved for
  cases that need it (a sweep-2 selection, OQ-2). C36 itself spends **no** LLM tokens; the heal-loop token cost
  is C38's. *(v4 gives no C36 cost model — G32 thread; the embedding cost in the loop is C37's, AI-CONTEXT/G32.)*
- **Scale.** Detection cost is roughly linear in the watched-series volume; the honest scale note is that very
  high metric volume (L5) may want **streamed/windowed** scoring rather than full-history re-scoring — a
  sweep-2/perf concern (OQ-2), not a Sweep-1 design force. No bespoke scaling machinery is warranted (the bar);
  PyOD/Anomalib handle the detection scale.
- **Observability.** C36 *is* an observability component — its anomaly signal is the headline P11 trigger. Its
  own health (series scored, flags emitted, false-positive rate per detector — the F52-mandated number, INV-5,
  exclusion counts for malformed values) is worth emitting as events for auditability. C36 is both a *reader*
  of observability and an *emitter* of the loop-opening signal.
- **Ops.** Pack-delivered **Python** tool node operated with the self-healing pack in Phase 3b (README:253,459).
  **Pin the PyOD/Anomalib versions** so the detection contract is reproducible (inherits the eval/P11-tier
  version-pin discipline; mirrors C21/C24). Detector retraining/baseline-refresh cadence is a sweep-2 ops
  concern.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (detects anomalies — I1/I2):** given a metric series containing a known anomalous value, C36 flags
   it; given a clean series, it flags nothing (README:253; AI-CONTEXT:327).
2. **AC-2 (off-the-shelf detector — INV-1, the bar):** the detection is **PyOD / Anomalib** (and/or
   Prometheus-style threshold rules); **no bespoke anomaly algorithm** is present (AI-CONTEXT:327,405).
   *(Verifiable: the scoring path is a configured call into the named engine, not custom estimator code.)*
3. **AC-3 (emits an actionable anomaly signal — I3/INV-3):** a flag produces a typed `anomaly` signal carrying
   the metric/series id, the **trajectory pointer into C21**, and a score/severity — consumable by C37/C38
   (README:248).
4. **AC-4 (detect-only — INV-2):** C36 renders **no** diagnosis, **no** fix, and **no** values-decision on
   drift; it only detects + routes (F57 "cannot decide"). *(Verifiable: C36 runs with no LLM provider and no
   fix-task writer configured.)*
5. **AC-5 (read-side / no source-of-truth — INV-4):** C36 reads the series from C21 and owns no durable store;
   re-scoring the same series re-derives the same verdicts (detector baseline re-fittable from C21).
6. **AC-6 (fail-open / skip-and-re-derive — addresses G33):** with C21 **down** (or the series incomplete
   because C24 is mid-outage), C36 **skips the unavailable window without crashing** and **re-scores it when
   the data lands**; a C36 restart loses no anomaly that the underlying series (in C21) still holds.
7. **AC-7 (false-positive discipline — INV-5, F52):** every configured detector points at a specific failure
   it catches and **its false-positive rate is measurable/surfaced**; no anomaly rule without a falsifying
   scenario (F-MODE-COVERAGE:100,170).
8. **AC-8 (cold-start / bad-value honesty):** a too-short series or a malformed value yields **no fabricated
   anomaly** — "insufficient data" / value-excluded-with-count, never a false flag from noise.
9. **AC-9 (simplest-first scope — boundary):** C36 does **not** cluster (C37), diagnose (C38), generate
   fix-tasks (C39), or run the LLM-trajectory/semantic anomaly layer (the "compose on generic" surface,
   AI-CONTEXT:328) — it is the first/simplest numeric P11 piece (README:466).

**Test strategy.** An **anomaly-detection pack** that seeds synthetic metric series in C21 (clean series,
known-anomalous series, drift series, cold-start/too-short series, malformed values) and drives AC-1…AC-9 — in
particular that a known anomaly is **flagged with a traceable signal** (AC-1/AC-3), that the detector is the
**off-the-shelf engine** (AC-2), that detection is **fail-open over a C21 outage and re-derives on recovery**
(AC-6, the G33 de-risker), and that **false-positive rate is surfaced per detector** (AC-7, the F52 guard). This
suite is built **after** the C21 conformance + C24 integration packs pass (C36 reads what they land), and
**must pass before C37/C38 build on the anomaly signal**, since they assume C36's signal is the canonical heal-loop
trigger.

## 9. Open questions

- **OQ-1 (→ review-log, top): the metric-stream read seam (C24/C21 boundary) + inherited G33 ceiling.** The
  inventory lists C36's deps as **C24 *and* C21**, but C24's own spec says C36 reads from **C21, not C24**
  (spec/C24:65). Confirm the faithful reading: C24 is the *provenance* dep (it lands the stream), C36 *reads*
  via C21 — and confirm C36's anomaly coverage is bounded by C24/C21's retained window (the C24 inbox/disk
  bound, spec/C24 OQ-4) with **no C36-side durability added**. Also confirm **which metric series** are the
  Sweep-1 watched set (CXDB trajectory-derived telemetry vs the OTLP/metrics path on C25/C26 — v4's metric
  sources are split, and the inventory points C36 at the CXDB/C24 side).
- **OQ-2 (→ review-log): detector selection + signal carrier + thresholds.** Which detector per metric class
  (lightweight PyOD vs Anomalib/PyTorch vs Prometheus threshold rule); the canonical **`anomaly`-signal record
  shape** and **whether it is a C20 bead type or a C23 event** (the carrier to C37/C38); the
  sensitivity/contamination/threshold defaults; the **quantified false-positive / recurrence policy** (F52);
  and batch-vs-streamed scoring at L5 volume. Freeze at sweep 2 with C37/C38 (consumers) + C20/C23 (carriers).
- **OQ-3 (→ review-log): the LLM-trajectory / semantic anomaly boundary.** v4 marks LLM-trajectory anomaly
  "None turnkey / **Compose on generic**" (AI-CONTEXT:328). Confirm C36 is the **numeric generic base** only,
  and that the semantic/LLM-trajectory anomaly layer is a **separate later P11 surface that composes on C36**
  (not a Sweep-1 C36 responsibility). This sets whether "compose on generic" is a sweep-2 extension to C36 or a
  distinct component.
- **OQ-4 (→ review-log): F4 quality-metric scope.** C36 detects anomalies in the quality series the factory
  emits, but F4 flags the *definition* of a quality metric as unsolved (F-MODE-COVERAGE:42). Confirm **which
  quality series exist** for C36 to watch at Phase 3b (and that defining new quality metrics is out of C36's
  scope), so F4 coverage is honestly scoped as Partial.
