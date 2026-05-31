# C46 — Meta-Metric Stream  (Spec, canonical track)

> Source: README §"Principle 12 — Self-optimization" (line 263 "The system **measures its own
> meta-performance and improves it over time**"; line 269 table row "**Meta-metric definition** | What
> 'better' means | **Custom: cost-per-satisfaction, time-to-threshold, judge false-positive rate** | n/a (your
> work) | **Configuration**"; line 270 "**Meta-metric tracking** | Records meta-metrics over time | **MLflow,
> Aim, Weights & Biases (free tier)** | Apache 2.0 / Apache 2.0 / freemium | **Gas City pack**"; line 470
> "Phase 3d — P12 … factory builds the **meta-metric pack**"; line 278 "P12 … **Build last, after Layers 1-5
> are solid**"); AI-CONTEXT §"Layer 6 — self-optimization (P12)" (line 353 "Meta-metric tracking | **MLflow,
> Aim, Weights & Biases** | … | **Mature**"; line 378 "MLflow | **L6 meta-metric tracking + L6 experiment
> registry**"; line 516 "**Self-optimization meta-metrics**: which specifically? **Values question — needs
> operator input**"); component-inventory C46 row (line 58 "Records cost-per-satisfaction, time-to-threshold,
> judge-FP-rate over time; **needs a defined cost model**"; maps A65/A66/A72b/A72d/B12/B-cost; depends **C33,
> C24**; gaps **G09, G32**; foundational no) + Batch-5 note (line 115); spec/C33 §1/§6 (the satisfaction
> *distribution* C46 divides cost by — the satisfaction *term*; C33 is threshold-free, the cutline lives at the
> decision sites); spec/C24 §1 (the telemetry→CXDB bridge — where the per-run cost signal lands); spec/C29 §1
> (line 19 "NOT the cost *meter* (C46 … owns cost-per-satisfaction measurement)", §6 "the cost-per-satisfaction
> model is **C46's**", §9 "[G32] Cost model deferred to C46"); spec/C37 §6 (cost-per-embedding "**surfaced to
> C46** … not modelled in C37", G32 reading (b)); spec/C55 §6 (experiment-grid cost "quantify with **C46** …
> cost model lives in **C46/G32**"); F-MODE-COVERAGE F47 (line 63/103 "**Multi-metric mandatory** … P12 always
> tracks **aggregate of multiple metrics**; no single visible target"), F60 (line 64/162 "**Aggregate-rate
> tracking** in meta-metric set (1 − (1−p)ⁿ explicit)"), F40 (line 47 "shipping rate vs project-start rate");
> ambiguities-and-gaps G09, G32; review-log D-6 (canonical track), D-15 (satisfaction holistic — C46 reads
> C33's distribution), D-19 (significance testing → C48, mirrors C33's significance→C48 boundary); C29:G32 /
> C28:OQ-2 / C32:OQ3 / C37:OQ-3 / C55:OQ-3 (the repo-wide deferral of the cost model **to C46**).
> Inventory ID: C46   Kind: data-flow   Status: sweep-1

## 1. Purpose & responsibility

C46 is the factory's **meta-metric stream**: the **data-flow that records the factory's own meta-performance
over time** — **cost-per-satisfaction, time-to-threshold, and judge-false-positive-rate** as time-series
(README:263/269). It is the component that operationalises **Principle 12 — self-optimization**: where C33
measures *one spec's* satisfaction, C46 measures *the factory's* performance **as a trend across runs**, so the
self-optimization loop (C47 variant-ID → C48 A/B → C50 promotion) has a measurable "**is the factory getting
better?**" signal to optimise against. It is the **meta-metric stream that makes the factory's own performance
measurable over time** — the load-bearing P12 instrument.

C46 has **two genuine deliverables**, both of which v4 marks as *custom work / configuration*, not engine:
1. **The cost MODEL definition (G32 — C46's core deliverable).** v4 says cost is "**essentially unmodeled**"
   (G32) yet makes "cost-per-satisfaction" P12's headline meta-metric (README:269). C46 is the **spec-of-record
   for what "cost" *means*** as a measurable unit: the **per-run cost vector** (tokens / dollars / wall-clock
   time) attributable to a unit of work, and how it is **divided by the satisfaction term (C33)** to yield
   cost-per-satisfaction. This is the "Meta-metric **definition** … **Custom … n/a (your work)** …
   **Configuration**" cell of README:269 — a *definition/config* artifact, **not** a metering engine.
2. **The meta-metric streams themselves (G09 consumer).** The three named meta-metrics as **time-series over
   the factory's runs**: cost-per-satisfaction (cost ÷ C33-satisfaction), time-to-threshold (elapsed time/runs
   for satisfaction to cross a supplied cutline), judge-FP-rate (rate at which the judge passes work later
   found bad). C46 **defines** these and **records** them; it stores them via the v4-named time-series tooling
   (**MLflow / Aim / W&B**, README:270), **not** a custom metrics engine.

C46 is **deliberately thin on engine, dense on definition**. The *storage/tracking* is v4's named **MLflow (or
Aim / W&B)** Gas City pack (README:270; AI-CONTEXT:353 "Mature") — an off-the-shelf experiment-tracking /
time-series store. C46's *custom* surface is **only the definitions** v4 explicitly calls "your work":
**what each meta-metric is, the cost model, and the cross-stack glue** that pulls the cost signal (C24/telemetry)
and the satisfaction term (C33) together into one recorded series. It computes **no statistical significance**
(that is C48, D-19) and makes **no promotion decision** (that is C50).

**Responsibilities (what C46 is the spec-of-record for):**
- **Define the cost model (G32, I1 — core deliverable).** Fix what **one unit of work's cost** is: the
  **per-run cost vector {tokens, dollars, wall-clock time}** (the three cost dimensions v4 gestures at across
  G32/G13 — "no token-budget math", "$200/month Max", second-family-judge tokens, embedding cost), how a
  run's cost is **attributed** (which trajectory / spec-revision a cost belongs to), and the **reduction** that
  turns the vector into cost-per-satisfaction (cost ÷ the C33 satisfaction term). C46 **names** the dimensions
  and the division; the *raw* cost numbers are read, not synthesised (see I2).
- **Define + record cost-per-satisfaction over time (I3).** The headline P12 series: per-run/per-spec-revision
  **cost (I1 model) ÷ satisfaction (C33 distribution term)**, recorded as a time-series point (README:269).
- **Define + record time-to-threshold over time (I3).** Elapsed time (or run-count) for a spec-revision's
  satisfaction (C33) to **cross a supplied cutline** — recorded per spec-revision as the factory iterates
  (README:269; "time-to-threshold"). C46 **consumes** a cutline; it does not own/decide it (G09 — the cutline
  is the decision sites', C50/C53/C39 — §6).
- **Define + record judge-false-positive-rate over time (I3).** The rate at which the judge (C32) scored work
  *satisfactory* that a later signal (loop-closure failure C39, override C35, human review) found **not**
  satisfactory — recorded as a trend (README:269; the F48 same-family-judge-bias monitor, review-log C32:OQ1
  "judge-FP via C46?"). C46 **records** the rate from labelled outcomes; it does **not** re-judge.
- **Store/track the streams via off-the-shelf time-series tooling (I4).** Persist the series through the
  v4-named **MLflow / Aim / W&B** pack (README:270; AI-CONTEXT:353/378) — a mature experiment-tracking store —
  **not** a bespoke metrics database. C46 owns the *schema of what is logged*, not the storage engine.
- **Surface the streams to the self-optimization tier (I5).** Expose the recorded meta-metrics (and their
  trend) for **C47** (which variants to try), **C48** (which series to compare for significance — D-19), and
  **C50** (the multi-metric promotion gate — F47). C46 produces the *measured* series; consumers decide/act.
- **Enforce multi-metric tracking (F47/F60 — invariant, not a feature).** Always record the **aggregate of
  multiple metrics**, never a single visible target, so Goodhart has no single number to game (F47
  "Multi-metric mandatory"); surface **aggregate-rate** awareness (F60, 1−(1−p)ⁿ) rather than single-cycle.

**Explicitly NOT (boundaries):**
- **NOT the satisfaction metric.** The satisfaction *distribution* (one spec's outcome variety) is **C33**
  (spec/C33 §1). C46 **consumes C33's distribution as the satisfaction *term*** it divides cost by; it never
  computes satisfaction, never invokes the judge, never reduces judge scores. Per **D-15**, the satisfaction
  C46 reads is **holistic** (C33 over C08's free-form DoD) — so C46's meta-metrics are **factory-level**, not
  per-criterion, at Sweep-1 (per-criterion meta-metric diagnosis is the FE-5/Sweep-2 extension, §6).
- **NOT the cost *meter* / the thing that incurs cost.** C46 **models and records** cost; it does **not**
  *spend* tokens or *route* models. Model-routing cost-awareness is **C29** (which carries a `cost_tier`, D-10,
  but explicitly defers the cost-per-satisfaction *model* to C46 — spec/C29 §1/§6/§9). The judge/coder/embed
  tokens are C32/C28/C37's spend; C46 only **reads** what they cost (I2).
- **NOT the source of the raw cost/usage signal.** The per-run usage (tokens, latency) lands via the
  **telemetry path** — Claude Code OTLP/usage + the **C24 telemetry→CXDB bridge** (inventory C46 `depends on
  C24`; spec/C24 §1). C46 **reads** the recorded usage; it does not capture or emit telemetry (that is
  C25/C26/C24). *(Dollar cost is a derived function of tokens × the model's price, not a separately metered
  feed — see I1/G32.)*
- **NOT the statistical-comparison engine.** Whether a meta-metric *moved significantly* between variants is
  **C48** (scipy/Evidently — README:275; **D-19**, mirroring C33's identical significance→C48 boundary). C46
  records the series and may show a raw trend; it runs **no** significance test, CI, or hypothesis test. (This
  is the same bar C33 holds: distributions/series here, significance at C48.)
- **NOT the promotion gate / the "is the variant better" decision.** The multi-metric, statistical gate that
  promotes a variant to default is **C50** (README:276; guards Goodhart). C46 supplies the *metrics* C50 reads;
  it neither decides nor promotes. (Parallels C33's "NOT the threshold/gate" boundary.)
- **NOT the variant identifier or the A/B router.** What to experiment with is **C47** (DSPy/Optuna); routing
  traffic between variants is **C48** (Unleash/bandit). C46 measures the *performance* those variants produce;
  it proposes and routes nothing.
- **NOT the satisfaction *threshold* owner (G09).** "Time-to-threshold" needs a cutline, but the cutline value
  and ownership are **deferred** exactly as in C33: the cutline lives at the **decision sites** (C50/C53/C39)
  and its *value* is operator/integrator policy v4 does not fix (§6, G09). C46 **consumes** a supplied cutline
  to compute time-to-threshold; it does not decide it.
- **NOT a custom metrics/time-series engine.** Storage is the v4-named **MLflow/Aim/W&B** pack (README:270).
  C46 introduces **no** bespoke time-series database, dashboarding stack, or metrics query engine — the
  prometheus/time-series + experiment-tracking capability already exists (the bar, §6).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (satisfaction term) | **C33** Satisfaction-metric aggregator | Produces the **satisfaction distribution** C46 divides cost by and watches for time-to-threshold. C46 reads C33's *holistic* distribution (D-15). Inventory C46 `depends on C33`. C46 is the principal consumer C33's distribution-record schema is frozen with (spec/C33 §4). |
| Upstream (cost/usage signal) | **C24** Telemetry→CXDB bridge | The seam where per-run usage telemetry (tokens, latency, conversation bodies) lands in CXDB; C46 **reads** recorded usage to compute the cost vector (I2). Inventory C46 `depends on C24`. |
| Cost-signal corroborator | **C29** Model-floor/stylesheet | Carries each model's `cost_tier` (D-10); C29 is cost-*aware at routing*, C46 is the cost-*meter over time*. C29 explicitly defers the cost-per-satisfaction model to C46 (spec/C29 §1/§6). *(Related interface — the price/tier reference — not a C46 dependency edge; deps are C33/C24.)* |
| Tracking/storage engine | **MLflow / Aim / W&B** (pack-wrapped) | The mature, "your work = Gas City pack" experiment-tracking / time-series store C46 logs the streams to (README:270; AI-CONTEXT:353/378). Engine reuse, **not** a custom metrics DB. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction; config via **C03** | C46 is the **meta-metric pack** (README:470) — its *definitions* are **Configuration** (README:269), surfaced/run via the tool-node + config model. *(Related interface, mirrors how C33/C24 name C02/C17/C03.)* |
| Downstream (variant ID) | **C47** Variant identification | Reads the meta-metric trend to decide what is worth experimenting with. Inventory C47 `depends on C46`. |
| Downstream (significance) | **C48** A/B routing & statistical comparison | Reads C46's series and runs the significance test C46 withholds (D-19). Inventory C48 `depends on C46`. |
| Downstream (promotion gate) | **C50** Promotion gate | Reads the **multiple** meta-metrics C46 records to make the multi-metric, Goodhart-guarded promotion decision (F47). C50 → C48 → C46 chain. |

**Position in the system.** C46 is **Batch-5** (component-inventory line 115), the **self-optimization
frontier built last** ("Build last, after Layers 1-5 are solid", README:278/470). It is **not foundational**
(inventory C46: Foundational? = no) and is **feature-flag-gated** with the self-optimization pack (it exists
only when P12 is enabled, C03). But it is the **load-bearing instrument of P12**: C47/C48/C50 all contract
against "the meta-metric that says whether the factory improved", and C46 is **the cost-quantification home** —
the component every other spec routes the cost model to (C29:G32, C28:OQ-2, C32:OQ3, C37:OQ-3, C38:OQ5,
C55:OQ-3; review-log C29:G32 "cost-per-satisfaction model deferred to C46"). C46 also feeds the **F47/F60**
Goodhart/compounding-error guards by *construction* (multi-metric, aggregate-rate).

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; the concrete cost-vector schema / per-metric record shape / the
exact statistic and tag set defer to sweep 2 (frozen with C33's distribution-record and C48's compare contract).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Cost-model definition (G32)** | definition/config | The spec-of-record for what cost *is*: the per-run **cost vector {tokens, dollars, wall-clock time}**, the **attribution rule** (cost → trajectory/spec-revision), and the **reduction** to cost-per-satisfaction (vector ÷ C33 term). A **definition/Configuration** artifact (README:269), not an engine. | **C46 (this)** |
| I2 | **Cost/usage signal read** | inbound (read) | Read the recorded per-run usage (tokens, latency) from the telemetry path (C24→CXDB; Claude Code usage). Dollars = tokens × model price (C29 `cost_tier`/price ref). C46 **reads + derives**; it does not meter. | C46 (this); **C24/CXDB** (source), C29 (price ref) |
| I3 | **Satisfaction-term read** | inbound (read) | Read C33's satisfaction **distribution** (the term divided into; the series watched for threshold-crossing). Holistic at Sweep-1 (D-15). | C46 (this); **C33** (producer) |
| I4 | **Meta-metric stream record/track** | internal → store | Compute the three series (cost-per-satisfaction, time-to-threshold, judge-FP-rate) per run/spec-revision and **log them as time-series** via the v4-named MLflow/Aim/W&B pack (README:270). C46 owns the **logged schema**; the store is off-the-shelf. | C46 (this); MLflow/Aim/W&B (engine) |
| I5 | **Meta-metric stream output / query** | outbound (data) | Surface the recorded series + trend for C47 (variant-ID), C48 (significance — D-19), C50 (promotion gate, multi-metric F47). Read-surface over the tracked store. | C46 (this); C47/C48/C50 (consumers) |
| I6 | **Judge-outcome label feed** | inbound (read) | The labelled outcomes that make a judge pass a *false* positive: loop-closure failure (C39), operator override (C35), human review. C46 reads these to compute judge-FP-rate; it does not generate the labels. | C46 (this); C39/C35 (label sources) |
| I7 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as the Gas City **meta-metric pack** (C02/C17 ABI, README:470); the cost model + metric defs + the supplied time-to-threshold cutline configured via pack TOML (C03, "Configuration", README:269). | C02/C17/C03 (ABI/config); C46 (binding) |

**Invariants C46 must uphold:**
- **INV-1 (multi-metric, never a single target — F47).** C46 always records the **aggregate of multiple
  meta-metrics**; it never collapses the factory's performance to one optimisable number. This is the
  load-bearing Goodhart guard (F-MODE F47 "Multi-metric mandatory"): a single visible target is forbidden by
  construction, so no consumer (C50) can optimise one metric to the others' ruin.
- **INV-2 (records, does not decide — no significance, no promotion).** C46 **measures and records** series;
  it computes **no** statistical significance (C48, D-19) and makes **no** promotion decision (C50). Like C33's
  INV-2/INV-3 (distribution, no verdict), C46 produces *measured trends*, never a "better/promote" verdict.
- **INV-3 (cost model is defined, not metered here — G32).** C46 **defines** cost (I1) and **reads** the raw
  usage (I2); it never *incurs* or *captures* cost. The cost numbers are a function of telemetry (C24) × price
  (C29), so C46 owns no source-of-truth usage feed — it is a **derived view** over recorded usage + C33
  satisfaction (parallels C33's INV-5 re-derivable view).
- **INV-4 (threshold-free except as a supplied input — G09).** Time-to-threshold **consumes** a cutline given
  by the decision owner (C50/C53/C39); C46 neither owns nor decides the cutline (G09 reading (b), inherited
  from C33). With no cutline configured, the other two series (cost-per-satisfaction, judge-FP-rate) remain
  fully defined; only time-to-threshold needs the supplied cutline.
- **INV-5 (population-/trend-honest).** Every recorded point carries its **provenance** (which spec-revision /
  run-cohort, sample count n from C33) and timestamp; a cost-per-satisfaction computed over n=3 trajectories is
  not silently comparable to one over n=300 (inherits C33's INV-4 sample-honesty up the stack — underwrites
  F60 aggregate-rate legibility).
- **INV-6 (off-the-shelf store — the bar).** The series are persisted through the v4-named MLflow/Aim/W&B
  tracking pack (README:270); C46 stands up **no** custom time-series engine. C46 owns only the *logged
  schema*, not storage.

## 4. Data model / state

C46 **owns the meta-metric definitions + the logged schema**, not a durable source-of-truth store. The
satisfaction is C33's; the raw usage is the telemetry path's (C24/CXDB); the time-series store is MLflow/Aim/W&B's.

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Cost-model definition (I1)** | The per-run cost vector {tokens, $, time}, attribution rule, and reduction to cost-per-satisfaction. The **core G32 deliverable** — a definition/config artifact. | Pack TOML / config (C03; "Configuration", README:269). | **C46 (this)** |
| **Meta-metric series (the three streams)** | cost-per-satisfaction, time-to-threshold, judge-FP-rate as time-series points (value + provenance + timestamp). C46 owns the **logged schema**; values are derived on each run. | Logged to the **MLflow/Aim/W&B** tracking store (README:270) — off-the-shelf, not C46-built. Re-derivable from C24 usage + C33 satisfaction. | C46 (schema); MLflow/Aim/W&B (store) |
| **Metric + tracking config** | Which metrics are recorded (the three named + any operator-added — AI-CONTEXT:516), the supplied time-to-threshold cutline, the cost-vector dimensions, attribution + cohort keys. | Pack TOML (C02/C03 model). | C02/C03 (model); C46 (binding) |
| **Cost/usage signal (read-only input)** | Recorded per-run tokens/latency. **Owned by the telemetry path (C24/CXDB)**, read-only to C46. | CXDB / telemetry store (C24). | **C24/C21** |
| **Satisfaction distribution (read-only input)** | C33's holistic distribution + n. **Owned by C33**, read-only to C46. | C33 output (re-computable). | **C33** |

> [FAITHFUL-FILL] v4 specifies the *behavior* ("records cost-per-satisfaction, time-to-threshold, judge-FP-rate
> over time", inventory C46:58; README:269) and the *store* (MLflow/Aim/W&B, README:270) but not C46's persisted
> schema. The minimal faithful set is **the definitions + the logged schema**, with **no C46-owned
> source-of-truth store**: the meta-metrics are a **derived view** over recorded usage (C24) and satisfaction
> (C33), logged to the off-the-shelf tracker. The exact cost-vector record (field names, the price-lookup
> binding, the canonical tag/cohort set) is **sweep-2**, frozen with C33's distribution-record (the satisfaction
> term) and C48's compare contract (the significance consumer).

> [FAITHFUL-FILL] v4 names the **three** meta-metrics (README:269) but AI-CONTEXT:516 explicitly leaves "**which
> specifically**" open as a "**values question — needs operator input**." The minimal faithful choice: the
> **three named** are the Sweep-1 canonical set; the stream definition is **extensible by config** (operators
> may add metrics) — but the *set selection beyond the three* is an operator policy v4 defers, not a C46
> invention (OQ-2).

**Consistency / lifecycle.** C46 stands up in **Phase 3d** with the self-optimization pack (README:470), last,
after the eval + telemetry tiers it reads from are solid. It owns no durable truth: the **usage** lives in the
telemetry store (C24/C21), the **satisfaction** in C33's re-computable distribution, the **series** in the
off-the-shelf tracker — so C46 is a **definition + derivation layer**, which is why the bar keeps it thin
(no custom engine, no source-of-truth store; §6).

## 5. Behavior

**Stand up (Phase 3d).** The meta-metric pack is installed (README:470); the cost model (I1), the metric set
(the three named + any operator additions), the supplied time-to-threshold cutline, and the tracking-store
binding (MLflow/Aim/W&B) are configured via pack TOML (README:269 "Configuration"). C46 is wired downstream of
C33 (satisfaction), C24/CXDB (usage), and C39/C35 (judge-outcome labels), and upstream of C47/C48/C50.

**Record path (per run / per spec-revision iteration).**
1. **Read the satisfaction term (I3):** pull C33's holistic distribution for the run/spec-revision (the
   satisfaction the factory just produced); carry its sample count n (INV-5).
2. **Read + derive cost (I1/I2):** read the run's recorded usage (tokens, latency) from the telemetry path
   (C24/CXDB); derive dollars (tokens × C29 price) and assemble the **cost vector {tokens, $, time}**,
   attributed to the trajectory/spec-revision.
3. **Compute the three series points (I4):**
   - **cost-per-satisfaction** = cost vector ÷ the C33 satisfaction term;
   - **time-to-threshold** = elapsed time/run-count for the spec-revision's satisfaction to cross the
     *supplied* cutline (INV-4) — undefined-but-skipped if no cutline configured;
   - **judge-FP-rate** = (judge-passed-but-later-found-bad) ÷ (judge-passed), from the C39/C35 label feed (I6).
   No significance test (INV-2); no promotion decision.
4. **Record (I4):** log each point — value + provenance (spec-revision/cohort, n) + timestamp — to the
   off-the-shelf MLflow/Aim/W&B store. **All** configured metrics are recorded together (INV-1 multi-metric).
5. **Surface (I5):** the recorded series + trend are queryable by C47 (variant-ID), C48 (significance — D-19),
   C50 (multi-metric promotion gate — F47).

**Trend / aggregate awareness (F60).** Because the streams are time-series, C46 surfaces **aggregate-rate**
behaviour (e.g. 1−(1−p)ⁿ compounding across parallel cycles, F-MODE F60) rather than single-cycle snapshots —
the property the self-optimization loop reasons over.

> The exact cost-vector schema, the per-metric record shape, the price-lookup binding, the canonical tag/cohort
> set, and whether series are stored continuous vs bucketed are **sweep-2+** (frozen with C33's distribution
> record + C48's compare contract). C46 runs **no** significance test (that is C48) and makes **no** promotion
> decision (that is C50).

## 6. Failure modes & handling

C46 owns the **cost-model gap (G32 — its core deliverable)** and is the **satisfaction-input consumer (G09)**.

**G32 (major) — cost is essentially unmodeled. ADDRESSED HERE (C46 is the cost-quantification home).** G32
flags that the only cost figure in v4 is "$200/month Max" and that P12's headline meta-metric
"cost-per-satisfaction" has **no cost model** for scenario suites, multi-judge ensembles, A/B replays,
trajectory embedding, or second-family-judge tokens. The whole corpus routes this gap to C46 (C29:G32,
C28:OQ-2, C32:OQ3, C37:OQ-3, C38:OQ5, C55:OQ-3; review-log "C29:G32 — cost-per-satisfaction model deferred to
C46"). **Faithful resolution — C46 defines the cost model:**
- **The cost MODEL is a per-run cost vector {tokens, dollars, wall-clock time}.** These are the three cost
  dimensions v4 gestures at: **tokens** (the missing "token-budget math", G13/G32), **dollars** (a derived
  function of tokens × the model's price — C29 carries the `cost_tier`, D-10 — not a separately metered feed),
  and **wall-clock time** (the basis for time-to-threshold). Cost is **attributed** to a trajectory/spec-revision
  via the run identity on the telemetry (C24). *This is the smallest model that makes all three named
  meta-metrics computable and is fully consistent with v4's "Configuration / your work" placement (README:269).*
  > [FAITHFUL-FILL] v4 names **no** cost dimensions explicitly; it only names *cost-per-satisfaction* as the
  > metric and "$200/month Max" as the one figure (G32). {tokens, $, time} is the minimal set that (a) covers
  > every unmodeled cost G32 enumerates (suite/ensemble/replay/embedding/judge tokens are all *token* costs),
  > (b) yields *dollars* without a new meter (tokens × price), and (c) supplies the *time* term
  > time-to-threshold needs. It is a **definition**, not an engine — exactly README:269's "Configuration".
- **cost-per-satisfaction = cost vector ÷ the C33 satisfaction term (I1).** C46 owns the **division/reduction**;
  the satisfaction term is C33's (G09), the raw usage is the telemetry path's (C24). C46 synthesises **no** raw
  cost — it **reads + derives** (INV-3), so it adds no metering machinery.
- **What stays open (not C46's to fix):** the *price table* (per-model $/token) under Max's flat subscription
  is itself murky (Max is $200/mo flat, not per-token — G13); C46's dollar figure is therefore a **modelled
  approximation** (tokens × a configured reference price), and the **absolute** dollar accuracy under a flat
  subscription is an operator/integrator policy input, not something C46 can derive (OQ-1). The **token** and
  **time** dimensions are exact; the **dollar** dimension is model-dependent.

**G09 (minor) — satisfaction input from C33. ADDRESSED HERE (consumed, not redefined).** G09 is C33's metric
gap; for C46 it is an **input dependency**, not a definition duty. C46 **consumes C33's satisfaction
distribution** as the term it divides cost by and watches for threshold-crossing (inventory C46 `depends on
C33`). Two C46-relevant facets:
- **Which satisfaction does C46 read? — RESOLVED by D-15 (holistic).** C46 reads C33's **holistic** distribution
  (one graded satisfaction per trajectory over C08's free-form DoD). Consequence: C46's meta-metrics are
  **factory-level / per-spec-revision**, **not per-criterion**. Per-criterion meta-metric *diagnosis* (which
  part of the spec costs the most satisfaction) is the **primary beneficiary of the deferred FE-5** enumerated
  per-criterion DoD — and per D-15 that "is built last" beneficiary is **C46**. So **C46 explicitly does
  *not* require enumerated per-criterion DoD at Sweep-1**; per-criterion meta-metrics are the clean Sweep-2
  extension to I3/I4, revisited when FE-5 lands (OQ-3).
- **The threshold for time-to-threshold — DEFERRED (not C46's, inherited from C33).**
  > [AMBIGUITY: G09] "Time-to-threshold" (README:269) needs a satisfaction *cutline*, but v4 **never defines
  > the cutline or what "satisfied" means** (G09; F40/F47). Two readings: **(a)** C46 owns the cutline and
  > decides "satisfied"; **(b)** C46 only **consumes** a cutline supplied by the decision owner and records the
  > *time* to reach it, owning no cutline. **Chosen: (b)** — identical to C33's resolved reading: P6 is
  > "satisfaction **not** test-pass", so a cutline is a *decision-site* property (C50 promotion / C53 bootstrap
  > / C39 loop-closure), never a property of the metric/measurement. C46 therefore **records time-to-threshold
  > against a supplied cutline (INV-4)**; the cutline's **value** is operator/integrator policy v4 does not fix
  > (OQ-1, shared with C33:OQ-1). With no cutline configured, time-to-threshold is simply not recorded; the
  > other two series are unaffected.

**Other failure cases.**
- **Missing satisfaction term (C33 returns insufficient-sample / n=0).** Record cost and judge-FP if available,
  but emit cost-per-satisfaction as **undefined/insufficient-sample** (carry n, INV-5) rather than dividing by
  a hollow satisfaction — never fabricate a ratio from n=0. *[FAITHFUL-FILL]: mirrors C33's small-n honesty up
  the stack; minimal honest choice.*
- **Missing/partial cost signal (telemetry gap, C24 back-pressure/outage — G33).** Record the meta-metric with
  the cost dimension(s) available and **flag the gap** (e.g. tokens known, dollars unknown); do not block the
  whole stream on one missing signal, and do not silently impute cost. *[FAITHFUL-FILL]: fail-open-per-dimension,
  mirrors C24/C21 fail-open posture; v4 silent.]*
- **Judge-FP label latency (I6).** Judge-FP-rate is **retrospective** — a judge "pass" only becomes a false
  positive when a *later* signal (C39 loop-closure failure / C35 override / human review) contradicts it. C46
  records judge-FP-rate as a **trailing** series and must not present early/unlabelled passes as confirmed-true
  (the rate is over *labelled* outcomes only). *[FAITHFUL-FILL]: the only honest construction of an
  FP-over-time rate; v4 names the metric, not its labelling latency.]*
- **Significance / "is the variant better?"** is **out of scope** — routed to **C48** (D-19). C46 surfaces a
  raw trend; any significance claim is C48's (boundary; mirrors C33→C48).

> F-mode applicability is owned by **C57** (coverage map). C46 underwrites the meta-metric-layer properties
> several modes lean on — **F47** (Goodhart on visible metrics: C46 is *why* "multi-metric mandatory" is true —
> it records the aggregate of multiple metrics, INV-1, so no single visible target exists), **F60** (parallel-
> cycle compounding: C46's time-series force **aggregate-rate** awareness, 1−(1−p)ⁿ), and partially **F40**
> (last-mile drift: "shipping rate vs project-start rate" is exactly a meta-metric trend C46 can record) and
> **F48** (same-family-judge bias: judge-FP-rate over time is the monitor that would *measure* the bias D-1
> accepts — review-log C32:OQ1 "judge-FP via C46?"). C46 **records** these signals but does **not** resolve the
> deferred **threshold-definition** modes (F40/F47 cutline) — that depends on the deferred G09 cutline. C46
> defers the canonical F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C46 is held to *only* the P12-tied capability (the
**meta-metric stream** that makes factory performance measurable over time) plus the two pieces v4 explicitly
calls custom/your-work: the **cost-model definition** (I1, README:269 "Custom … Configuration") and the
**cross-stack glue** that joins cost (C24) + satisfaction (C33) into one recorded series. **Dropped / refused as
non-principle or not-C46's:** (1) any **custom time-series / metrics engine or dashboard** — the v4-named
**MLflow/Aim/W&B** tracking pack already does this (README:270; "Mature", AI-CONTEXT:353), and the
prometheus/time-series + experiment-tracking capability is exactly what the stack already provides (INV-6);
(2) **statistical significance / CI / hypothesis testing** — that is the v4-named **scipy/Evidently** stack at
**C48** (README:275; **D-19**), not a C46 estimator (same boundary C33 holds at §6); (3) a **promotion / "is the
variant better" decision** — that is **C50** (the multi-metric gate); (4) the **satisfaction computation
itself** — that is **C33** (C46 only consumes the term); (5) **token/usage metering** — that is the telemetry
path (**C24/C25/C26**); C46 reads, it does not capture; (6) a **per-token dollar accounting** beyond a
modelled tokens × reference-price approximation — exact $ under a flat Max subscription is an operator policy
input (OQ-1), not C46 machinery; (7) **per-criterion meta-metrics** — deferred with FE-5 to Sweep-2 (D-15).
What is **kept**: the **cost-model definition** (the genuine G32 deliverable — load-bearing, *and the one v4
names as your work*) and the **meta-metric stream definitions + the cross-stack glue** that the off-the-shelf
tracker does not itself span.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C46 reads **metrics about** runs (satisfaction distributions, usage counts, FP labels), not raw
  prompts/outputs — low sensitivity, like C33; it inherits the telemetry store's access posture and adds no new
  exposure. It performs no model call (no judge/coder credential needed).
- **Cost.** C46 is **the cost-quantification home** (its whole purpose) but is itself **negligible** to run: a
  pack doing a division (cost ÷ satisfaction) + a log-write to MLflow/Aim/W&B per run — no model tokens, no
  managed store beyond the off-the-shelf tracker. *Meta-note: C46 is where the corpus's deferred cost questions
  (C28/C32/C37/C55 single-Max-seat fan-out, G13/G34) finally become measurable — C46 supplies the number those
  specs said they could not, but it does not itself bound throughput (that is C04/C28/scheduling).*
- **Scale.** Recording cost is O(1) per run; the time-series store handles retention/rollup (its job, not
  C46's). The only honest scale note: at L5 volume the FP-label join (I6) and the per-run satisfaction read
  (I3) should be incremental, not full re-scans — a sweep-2/perf concern (OQ), not a Sweep-1 design force. No
  bespoke scaling machinery is warranted (the bar).
- **Observability.** C46 **is** the meta-observability layer — the factory watching itself. Its own health
  (which metrics recorded, gaps flagged for missing cost/satisfaction signals, last-recorded per series) is
  worth emitting, but C46 is the thing *being read* by the self-opt loop, not a heavy emitter.
- **Ops.** Pack-delivered, operated with the self-optimization pack in Phase 3d (README:470). Pin the
  MLflow/Aim/W&B version so the tracked-series schema is reproducible; the cost-model **price reference** (for
  the dollar dimension) is operator-maintained config (OQ-1), reviewed when Max pricing/terms change.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (meta-metrics over time — inventory C46:58):** given a sequence of runs, C46 records
   **cost-per-satisfaction, time-to-threshold, and judge-FP-rate** as **time-series** (README:269), each point
   carrying provenance + timestamp.
2. **AC-2 (cost model defined — G32, I1):** C46 is the spec-of-record for a **per-run cost vector
   {tokens, $, time}**, an attribution rule, and the reduction to cost-per-satisfaction (cost ÷ C33 term);
   token + time dimensions are exact, the dollar dimension is a modelled tokens × reference-price (OQ-1).
3. **AC-3 (consumes satisfaction, does not compute it — boundary, G09):** every satisfaction value is **C33's
   holistic distribution** (D-15); C46 makes **no** judge/model call and reduces **no** judge scores.
   (Verifiable: C46 runs with no judge provider and no C33 internals, reading C33's output only.)
4. **AC-4 (multi-metric mandatory — INV-1/F47):** C46 records the **aggregate of multiple** metrics together;
   there is **no** mode that exposes a single optimisable target (the Goodhart guard).
5. **AC-5 (records, does not decide — INV-2):** C46 runs **no** statistical significance test (that is C48,
   D-19) and makes **no** promotion decision (that is C50); it emits measured series + raw trend only.
6. **AC-6 (threshold-free except as supplied input — INV-4, addresses G09):** cost-per-satisfaction and
   judge-FP-rate are fully defined with **no** cutline configured; time-to-threshold is recorded **only** when
   a cutline is supplied, and C46 renders **no** "satisfied" verdict from it.
7. **AC-7 (off-the-shelf store — INV-6, the bar):** the series are persisted via the v4-named **MLflow/Aim/W&B**
   tracking pack (README:270; AI-CONTEXT:353/378); **no** bespoke time-series engine/dashboard is present.
8. **AC-8 (signal-honest — INV-5):** every point carries provenance + sample count (n from C33); a missing
   satisfaction term yields an **insufficient-sample** cost-per-satisfaction (not a fabricated ratio), and a
   missing cost dimension is **flagged**, not imputed.
9. **AC-9 (consumable downstream — I5):** the recorded series are consumable by **C47** (variant-ID), **C48**
   (significance — D-19), and **C50** (multi-metric promotion gate) per their inventory dependencies.

**Test strategy.** A **meta-metric pack** that seeds a synthetic sequence of runs — each with a usage record
(telemetry/C24 shape), a C33 satisfaction distribution (varied, incl. small-n/insufficient), and judge-outcome
labels (incl. later-contradicted passes for judge-FP) — and drives AC-1…AC-9: in particular that the output is
a **multi-metric time-series** (AC-1/AC-4), that the **cost model** divides cost by satisfaction correctly with
the {tokens,$,time} vector (AC-2), that it is **threshold-free** except for a supplied cutline (AC-6), that **n
+ gaps are surfaced** (AC-8), that it uses the **off-the-shelf tracker** (AC-7), and that it runs **no
significance test / no promotion** (AC-5). This suite **must pass before C47/C48/C50 consume the meta-metrics**,
since the self-optimization loop assumes C46's series are the canonical "is the factory improving?" signal.

## 9. Open questions

- **OQ-1 (→ review-log, top): G32 cost-model dollar dimension + price reference.** §6 defines cost as
  {tokens, $, time} with tokens/time exact and dollars = tokens × a **reference price**. Under a **flat $200/mo
  Max subscription** (G13) there is no per-token price, so the dollar figure is a *modelled approximation* whose
  reference price is **operator/integrator policy**. Confirm the dollar dimension is an operator-maintained
  config input (not C46-derived), and how it is set under a flat subscription (amortised? marginal-zero? a
  notional API-equivalent price?). Token + time dimensions stand regardless.
- **OQ-2 (→ review-log): which meta-metrics beyond the three (AI-CONTEXT:516 "values question").** v4 names
  three (README:269) but explicitly leaves "which specifically" to operator input (AI-CONTEXT:516). Sweep-1
  fixes the **three named** as canonical + makes the set **config-extensible**; confirm whether the operator
  adds others (and which) at sweep-2 — and that C50's multi-metric gate reads whatever set C46 records.
- **OQ-3 (→ review-log): per-criterion meta-metrics (FE-5 / D-15 beneficiary).** C46 reads C33's **holistic**
  satisfaction (D-15), so meta-metrics are factory-level. The deferred **FE-5** (enumerated per-criterion DoD)
  names **C46's per-criterion diagnosis** as its primary beneficiary "built last." Confirm per-criterion
  meta-metrics are the Sweep-2 extension to I3/I4, revisited when FE-5 lands (C46 does **not** require
  enumerated DoD at Sweep-1). (Shared with C33:OQ-3 / D-15.)
- **OQ-4 (→ review-log): C46↔C48 compare-contract + C46↔C33 schema freeze.** C46 records series; **C48** tests
  significance (D-19). Freeze (a) the **logged metric-record schema** jointly with C33's distribution-record
  (the satisfaction term) and (b) the **read-surface C48 consumes** at sweep-2, so the significance consumer and
  the meta-metric producer agree on shape. (Mirrors C33's "freeze with C46" — now reciprocated.)
- **OQ-5 (→ review-log): judge-FP label source + latency (I6).** Judge-FP-rate needs *labelled* outcomes
  (judge passed, later found bad). Confirm the label sources (C39 loop-closure failure, C35 override, human
  review) and how the **trailing** FP-rate handles label latency without mispresenting unlabelled passes.
