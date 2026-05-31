# C33 — Satisfaction Metric Aggregator  (Spec, canonical track)

> Source: README §"Principle 6 — Satisfaction not test-pass" (line 181 "Probabilistic metric over scenario
> trajectories. LLM-as-judge. Boolean assertions don't survive at scale"; line 188 table row "Satisfaction
> metric aggregation | **Distribution over trajectory population** | Inspect AI score reduction | MIT | Gas
> City pack"; Phase 2 line 426 "Build satisfaction aggregator: **small Go tool node reading judge outputs from
> beads, computing distributions**"; line 440 "**P6** … Inspect AI scorer + **Gas City aggregator** +
> cross-family enforcement"; line 269 meta-metric row "cost-per-satisfaction, **time-to-threshold**, judge
> false-positive rate"); AI-CONTEXT §"12 principles" (line 36 "Satisfaction not test-pass | **Probabilistic
> over trajectory population**"), §"Layer 2" decisions (line 302 "Satisfaction aggregation | **Inspect AI
> score reduction** | MIT | Mature within framework"; line 373 "Inspect AI | L2: authoring + runner + judge +
> **aggregation**"; line 393 "Aggregation: **Inspect AI score reduction**, MLflow tracking"); component-inventory
> C33 row (line 45 "Computes the satisfaction distribution over the trajectory population from judge outputs";
> maps A53/A19/B41; depends C32, C19; gap G09; foundational yes) + Batch-3 note (line 111); spec/C32 (judge
> output = the input C33 reduces); spec/C30 §1 (line 110 "aggregating scores into a satisfaction distribution
> is **C33**"); spec/C31 §3 (INV-4 "verdict-blind … C32/C33 do"); spec/C19 (bead store the judge outputs land
> on); spec/C08 §8 (the spec's acceptance/DoD surface C33 scores *against* — Reading A collapsed spec);
> F-MODE-COVERAGE F2/F39/F47/F60 (satisfaction-over-population as the reward-hacking / region-mismatch /
> Goodhart / compounding-error guard); ambiguities-and-gaps G09; review-log D-1 (judge same-provider),
> D-6 (canonical track); FUTURE-ENHANCEMENTS FE-5 (enumerated per-criterion DoD — decision below).
> Inventory ID: C33   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C33 is the factory's **satisfaction-metric aggregator**: the **Gas City pack / tool node** that **reads judge
outputs (C32) for a population of scored trajectories and reduces them into the satisfaction *distribution*
over that population** (README:188, 426; AI-CONTEXT:36). It is the component that operationalises **Principle 6
— "satisfaction not test-pass"**: where a test suite yields one boolean, C33 yields a **distribution of
per-trajectory satisfaction scores** (and summary statistics over it) so the factory reasons about *the
variety of outcomes a spec produces*, not a single green/red. This is the **P5 Ashby's-law** posture made
measurable — measuring the variety of outcomes (the spread of satisfaction), not collapsing it to a point.

C33 is the **spec-of-record for the satisfaction-metric definition (G09)**: what one trajectory's satisfaction
*is* (the judge's score), how a population of them is *reduced* (the distribution + its summary statistics),
and — explicitly bounded below — what is **deferred** (the pass/fail *threshold* / "satisfied" cutline, which
v4 never defines). It is **deliberately thin**: v4 names the engine as **Inspect AI score reduction** (a mature
MIT capability, AI-CONTEXT:302; v4's named companion is **MLflow tracking**, AI-CONTEXT:393) wrapped as a Gas
City pack; C33's *custom* surface is only the **distribution shape + the bead-population read/aggregate glue**
that Inspect AI's per-task reduction does not by itself span (README:426 "small Go tool node … computing
distributions").

**Responsibilities (what C33 is the spec-of-record for):**
- **Read judge outputs for a trajectory population (I1).** Pull the per-trajectory judge results — scores +
  the run/scenario identity they carry — from where C32 lands them: **judge-output beads on C19** (README:426
  "reading judge outputs **from beads**"; inventory C33 `depends on C19`).
- **Define the per-trajectory satisfaction *score* (G09, partial).** One trajectory's satisfaction = its
  **judge score** (C32's output) — a graded value, *not* a boolean test-pass (README:181; P6). C33 owns the
  **normalisation contract** (what scale judge scores are reduced on); the score *value* is C32's.
- **Reduce the population into a *distribution* + summary statistics (I2).** Compute, over the population of
  per-trajectory scores, the **satisfaction distribution** and its summary statistics (count, mean/median,
  spread, quantiles; and — *only if* an optional reporting cutline is configured — rate-above-cutline) — the
  "distribution over trajectory population" of README:188. The engine is v4's named **Inspect AI score
  reduction** (README:188; AI-CONTEXT:302/393), plus a **thin stats helper** for the distribution summaries
  Inspect AI's per-task reduction does not itself emit — **not** a custom statistics engine.
  > [FAITHFUL-FILL] v4 names **only** "Inspect AI score reduction" (companion: MLflow tracking, AI-CONTEXT:393)
  > for C33's aggregation; `numpy`/`pandas` appear nowhere in v4 and `scipy` is named in v4 specifically as
  > **C48**'s A/B significance engine (README:275; AI-CONTEXT:360/421). So any stats library behind Inspect
  > AI's reduction is a minimal *helper* inference for quantiles/spread, NOT a v4-stated C33 engine and
  > explicitly NOT the scipy significance machinery (that is C48). Concrete library choice is sweep-2.
- **Define the population/grouping key (I3).** What set of trajectories one distribution is computed over —
  **per spec-revision** (the unit C08 §7 obs names: "A spec revision is the unit a satisfaction metric (C33)
  … are computed *against*", C08:112), optionally sliced per scenario / per run-cohort.
- **Emit the satisfaction metric as a typed result (I4).** Surface the distribution + statistics as the tool
  node's declared output, consumable by **C46** (meta-metrics: cost-per-satisfaction, time-to-threshold —
  README:269), **C53** (bootstrap-validation gate — inventory C53 `depends on C33`), and **C55** (methodology
  experiment loop — inventory C55 `depends on C33`).

**Explicitly NOT (boundaries):**
- **NOT the judge.** Scoring *one* trajectory against *one* scenario (the LLM-as-judge) is **C32** (README:185;
  spec/C30:110). C33 never invokes a model and never scores a trajectory; it only **reduces scores C32 already
  produced**. C33 is model-free and deterministic.
- **NOT the threshold / promotion gate / "is this good enough" decision.** C33 *computes* the distribution; it
  does **not** own a pass/fail cutline, a "satisfied" verdict, or a ship/no-ship decision. The
  satisfaction-vs-threshold *gate* is **C50** (promotion gate) / **C53** (bootstrap validation) / **C39**
  (loop-closure); the **threshold itself is undefined in v4 and is deferred (G09, §6)**. C33 may *report* a
  rate-above-a-supplied-cutline as one statistic, but it does not *decide* the cutline or act on it.
- **NOT the meta-metric stream.** cost-per-satisfaction, time-to-threshold, and judge-false-positive-rate over
  *time* are **C46** (README:269; inventory C46 `depends on C33`). C33 produces the *satisfaction* term C46
  divides cost by; it does not model cost, time, or trend.
- **NOT a custom statistics engine.** The reduction is v4's named **Inspect AI score reduction**
  (AI-CONTEXT:302/393) plus a thin distribution-summary helper ([FAITHFUL-FILL]; v4 names no stats library for
  C33 — see I2). C33 introduces **no bespoke estimator, bootstrap, or significance machinery** — A/B
  significance testing lives in **C48** (the v4-named scipy/Evidently engine, README:275). If a future need
  arises for confidence intervals on the satisfaction rate, that is C48/C46 territory, not a C33-owned stats
  engine (§6, the-bar note).
- **NOT the trajectory store or the judge-output schema.** Trajectories live in **C21** (CXDB); the
  judge-output *bead* shape is **C20**'s schema over **C19** (C33 *reads* it, does not define it). C33 owns the
  *aggregation* contract, not the storage or the input record format.
- **NOT the spec's Definition-of-Done.** What a trajectory is scored *against* is the **C08 spec** (its
  acceptance/DoD surface) interpreted by the **C32 judge** — C33 never reads the spec. The FE-5 question (does
  satisfaction require *enumerated per-criterion* DoD in C08?) is addressed in §6 and **flagged to the
  integrator; C33 does not unilaterally change C08**.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (judge output) | **C32** Judge harness | Produces the per-trajectory **judge score** C33 reduces. Same provider/family as coder (D-1) — does not change C33, which is provider-agnostic (it consumes scores, not models). Inventory C33 `depends on C32`. |
| Upstream (population source) | **C19** Bead work-graph | The durable store where C32's judge outputs land as beads; C33 **reads the judge-output beads** for a population ("reading judge outputs from beads", README:426). Inventory C33 `depends on C19`. |
| Input-record schema | **C20** Bead schema registry | Owns the judge-output bead *type/payload* (score + run/scenario identity) C33 reads. C33 uses the registered type; it does not define it. |
| Reduction engine | **Inspect AI score reduction** (pack-wrapped) | The MIT, "mature within framework" reducer (AI-CONTEXT:302; v4's named companion is MLflow tracking, AI-CONTEXT:393) C33 wraps as a Gas City pack; plus a thin stats helper for distribution summaries (`[FAITHFUL-FILL]` — v4 names no stats library for C33; scipy is C48's). Pattern/engine reuse, not custom stats. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C33 is a **small Go tool node in a Gas City pack** (README:426/440), invoked via the tool-node protocol. *(Related interface, not a dependency edge; mirrors how C24 names C02/C17.)* |
| Downstream (meta-metrics) | **C46** Meta-metric stream | Consumes the satisfaction term to compute cost-per-satisfaction / time-to-threshold (README:269). Inventory C46 `depends on C33`. |
| Downstream (bootstrap gate) | **C53** Bootstrap-validation milestone | The go/no-go gate that needs a satisfaction rubric, not "looks good" (G23); reads C33's distribution. Inventory C53 `depends on C33`. |
| Downstream (methodology loop) | **C55** Methodology-experiment loop | Selects methodology per work-type by **empirical** satisfaction; reads C33. Inventory C55 `depends on C33`. |

**Position in the system.** C33 is **Batch-3** (component-inventory line 111), built in **Phase 2** with the
rest of the evaluation tier (Inspect AI wrap, scenario isolation, judge, satisfaction aggregator —
README:421–427). It is **foundational** (inventory C33: Foundational? = yes) — not because it is large, but
because it is the **satisfaction-metric definition** that **C46, C53, C55** (and through C46, the whole
self-optimization tier) contract against: "what satisfaction *is* as a number" is fixed here. It is on the
P5/P6-delivery path (README:440) and is **feature-flag-gated** with the evaluation pack (it exists only when
the scenario/judge capability is enabled, C03).

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete reducer signatures / distribution-record schema / the
exact statistic set defer to sweep 2 (and the judge-output bead shape to C20, the reduction primitives to
Inspect AI).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Judge-output population read** | inbound (read) | Query C19 for the judge-output beads constituting a population (by grouping key, I3); each carries a per-trajectory **score** + run/scenario identity (README:426). | C33 (this); **C19/C20** (store + record) |
| I2 | **Score reduction → distribution + statistics** | internal | Reduce the population of scores into the **satisfaction distribution** and summary statistics (count, mean/median, spread, quantiles; rate-above-cutline only if a cutline is configured). Engine = v4-named **Inspect AI score reduction** + a thin distribution-summary helper (`[FAITHFUL-FILL]`; v4 names no stats library for C33, scipy is C48's) — no custom estimator. | C33 (this); Inspect AI (engine) |
| I3 | **Population / grouping key** | input (config) | Defines the trajectory set one distribution spans — default **per spec-revision** (C08 §7 obs, C08:112), optionally sliced per scenario / cohort. Sweep-1 names the key; the canonical slice taxonomy is sweep-2. | C33 (this) |
| I4 | **Satisfaction-metric result output** | outbound (data) | The tool node's declared output: the distribution + statistics + population identity (which spec-revision/scenario set, sample count), surfaced via the tool-node ABI and consumable by C46/C53/C55. | C33 (this); C02/C17 (surfacing) |
| I5 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as a Gas City tool node (C02/C17 ABI); configured via pack TOML (population default, the optional reporting cutline, the score-normalisation rule). | C02/C17 (ABI); C33 (config) |

**Invariants C33 must uphold:**
- **INV-1 (distribution, not boolean — P6).** C33's output is a **distribution + statistics over a population**,
  never a single pass/fail. Even a one-trajectory population is reported as a (degenerate) distribution, not a
  boolean. This is the load-bearing P6/Ashby's-law property (README:181; AI-CONTEXT:36).
- **INV-2 (no scoring — verdict comes pre-computed).** Every input score is **C32's**; C33 performs **no model
  call and no per-trajectory judgement**. C33 is a pure reduction over given scores (deterministic given its
  inputs + config). (C33 *reduces* scores but, like the C31 runner's INV-4, renders **no pass/fail verdict** —
  INV-3; the cutline/decision is C50/C53/C39's. C31:159 hands the scoring layer to C32/C33; C33 then defers
  the pass/fail cutline onward.)
- **INV-3 (threshold-free computation — G09).** C33 **computes** the distribution **without** depending on a
  "satisfied" cutline. A reporting cutline, if supplied, only produces an *additional statistic*
  (rate-above-cutline); it is **never** required for the metric to be well-defined and C33 renders **no**
  pass/fail verdict from it (the cutline/decision is C50/C53/C39 — §6).
- **INV-4 (population-honest — sample size surfaced).** Every result carries its **sample count** (n) and the
  grouping key; a distribution over n=3 is not silently presented as comparable to one over n=300. (Guards the
  F60 "aggregate-rate, not single-cycle" property — small-n satisfaction must be legible as small-n.)
- **INV-5 (reduction is reproducible).** Given the same population of judge-output beads + the same config, C33
  produces the **same** distribution/statistics — it is a deterministic re-derivable view over C19, owning no
  source-of-truth state of its own (the scores live on beads; the trajectories in CXDB).

## 4. Data model / state

C33 **owns the aggregation contract**, not durable source-of-truth data. The **judge-output bead** is C20/C19's;
the **trajectory** is C21's. State C33 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Satisfaction-metric result** | The computed distribution + summary statistics + population identity (grouping key, sample count). The component's *output*, derivable on demand from C19. | Emitted as tool-node output; optionally recorded as a bead/CXDB result for C46 trend use (an *optimization*, not required — re-computable from inputs, INV-5). | C33 (shape); C46 (trend consumer) |
| **Reduction config** | Population-default grouping key, score-normalisation rule, the optional reporting cutline, the statistic set to emit. | Pack TOML (C02/C03 model). | C02/C03 (model); C33 (binding) |
| **Judge-output beads (read-only input)** | Per-trajectory score + run/scenario identity — the population C33 reduces. **Owned by C20/C19**, read-only to C33. | C19 (bead store). | **C20** (schema), **C19** (store) |
| **Trajectory (referenced, not read)** | The scored run; lives in CXDB (C21), reachable via the judge output's run identity. C33 does **not** read trajectory bodies — only the scores about them. | CXDB (C21). | **C21** |

> [FAITHFUL-FILL] v4 specifies the *behavior* ("read judge outputs from beads, compute distributions",
> README:426) but not C33's persisted state. The minimal faithful set is **none that is source-of-truth**: the
> satisfaction metric is a **deterministic reduction** over judge-output beads (C19) — re-runnable any time
> (INV-5), so C33 holds no independent store. Persisting a computed result as a bead is at most an *optimization*
> for C46's trend reads, not required state. The exact distribution-record schema (fields, the canonical
> statistic set, the slice taxonomy) is **sweep-2**, frozen with C46 (the principal consumer) and C20 (the
> input-bead type).

**Consistency / lifecycle.** C33 stands up in **Phase 2** with the evaluation pack (README:421). It owns no
durable truth: the **scores** survive on beads (C19), the **trajectories** in CXDB (C21), so a re-run of C33
reproduces the metric (INV-5). C33 is therefore a **stateless, re-derivable view** — exactly what "reduction"
implies — which is why the bar keeps it thin (no store, no estimator engine; §6).

## 5. Behavior

**Stand up (Phase 2).** The pack is installed; the tool node is configured with the default population key
(per spec-revision), the score-normalisation rule, the statistic set, and any optional reporting cutline. It is
wired downstream of C32 (judge outputs land on C19) and upstream of C46/C53/C55.

**Aggregate path (steady state).**
1. **Select population (I3):** resolve the grouping key (e.g. all judge outputs for a given spec-revision,
   optionally a scenario/cohort slice).
2. **Read judge outputs (I1):** query C19 for that population's judge-output beads; collect per-trajectory
   scores + identities.
3. **Reduce (I2):** apply v4's named Inspect AI score reduction + a thin distribution-summary helper
   (`[FAITHFUL-FILL]`; no v4-named stats library for C33) to produce the **satisfaction distribution** and
   summary statistics (count, central tendency, spread, quantiles, and — if a reporting cutline is configured
   — rate-above-cutline). No model call (INV-2); no pass/fail verdict (INV-3).
4. **Emit (I4):** surface the distribution + statistics + population identity (incl. sample count, INV-4) as
   the tool-node output, for C46 (meta-metrics), C53 (bootstrap gate), C55 (methodology selection).

**Re-computation.** Because C33 owns no source-of-truth (INV-5), any consumer can request a fresh metric over a
(possibly enlarged) population at any time; the result is a pure function of the current judge-output beads +
config. There is no checkpoint to recover and nothing to lose on restart.

> The exact reduction signatures, the canonical statistic set + distribution-record schema, the score-
> normalisation rule, and the slice/grouping taxonomy are **sweep-2+** (frozen with C46 + C20). Whether
> "satisfaction" is a continuous distribution, a binned histogram, or both is a sweep-2 representation choice
> (OQ-2). C33 invokes **no** model and runs **no** statistical-significance test (that is C48).

## 6. Failure modes & handling

C33 owns the satisfaction-metric-definition gap (G09) and the deferred FE-5 decision at this component.

**G09 (minor) — satisfaction metric / threshold definition. ADDRESSED HERE (split: definition resolved,
threshold deferred).** G09 flags that v4 describes satisfaction as "a distribution over trajectory population"
but gives **no threshold semantics, no pass/fail cutline, no definition of 'satisfied'** (and F40/F47 reference
thresholds never defined). Faithful resolution, in two parts:
- **The metric *definition* — RESOLVED.** Satisfaction is operationalised exactly as v4 states: **one
  trajectory's satisfaction = its judge score (C32); the population metric = the distribution of those scores +
  summary statistics** (README:188; AI-CONTEXT:36). This is the smallest faithful reading and is fully
  buildable with the v4-named **Inspect AI score reduction** (AI-CONTEXT:302) plus a thin distribution-summary
  helper (`[FAITHFUL-FILL]`; v4 names no stats library for C33 — §1/I2). **C33 is the spec-of-record for this
  definition.**
- **The *threshold* / "satisfied" cutline — DEFERRED (not C33's to own).**
  > [AMBIGUITY: G09] v4 references a satisfaction *threshold* (README:269 "time-to-threshold"; F40/F47) but
  > **never defines the cutline or what "satisfied" means**. Two readings: **(a)** C33 owns a pass/fail
  > cutline and emits a boolean "satisfied"; **(b)** C33 owns only the *distribution*, and any cutline /
  > "satisfied" decision belongs to the **consumer that acts on it** (C50 promotion gate, C53 bootstrap gate,
  > C39 loop-closure). **Chosen: (b)** — it is the reading most consistent with the rest of v4: P6 is explicitly
  > "satisfaction **not** test-pass" (README:181), so collapsing the distribution back to a boolean *inside the
  > metric* would re-introduce the test-pass framing P6 rejects; and the "threshold" always appears in v4 at a
  > **decision** site (promotion, bootstrap go/no-go, meta-metric "time-to-threshold"), never as a property of
  > the metric itself. So **C33 computes a threshold-free distribution (INV-3)**; the cutline is **named but
  > deferred to the gate/decision owners**, and the *value* of any cutline is an operator/integrator policy v4
  > does not fix (OQ-1). C33 may *report* a rate-above-a-supplied-cutline as one statistic, but it neither
  > decides nor acts on the cutline.

**FE-5 (per-criterion DoD) — DECISION POINT, addressed; recommendation = minimal path; flagged to integrator.**
FE-5 (enumerated per-criterion Definition-of-Done living *inside* the spec artifact, with stable per-criterion
IDs that P5/P6 scoring reads) was deferred "to decide when C32/C33 are authored" (FUTURE-ENHANCEMENTS FE-5) —
that is now. C33 scores **against** the C08 spec's DoD. The question: can satisfaction be computed against the
DoD **that already exists in the C08 bundle**, or does it **require** enumerated per-criterion DoD (a real P5
capability, but a **C08 change**)?
- **Finding (load-bearing):** the **C08 spec adopted Reading A** (the prompt-template file *is* the spec; spec/C08
  §1 OQ-1) and ships **no Definition-of-Done at all** in its acceptance contract — C08 AC-1…AC-5 cover
  format/renderability/versioning/lint/loop-closure, **not** a target-system DoD — and its body is **free-form
  Markdown prose** (C08 §7 F18 "the format is free-form Markdown prose"). The `DoD.md`-style per-criterion DoD
  the brief assumes "already exists (holistic/per-section)" only exists under **Reading B** (the standalone
  `spec.md`+`DoD.md` shape from the one-shot corpus), which **C08 did not adopt**.
- **Recommendation (minimal path):** **Compute satisfaction *holistically* against the existing free-form C08
  spec — do NOT require enumerated per-criterion DoD for Sweep-1.** The judge (C32) scores a trajectory against
  the prose spec as-a-whole (a holistic judge rubric), and C33 reduces those holistic scores into the
  distribution. This needs **zero C08 change** and is fully consistent with P6 (a graded judge over a prose
  spec is exactly "satisfaction not test-pass"). **What it costs:** holistic scoring gives a *single* graded
  satisfaction per trajectory but **cannot attribute *which* part of the spec was unmet** — so per-criterion
  diagnosis (and per-criterion meta-metrics in C46) are not available; the satisfaction signal is coarse-grained.
- **The alternative (enumerated per-criterion DoD)** is the genuine P5 capability (per-criterion satisfaction →
  finer Ashby-variety + targeted fix-tasks), but it **requires a C08 change** (add a stable-ID DoD section to
  the spec artifact) **plus** a C32 judge contract that scores per-criterion **plus** a C33 reduction that
  aggregates per-criterion as well as per-trajectory. That is a multi-component change (C08 + C32 + C33) and
  per the brief **C33 must not unilaterally add enumerated-DoD to C08**.
- **`FE-5 → orchestrator/integrator decision` (flagged).** The Batch-3 integrator should rule whether Sweep-1
  ships **holistic-only** (recommended: cheapest, no C08 change) or commits the **enumerated-per-criterion**
  path (C08 + C32 + C33 change). C33's spec is written to the **holistic** baseline; per-criterion aggregation
  is a clean sweep-2 extension to I2/I3 **iff** the integrator rules enumerated-DoD in. (OQ-3.)

**Other failure cases.**
- **Empty / too-small population (I1 returns 0 or n<small).** Emit an explicit *insufficient-sample* result
  (n surfaced, INV-4) rather than a misleading point estimate; never fabricate a distribution from n=0.
  *[FAITHFUL-FILL]: v4 silent on small-n; surfacing n + refusing a hollow estimate is the minimal honest
  choice and underwrites the F60 aggregate-vs-single-cycle property.*
- **Malformed / missing judge-output bead** (score absent or off-scale) → exclude from the population + record
  the exclusion count; do not let one bad bead poison the distribution. *[FAITHFUL-FILL]: minimal
  fail-open-per-record choice; mirrors C24's quarantine-and-continue posture.*
- **Judge disagreement / multi-scorer inputs** (C32 multi-judge ensemble, README:187) → C33 reduces whatever
  per-trajectory score C32 emits; **how** ensemble disagreement collapses to one trajectory score is **C32's**
  contract, not C33's (boundary; OQ-4).

> F-mode applicability is owned by **C57** (coverage map). C33 underwrites the satisfaction-over-population
> property that several modes lean on — **F2** (reward hacking: probabilistic satisfaction, not gate-pass),
> **F39** (region-mismatch: distribution over a region of acceptable trajectories), **F47** (Goodhart:
> distribution + multi-metric, not a single visible target), **F60** (compounding error: aggregate-rate, not
> single-cycle) — and surfaces, but does **not** resolve, the **threshold-definition** classes **F40**
> (last-mile drift "need explicit shipping definition") and **F47** (visible-metric drift), which depend on the
> deferred cutline (G09). C33 defers the canonical F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C33 is held to *only* the P5/P6-tied capability (compute
the satisfaction **distribution** — the variety-of-outcomes measure) plus the low-effort bead-read/aggregate
glue v4 explicitly names as custom ("small Go tool node", README:426). **Dropped / refused as non-principle or
not-C33's:** (1) any **custom statistics engine** — bootstrap/CI/significance machinery is the v4-named
**scipy/Evidently** stack assigned to **C48** (README:275; AI-CONTEXT:360/421), not a new C33 estimator (C33
adds only a thin summary helper behind Inspect AI's reduction — `[FAITHFUL-FILL]`, §1/I2); (2) a built-in **pass/fail
"satisfied" verdict / threshold** — that re-introduces test-pass (anti-P6) and belongs to the C50/C53/C39
decision sites (G09 reading (b)); (3) **trend/cost modelling** (cost-per-satisfaction, time-to-threshold over
time) — that is **C46**; (4) **unilateral enumerated-DoD in C08** — deferred to the integrator (FE-5). What is
**kept**: the distribution definition itself (the P5 variety measure, genuinely load-bearing) and the thin
bead-population read/reduce glue Inspect AI's per-task reduction does not by itself span.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C33 reads **scores about** trajectories (judge-output beads), not raw prompts/outputs — far less
  sensitive than the C24 raw-body path; it inherits C19's access posture and adds no new exposure. It performs
  no model call (no judge-provider credential needed — unlike C32; D-1 is irrelevant to C33).
- **Cost.** A local Go tool node doing a stats reduction over beads — **negligible compute, no model tokens, no
  managed store** (consistent with the no-managed-DB stance). The *judge* tokens are C32's cost; C33 adds none.
  C33 produces the **satisfaction term** C46 later divides cost by (README:269) but models **no** cost itself.
- **Scale.** Reduction cost is linear in population size and trivially handled by the thin stats helper; the only honest
  scale note is that very large populations (many trajectories per spec-revision under L5 volume) should be
  reduced **incrementally / streamed** rather than fully materialised — a sweep-2/perf concern (OQ-2), not a
  Sweep-1 design force. No bespoke scaling machinery is warranted (the bar).
- **Observability.** C33 *is* an observability component — the satisfaction distribution is the headline P6
  signal. Its own health (population sizes reduced, exclusion counts for malformed beads, last-computed
  per key) is worth emitting as events for auditability, but C33 is the thing *being read*, not a heavy emitter.
- **Ops.** Pack-delivered tool node operated with the evaluation pack in Phase 2 (README:421/426). Pin Inspect
  AI's version so the score-reduction contract is reproducible (inherits the eval-tier version-pin discipline).

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (distribution, not boolean — INV-1, P6):** given a population of judge outputs, C33 emits a
   **distribution + summary statistics**, never a single pass/fail (README:188; AI-CONTEXT:36).
2. **AC-2 (read judge outputs from beads — I1):** C33 reads the per-trajectory judge scores for a population
   from C19 judge-output beads (README:426) and reduces exactly that population.
3. **AC-3 (no scoring / pre-computed verdict — INV-2):** C33 makes **no** model call and computes **no**
   per-trajectory judgement; every input score is C32's. (Verifiable: C33 runs with no judge provider
   configured.)
4. **AC-4 (threshold-free — INV-3, addresses G09):** the distribution is well-defined with **no** cutline
   configured; supplying a reporting cutline adds a rate-above-cutline statistic but yields **no** pass/fail
   verdict from C33.
5. **AC-5 (population-honest — INV-4):** every result carries its **sample count** + grouping key; an n=0
   population yields an explicit insufficient-sample result, not a fabricated estimate.
6. **AC-6 (reproducible reduction — INV-5):** the same population + config re-computes the **same** distribution
   (C33 owns no source-of-truth; it is a re-derivable view over C19).
7. **AC-7 (consumable downstream — I4):** the emitted metric (distribution + statistics + population identity)
   is consumable by **C46** (meta-metrics), **C53** (bootstrap gate), **C55** (methodology selection) per their
   inventory dependencies.
8. **AC-8 (engine-reuse, no custom stats — the bar):** the reduction is v4's named **Inspect AI score
   reduction** (AI-CONTEXT:302/393) + a thin distribution-summary helper (`[FAITHFUL-FILL]` — v4 names no
   stats library for C33; scipy is C48's); no bespoke estimator/significance engine is present (significance
   is C48).
9. **AC-9 (FE-5 holistic baseline — addresses FE-5):** satisfaction is computed against the **existing C08
   spec** (holistic judge rubric) with **no C08 change**; per-criterion aggregation is *absent* at Sweep-1 and
   gated on the integrator's FE-5 ruling (OQ-3).

**Test strategy.** A **satisfaction-aggregation pack** that seeds a synthetic population of judge-output beads
on C19 (varied scores, including malformed/missing and small-n cases) and drives AC-1…AC-9 — in particular
that the output is a **distribution** (AC-1), that it is **threshold-free** yet can *report* a supplied cutline
(AC-4), that **n is always surfaced** (AC-5), and that the reduction is **reproducible** and uses the
**off-the-shelf reducer** (AC-6/AC-8). This suite **must pass before C46/C53/C55 consume the satisfaction
metric**, since they assume C33's distribution is the canonical satisfaction number.

## 9. Open questions

- **OQ-1 (→ review-log, top): G09 threshold value + ownership.** §6 binds C33 to a **threshold-free**
  distribution (reading (b)) and defers the "satisfied" cutline to the decision sites (C50/C53/C39). Confirm
  the cutline lives there (not in C33), and that the **value** of any threshold is an operator/integrator
  policy v4 does not fix (F40/F47 depend on it).
- **OQ-2 (→ review-log): distribution representation + statistic set.** Continuous distribution vs binned
  histogram vs both; the canonical summary-statistic set (which quantiles, which spread measure); and whether
  large populations are reduced incrementally/streamed. Freeze at sweep 2 with C46 (principal consumer).
- **OQ-3 (→ review-log): FE-5 — enumerated per-criterion DoD.** **`FE-5 → orchestrator/integrator decision`:**
  ship **holistic-only** (recommended — no C08 change) or commit the **enumerated-per-criterion** path (a
  coordinated C08 + C32 + C33 change). C33's Sweep-1 is the holistic baseline; per-criterion aggregation is a
  clean I2/I3 sweep-2 extension **iff** ruled in. (Mirrors the FE-5 decision the C32 builder also surfaces.)
- **OQ-4 (→ review-log): score model + ensemble collapse (C32 boundary).** The per-trajectory **score scale**
  and how a **multi-judge ensemble** (README:187) collapses to one trajectory score are **C32's** contract;
  C33's normalisation rule (I2) must be frozen against C32's actual output shape at sweep 2 (incl. how judge
  disagreement is represented before reduction).
