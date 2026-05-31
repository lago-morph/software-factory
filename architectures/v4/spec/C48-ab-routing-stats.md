# C48 — A/B routing & statistical comparison  (Spec, canonical track)

> Source: README §"Principle 12 — Self-optimization" (L263–278: the P12 capability table — **L273 "A/B test
> routing | Routes traffic to variants | Unleash, GrowthBook, Flagsmith | MIT / MIT / commercial-with-OSS-core
> | Gas City pack"**; **L275 "Statistical comparison | Was variant better? | scipy.stats, Evidently AI | BSD /
> Apache 2.0 | Python tool node"**; L269 meta-metric row "cost-per-satisfaction, **time-to-threshold**, judge
> false-positive rate"; L276 "Promotion gate | New variant becomes default | Custom: Gas City formula with
> **statistical gate**"; **L278 "P12 is the most ambitious and the most research-flavored. CXDB + DSPy + Optuna
> + scipy + Unleash compose into the layer … Build last"**); README §Phase 3d (**L470 "the A/B routing pack
> (transfusion from Unleash) … This is the highest-risk layer; heaviest human review"**); README license table
> (L320 "scipy / statsmodels | BSD | Clean"; L321 "Evidently AI | Apache 2.0 | Clean"; L322 "Unleash | Apache
> 2.0 | Clean"; L323 GrowthBook MIT; L324 Flagsmith BSD-3); AI-CONTEXT §7 Layer-6 capability table (**L358 "A/B
> routing | Unleash, GrowthBook, Flagsmith, OpenFeature | Apache 2.0/MIT/BSD-3/CNCF spec | Mature for product
> features"**; **L360 "Statistical comparison | scipy.stats, statsmodels, Evidently AI | BSD/BSD/Apache 2.0 |
> Mature"**; **L361 "Multi-armed bandit | Vowpal Wabbit, MABWiser | BSD/Apache 2.0 | Mature narrow domain"**;
> L364 "Regression detection | Evidently AI, NannyML"); AI-CONTEXT §6.5 (**L286 "Layer 6: cost-routing covered;
> A/B + promotion absent"** — the gap C48 fills); AI-CONTEXT §7 L6 prose (L420 "A/B routing: Unleash,
> GrowthBook, OpenFeature"; L421 "Statistical comparison: scipy.stats, Evidently AI"; L422 "Multi-armed bandit:
> Vowpal Wabbit, MABWiser"); AI-CONTEXT §9.1 (Layer-6 transfusion map) + L652 "Unleash: `github.com/Unleash/
> unleash`"; component-inventory C48 row (L60 "Routes traffic between variants (Unleash/bandit) and determines
> whether a variant was actually better (scipy/Evidently)"; maps A69/A71/A72c/B60/B63; **depends C47, C46**; gap
> **G32**; foundational: no; **Batch 5**, L115); per-track inventory A69 (A/B routing pack), A71 (statistical
> comparison "Was variant better?"), **A72c (multi-armed bandit — Vowpal Wabbit/MABWiser)**, B60 (A/B routing),
> B63 (statistical comparison "Determines whether a variant was actually better"); spec/C55 §6 +I4 (C55 **poses**
> a candidate-vs-candidate comparison and **consults C48's significance verdict** — the methodology-significance
> seam); spec/C33 §6/§8 (C33's significance→C48 boundary: "A/B significance testing lives in **C48** … the
> v4-named scipy/Evidently engine, README:275"); F-MODE-COVERAGE §5 (**F47 "Visible-metric drift / Goodhart …
> variant testing measures multiple metrics simultaneously; no single visible target"**; **F60 "Parallel-cycle
> compounding error … A/B harness reports aggregate not single-cycle — Addressed"**) + §10 (F47 "Multi-metric
> mandatory: … promotion gate requires multiple metrics moving together"); ambiguities-and-gaps **G32**
> (major — cost essentially unmodeled); review-log **D-6** (canonical track), **D-19** (methodology significance
> → C48), **D-15** (satisfaction holistic).
> Inventory ID: C48   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C48 is the factory's **A/B routing & statistical-comparison component** — the **two-faced apparatus of
Principle 12 (self-optimization)** that v4 names as a single inventory row (README:273+275; inventory C48). It
does exactly two things, and the seam between them is the point of the component:

1. **Routes traffic between variants (the *router*).** Given a set of candidate variants (C47's prompt/
   hyperparameter variants), C48 **decides which variant serves a given unit of work** — via **feature-flag
   routing (Unleash / GrowthBook / Flagsmith / OpenFeature)** for fixed-split A/B (README:273; AI-CONTEXT:358),
   or via a **multi-armed bandit (MABWiser / Vowpal Wabbit)** for adaptive exploration (AI-CONTEXT:361; A72c).
   This is the "cost-routing covered" half that v4 says already exists in the stack (AI-CONTEXT:286). *(The
   router serves the **C47** live-A/B variant set; C55's methodology candidates are **not** routed by C48 — C55
   runs its own candidates through the eval tier and consults C48 only for the significance verdict; see I4, §2,
   and the C55 boundary below.)*
2. **Determines whether a variant was *actually* better (the *judge of variants*).** Given the per-variant
   outcomes that accrue (C33 satisfaction distributions + C46 meta-metrics), C48 runs the **statistical
   significance test** — **scipy.stats / statsmodels** for the hypothesis test, **Evidently AI** for
   distribution-shift / regression detection (README:275; AI-CONTEXT:360/364; A71/B63) — and emits a **verdict**:
   *did variant B genuinely beat variant A, or is the apparent difference noise?* This is the "A/B + significance
   **absent**" half that v4 says the stack does **not** yet provide for the LLM-factory loop (AI-CONTEXT:286) —
   the gap C48 closes.

C48 serves **P12** precisely because P12's claim is not "ship the variant with the higher mean" — it is
"**determine whether a variant was *actually* better**" (inventory C48; B63). A higher sample mean over n=12
trajectories is not evidence; the **significance determination** is the capability, and it is the load-bearing
*keep*. C48 is **deliberately thin**: every primitive it needs is **mature off-the-shelf OSS** v4 names by
project — Unleash/MABWiser for routing, scipy/Evidently for significance. C48's *custom* surface is only the
**routing-config + significance-determination wiring** and the **verdict contract** that C50 (promotion gate)
and C55 (methodology experiment, per D-19) consume. It builds **no** routing engine and **no** statistics engine.

**Responsibilities (what C48 is the spec-of-record for):**
- **Define & operate the variant-routing decision (I1).** Bind a candidate variant set (from **C47** — the
  live-A/B variant set) to a **routing strategy** — fixed-split feature-flag (Unleash, README:273) or adaptive
  **bandit** (MABWiser, AI-CONTEXT:361; A72c) — and decide, per unit of work, **which variant serves it**. C48
  wraps the OSS router; it owns the *binding + config*, not the flag/bandit algorithm. *(Routing is over C47's
  variants; C55's methodology candidates are run by C55 via the eval tier and only consult C48's verdict — I4.)*
- **Collect per-variant outcomes for comparison (I2).** Read the outcomes that accrue per variant arm — the
  **C33 satisfaction distribution** (the primary outcome — D-15 holistic satisfaction) **and** the **C46
  meta-metrics** (cost-per-satisfaction, time-to-threshold, judge-FP-rate — README:269). C48 does **not**
  compute satisfaction or cost; it **reads** C33/C46 keyed by variant arm.
- **Run the significance determination (I3) — the keep.** Apply the v4-named **scipy.stats / statsmodels**
  hypothesis test (and **Evidently** for distribution-shift / regression) to the two (or k) arms' outcome
  distributions, producing per-metric **effect size + p-value/confidence interval + a significance decision**.
  This is the "was the variant *actually* better" determination (README:275; B63).
- **Emit the comparison verdict (I4) — the contract.** Surface a typed **verdict** — per metric: which arm,
  effect size, significance, sample sizes; and an **overall multi-metric reading** (no single visible target,
  F47) — consumable by **C50** (promotion gate; inventory C50 `depends on C48`) and by **C55** (methodology
  significance, D-19). C48 emits the *verdict*; it does **not** decide promotion (that is C50).
- **Surface cost-aware routing inputs (I5) — G32.** Make the **per-variant cost** that C46 measures a
  **first-class routing input**: a variant's *expense* (tokens/$ per unit, from C46) participates in the routing
  decision (e.g. a bandit reward that is satisfaction-per-dollar, or a flag rule that caps spend on a losing
  arm) and in the verdict (report cost effect alongside satisfaction effect). C48 owns the *wiring* of C46's
  cost signal into routing/comparison; it does **not** own the cost *model* (that is C46 — G32, §6).

**Explicitly NOT (boundaries):**
- **NOT the variant *identifier*.** *What* to experiment with — the prompt variants (DSPy) and hyperparameter
  variants (Optuna/Ray Tune) — is **C47** (README:271–272; inventory C47). C48 *routes among* and *compares* a
  variant set; it never discovers or generates variants. (Inventory C48 `depends on C47`.)
- **NOT the promotion decision / "becomes the default."** Deciding that a winning variant **becomes the new
  default** is the **C50 promotion gate** — "Custom: Gas City formula with statistical gate" (README:276;
  inventory C50 `depends on C48`). C48 supplies the **statistical gate's evidence** (the verdict); C50 owns the
  *policy* (the multi-metric formula, the Goodhart guard, the act of flipping the default). C48 determines
  *better*; C50 decides *promote*.
- **NOT the satisfaction metric or the cost model.** The **satisfaction distribution** per arm is **C33**'s
  (README:188; D-15); the **cost/meta-metrics** are **C46**'s (README:269; inventory C46 owns G32's cost
  model). C48 **consumes** both keyed by variant; it computes neither. (Inventory C48 `depends on C46`.)
- **NOT a custom statistics engine.** The significance machinery is the v4-named **scipy.stats / statsmodels /
  Evidently** stack (README:275/320–321; AI-CONTEXT:360/364), wrapped as a Python tool node — **no bespoke
  estimator, bootstrap, or test**. This is the *home* of significance testing for the self-opt loop (and, per
  D-19, for C55) — but the *test* is off-the-shelf; C48's custom surface is the **wiring + verdict contract**,
  not the math (§6, the-bar note).
- **NOT a custom routing engine.** The router is **Unleash / GrowthBook / Flagsmith** (feature flags,
  README:273) or **MABWiser / Vowpal Wabbit** (bandit, AI-CONTEXT:361) — both mature OSS. C48 owns the
  **strategy binding + config**, not a hand-rolled traffic-splitter or bandit algorithm.
- **NOT the counterfactual-replay driver.** Re-running a variant from a trajectory midpoint (CXDB O(1)
  branching) is **C49** (README:274). C48 compares *outcomes that accrued*; how those outcomes were *generated*
  (live traffic vs. replay) is C49/the harness's concern. *(Related, not a C48 dependency edge — C48 deps are
  C47, C46.)*
- **NOT the experiment registry / meta-metric tracker.** Recording experiments + meta-metrics **over time** is
  **C46 / MLflow** (README:270; AI-CONTEXT:360 "Experiment registry | MLflow"). C48 reads the current outcomes
  to render a verdict; it does not own the longitudinal store.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (variant set) | **C47** Variant identification | Produces the **candidate variants** (DSPy prompt / Optuna hyperparameter) C48 routes among and compares (README:271–272). Inventory C48 `depends on C47`. |
| Upstream (cost / meta-metrics) | **C46** Meta-metric stream | Produces **cost-per-satisfaction / time-to-threshold / judge-FP-rate** per arm; C48 reads these for the comparison **and** for cost-aware routing (G32). **C46 owns the cost *model* (G32); C48 owns the *use* of it.** Inventory C48 `depends on C46`. |
| Upstream (satisfaction) | **C33** Satisfaction metric | The **primary outcome distribution** per arm (holistic satisfaction, D-15). C48 reads it keyed by variant; it does not compute it. C33 routes its own significance question to C48 (C33 §6). *(Via C46/C33 contract; the named outcome input.)* |
| Routing engine | **Unleash / GrowthBook / Flagsmith** (flags) + **MABWiser / Vowpal Wabbit** (bandit) | The mature OSS routers C48 wraps as a Gas City pack (README:273; AI-CONTEXT:358/361). Engine reuse, not custom routing. |
| Significance engine | **scipy.stats / statsmodels** (hypothesis test) + **Evidently AI** (distribution-shift / regression) | The mature OSS significance stack C48 wraps as a Python tool node (README:275; AI-CONTEXT:360/364). Engine reuse, not custom stats. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction, **C03** feature-flag gate | C48 is a **Gas City pack (router) + Python tool node (stats)** (README:273/275), invoked via the tool-node protocol, feature-flag-gated (P12 builds last). *(Related interface, not a dependency edge.)* |
| Downstream (promotion) | **C50** Promotion gate | The **statistical gate** that flips the default; **consumes C48's verdict** as its evidence (README:276; inventory C50 `depends on C48`). C48 determines *better*; C50 decides *promote*. |
| Downstream (methodology significance) | **C55** Methodology-experiment loop | **Consults C48's significance verdict** for "is this methodology candidate actually better" (D-19; spec/C55 §6, I4). C55 poses the comparison; C48 returns the verdict. |

**Position in the system.** C48 is **Batch 5** (component-inventory L115) — the **self-optimization research
frontier, built last**, after Layers 1–5 are solid (README:278/470). It is **feature-flag-gated** (C03): the
factory runs without it; C48 is the apparatus that, *when enabled*, turns a variant set into a *defensible
"this one is actually better" verdict*. It is **not foundational** (inventory C48: foundational = no) — it sits
late in the dependency graph and nothing in Batch 5 is upstream of it except C47/C46. It is the **home of
statistical-significance testing for the whole self-opt loop** (and, per D-19, for C55's methodology
experiment) — the single place the "actually better?" question is answered, so the answer is consistent and
the stats stack is wrapped once.

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete routing-strategy config, the verdict-record schema, the
exact test selection (which scipy test for which outcome shape), and the bandit reward definition defer to
sweep 2 (and bind to C47's variant shape, C46's meta-metric shape, C33's distribution shape, and C50/C55's
verdict-consumer contracts).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Variant-routing decision** | inbound (config) + outbound (route) | Bind a candidate variant set (**C47** — live-A/B variants) to a **routing strategy** — fixed-split **feature flag** (Unleash, README:273) or adaptive **bandit** (MABWiser, AI-CONTEXT:361) — and decide, per unit of work, **which arm serves it**. C48 owns the binding/config + the route call; the flag/bandit **algorithm** is the OSS engine's. *(C55's methodology candidates are not routed here — C55 runs them via the eval tier and consults I4 only.)* | C48 (binding); Unleash/MABWiser (engine) |
| I2 | **Per-variant outcome read** | inbound (data) | Read the outcomes that accrue per arm: the **C33 satisfaction distribution** (primary, D-15) **and** the **C46 meta-metrics** (cost-per-satisfaction, time-to-threshold, judge-FP-rate — README:269), keyed by variant arm + experiment. C48 reads; it computes neither. | C48 (read); **C33/C46** (produce) |
| I3 | **Significance determination** | internal | Apply **scipy.stats / statsmodels** (hypothesis test) + **Evidently** (distribution-shift / regression) to the arms' outcome distributions → per metric: **effect size + p-value/CI + significance decision** ("was the variant *actually* better"). Off-the-shelf engine; C48 owns the *wiring + test selection*, not the math. | C48 (wiring); scipy/Evidently (engine) |
| I4 | **Comparison verdict** | outbound (data) | The component's declared output: per metric — winning arm, effect size, significance (p/CI), sample sizes; plus an **overall multi-metric reading** (no single target, F47); plus the **cost effect** (G32). Consumable by **C50** (promotion gate evidence) and **C55** (methodology significance, D-19). C48 emits the verdict; **C50 decides promotion**. | C48 (this); **C50/C55** (consumers) |
| I5 | **Cost-aware routing input (G32)** | inbound (data) + internal | C46's **per-variant cost** is a first-class routing input: a bandit reward of **satisfaction-per-dollar**, or a flag rule that **caps spend on a losing arm**; and a **cost effect** reported in the verdict (I4). C48 wires C46's cost signal into routing + comparison; **C46 owns the cost *model*** (G32, §6). | C48 (wiring); **C46** (cost model) |
| I6 | **Tool-node / pack lifecycle** | inbound (ops) | Packaged + invoked as a Gas City **router pack** + **Python stats tool node** (C02/C17 ABI); configured via pack TOML (variant set binding, routing strategy, significance test/α, cost-aware policy). **Feature-flag-gated** (C03; P12 builds last). | C02/C17 (ABI); C03 (gate); C48 (config) |

**Invariants C48 must uphold:**
- **INV-1 (significance, not higher-mean — the P12 keep).** C48's verdict asserts a variant is "better" **only**
  when the comparison is **statistically significant** (effect size + p/CI from scipy/Evidently), never on a
  raw higher mean. This is the load-bearing "**determine whether a variant was *actually* better**" property
  (inventory C48; B63; README:275). A non-significant difference is reported as **inconclusive**, not a win.
- **INV-2 (multi-metric — anti-Goodhart, F47).** The verdict is **always over multiple metrics** (satisfaction
  + cost + the C46 set), never a single visible target — so promotion (C50) can require "multiple metrics
  moving together" (F-MODE-COVERAGE:103/174). C48 must surface per-metric verdicts, not collapse to one number.
- **INV-3 (aggregate-rate, not single-cycle — F60).** The comparison is over the **aggregate** outcome
  distribution per arm (the population of trajectories), not a single cycle — the "A/B harness reports
  aggregate not single-cycle" property (F-MODE-COVERAGE:64). Inherits C33's population-honesty: small-n arms
  are legible as small-n (sample sizes always in the verdict).
- **INV-4 (verdict-only — no promotion, no scoring).** C48 renders a **statistical verdict**; it makes **no**
  promotion decision (C50), runs **no** model/judge (C32), and computes **no** satisfaction (C33) or cost (C46).
  It is a pure comparison over given outcomes (deterministic given inputs + test config). Mirrors C33's
  verdict-blind posture one layer up: C33 won't render pass/fail; C48 won't render promote/reject.
- **INV-5 (engine-wrapped — no custom router/stats).** Routing is Unleash/MABWiser; significance is
  scipy/Evidently. C48 owns **binding + config + verdict shape**, never a hand-rolled traffic splitter, bandit,
  or statistical test (the bar — §6).
- **INV-6 (cost is in the loop — G32).** When a cost signal is available from C46, the routing decision and the
  verdict **account for cost** (satisfaction-per-dollar, not satisfaction alone) — so the self-opt loop cannot
  silently promote a marginally-better-but-far-more-expensive variant. If C46's cost model is absent, C48
  degrades to satisfaction-only routing/verdict and **says so** (never fabricates a cost effect). (G32, §6.)

## 4. Data model / state

C48 **owns the routing-binding + verdict contract**, not durable source-of-truth outcome data. The
**satisfaction distribution** is C33's; the **meta-metrics/cost** are C46's; the **variant definitions** are
C47's. State C48 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Experiment / routing binding** | Which **C47** variant set is under test, the **routing strategy** (flag split or bandit), and the arm→variant mapping. The router's live config. *(Routing binds C47 variants; a C55 methodology comparison is posed at the verdict, not routed.)* | Pack TOML (C02/C03) + the OSS router's own store (Unleash/MABWiser state). | C48 (binding); Unleash/MABWiser (engine state) |
| **Bandit arm state (if bandit)** | Per-arm reward statistics the **MABWiser/VW** engine maintains to adapt routing (e.g. satisfaction-per-dollar reward, G32). **Owned by the bandit engine**, not a bespoke C48 store. | Bandit engine state (re-derivable from the C33/C46 outcome history). | MABWiser/VW (engine); C48 (reward def) |
| **Comparison verdict** | The computed per-metric verdict (winning arm, effect size, p/CI, sample sizes) + overall multi-metric reading + cost effect. The component's *output*, re-derivable from C33/C46. | Emitted as tool-node output; optionally recorded (MLflow/bead) for C50/audit — an *optimization*, re-computable (INV-4). | C48 (shape); **C50/C55** (consumers) |
| **Significance config** | The test selection + significance level (α), the multi-metric policy, the cost-aware routing policy (G32). | Pack TOML (C02/C03 model). | C48 (binding) |
| **Outcome inputs (read-only)** | Per-arm **C33 satisfaction distribution** + **C46 meta-metrics/cost** — the populations C48 compares. **Owned by C33/C46**, read-only to C48. | C33/C46 (their stores; C19/CXDB/MLflow). | **C33, C46** |

> [FAITHFUL-FILL] v4 specifies the *behavior* (route via Unleash/bandit; compare via scipy/Evidently —
> README:273/275) but not C48's persisted state. The minimal faithful set is **none that is source-of-truth**:
> the **verdict is a deterministic comparison** over C33/C46 outcomes (re-runnable any time, INV-4), and the
> **routing/bandit state lives in the OSS engine**, not a bespoke C48 store. Persisting a verdict (MLflow/bead)
> is at most an *optimization* for C50/audit, not required state. The exact verdict-record schema (fields, the
> canonical metric set, the test-selection table) is **sweep-2**, frozen with **C50** (the principal verdict
> consumer), **C46** (the cost/meta-metric shape), and **C47** (the variant shape).

**Consistency / lifecycle.** C48 stands up in **Phase 3d / Batch 5** with the rest of P12 (README:470), behind a
feature flag (C03). It owns no durable truth: outcomes survive on C33/C46, routing state in the OSS engine, so
a re-run reproduces the verdict (INV-4). C48 is therefore a **stateless-over-its-own-data comparison** plus a
**thin binding** over the OSS router — which is why the bar keeps it thin (no store, no stats engine, no
router engine; §6).

## 5. Behavior

**Stand up (Phase 3d / Batch 5).** The router pack + stats tool node are installed behind a feature flag (C03).
C48 is configured with the **C47** variant set under test, the routing strategy (flag split or bandit), the
significance test + α, the multi-metric policy (INV-2), and the cost-aware policy (G32, I5). It is wired
downstream of C47/C46/C33 (inputs) and upstream of C50/C55 (verdict consumers). *(C55 supplies no routing
input — it consults C48 for significance over distributions it produced via the eval tier; I4, §2.)*

**Route path (steady state).**
1. **Resolve the arm (I1):** for a unit of work, the **feature flag** (Unleash) returns the assigned arm for a
   fixed split, **or** the **bandit** (MABWiser) selects an arm to balance exploration/exploitation — optionally
   weighted by the **cost-aware reward** (satisfaction-per-dollar, G32/I5/INV-6).
2. **Work runs under the chosen variant**, producing a trajectory scored by the eval tier (C31/C32) into a
   **C33 satisfaction** + **C46 meta-metrics** keyed by the arm. *(C48 does not run the work; it only chose the
   arm — INV-4.)*

**Compare path (on demand / when enough evidence accrued).**
1. **Collect outcomes (I2):** read the per-arm **C33 satisfaction distributions** + **C46 meta-metrics/cost** for
   the experiment.
2. **Test (I3):** apply **scipy.stats/statsmodels** (hypothesis test) + **Evidently** (distribution-shift /
   regression) **per metric** → effect size + p/CI + significance decision (INV-1), across the **multiple
   metrics** (INV-2) over the **aggregate** distributions (INV-3). No model call; no promotion (INV-4).
3. **Emit verdict (I4):** surface per-metric verdicts + overall multi-metric reading + **cost effect** (G32) +
   sample sizes — for **C50** (promotion gate evidence) and **C55** (methodology significance, D-19). A
   non-significant difference is reported **inconclusive**, never a win (INV-1).

**Re-computation.** Because C48 owns no source-of-truth (INV-4), C50 or C55 can request a fresh verdict over a
(possibly enlarged) outcome population at any time; the verdict is a pure function of the current C33/C46
outcomes + config. Adaptive routing (bandit) likewise re-derives from the outcome history.

> The exact route-call + verdict signatures, the canonical metric set + verdict-record schema, the
> **test-selection table** (which scipy/statsmodels test for which outcome shape; when Evidently's
> distribution-shift vs. a point hypothesis test), the **bandit reward definition** (the G32 cost-aware reward),
> and multiple-comparison correction across metrics/arms are **sweep-2+** (frozen with C50 + C46 + C47). C48
> invokes **no** model and rolls **no** statistical test or router of its own.

## 6. Failure modes & handling

C48 owns the **cost-aware-routing gap (G32)** at this component, sits behind the **F47 (Goodhart)** and **F60
(compounding-error)** Layer-6 guards, and is the routed home of significance testing (D-19).

**G32 (major) — cost is essentially unmodeled. ADDRESSED HERE (the *routing/comparison use* of cost; the
*model* is C46's).** G32 flags that the only cost figure in the corpus is "$200/month Max" (AI-CONTEXT:143) yet
P12's headline meta-metric is **cost-per-satisfaction** (README:269) and "cost amortizes across methodologies"
(README:512) is asserted with **no number**. C48 is a principal *consumer* of cost (A/B variant replays are
explicitly called out in G32 as an unmodeled cost driver), so it must take a faithful stance:
- **What C48 owns — cost as a first-class routing/comparison input (RESOLVED for C48's scope).** C48 makes the
  per-variant cost C46 measures a **first-class signal** in both the **routing decision** (a bandit reward of
  **satisfaction-per-dollar**, or a flag rule that caps spend on a losing arm — I5/INV-6) **and** the **verdict**
  (a **cost effect** reported alongside the satisfaction effect — I4). This is the smallest faithful reading
  that honors P12's "cost-per-satisfaction" headline: the self-opt loop must not promote a marginally-better
  but far-more-expensive variant, and routing must not burn the single $200/month seat exploring a losing arm.
  The A/B-replay cost driver G32 names is thereby made **visible and actionable** at C48.
- **What C48 does NOT own — the cost *model* itself.**
  > [AMBIGUITY: G32] v4 names "cost-per-satisfaction" (README:269) but **defines no cost model** — no token/$
  > accounting for scenario-suite runs, multi-judge ensembles, A/B replays, or second-family judge tokens
  > (G32). Two readings: **(a)** C48 builds its own cost accounting to drive routing; **(b)** the cost *model*
  > is **C46**'s (inventory C46 row explicitly: "needs a defined cost model"; C46 carries G32 too), and C48
  > merely **consumes** C46's cost signal. **Chosen: (b)** — it is the reading most consistent with v4: C46 is
  > the **meta-metric stream** that owns cost-per-satisfaction (README:269) and is the inventory home of the
  > cost model (C46 row + G32 on C46); duplicating cost accounting in C48 would split the model across two
  > components and violate the bar. So **C48 wires C46's cost signal into routing + verdict (G32 *use* resolved
  > here)**; the **cost-model *definition* is C46's shared G32 obligation** (named, deferred to C46). If C46's
  > cost model is absent, C48 **degrades to satisfaction-only** routing/verdict and **declares the cost
  > dimension unavailable** (INV-6) — it never fabricates a cost effect. (OQ-1 carries the C46↔C48 cost-signal
  > contract freeze.)

**F47 (Goodhart / visible-metric drift) — multi-metric mandatory (INV-2).** P12's meta-metric layer creates
explicit visible metrics; Goodhart applies (F-MODE-COVERAGE:63/103). C48's guard: the verdict is **always over
multiple metrics** (satisfaction + cost + the C46 set), **no single visible target** — so C50's promotion gate
can "require multiple metrics moving together" (F-MODE-COVERAGE:174). C48 *surfaces* the multi-metric verdict;
the **promotion policy** that enforces "moving together" is **C50**'s (boundary). *Status per v4: Partial —
Goodhart applies recursively to meta-metrics (F-MODE-COVERAGE:63); C48 does not claim to fully close F47.*

**F60 (parallel-cycle compounding error) — aggregate-rate (INV-3).** C48 compares the **aggregate** outcome
distribution per arm, not a single cycle — the "A/B harness reports **aggregate not single-cycle**" mechanism
v4 marks **Addressed** (F-MODE-COVERAGE:64). The aggregate-rate framing (1−(1−p)ⁿ) is C46's meta-metric set;
C48 inherits it by comparing populations, not points (INV-3).

**Other failure cases.**
- **Insufficient / unequal sample across arms (I2).** If arms were measured over too few or **unequal** runs,
  C48 returns an **inconclusive** verdict with sample sizes surfaced (INV-1/INV-3) — never a win on thin/uneven
  evidence; re-run when more accrues. *[FAITHFUL-FILL]: inherits C33 INV-4 population-honesty; minimal.*
- **Unfair comparison (different scenarios/judge across arms).** Variants compared on **different** held-out
  C30 scenarios or a different judge are **not comparable**; C48's verdict is only valid over a **fair**
  comparison (same scenarios/judge — the C55 INV-2 / README:31 guarantee). C48 *relies on* the orchestrator
  (C55 / the experiment driver) for fairness; it does **not** itself enforce scenario isolation (that is
  C30/C34/C42). *(Boundary, not a C48 mechanism.)*
- **Multiple-comparison inflation (k arms / many metrics).** Testing many arms × many metrics inflates
  false-positives; C48 must apply a **correction** (the named statsmodels/scipy multiple-comparison facility) —
  *which* correction is a **sweep-2** test-selection choice (OQ-2), but the *requirement* is noted now so the
  multi-metric verdict (INV-2) is not itself a Goodhart hole.
- **Routing engine unavailable / variant arm errors mid-experiment.** If the OSS router is down, C48 fails
  **closed to the current default** (no experiment routing rather than misrouting); an arm that errors
  mid-experiment is recorded **failed-to-evaluate** and **excluded** from the comparison (not read as low
  satisfaction). *[FAITHFUL-FILL]: minimal fail-safe; mirrors C55's failed-candidate exclusion.*

> F-mode applicability is owned by **C57** (coverage map). C48 underwrites the Layer-6 self-opt guards —
> **F47** (multi-metric variant testing, no single target) and **F60** (aggregate-rate A/B reporting) — and is
> the mechanism behind v4's "**A/B + promotion absent → now present**" closure (AI-CONTEXT:286). C48 defers the
> canonical F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C48 is held to *only* the P12-tied capability — **route
traffic between variants** (Unleash/bandit) **+ determine whether a variant was *actually* better**
(significance, not a higher mean) **+ the verdict contract** C50/C55 consume — plus the low-effort wiring that
binds the OSS engines. **Dropped / refused as non-principle or already-in-the-stack:** (1) any **custom
statistics engine** — the significance test is the v4-named **scipy.stats / statsmodels / Evidently** stack
(README:275/320–321), not a bespoke estimator/bootstrap/test (C48 adds only test-selection + wiring); (2) any
**custom routing engine** — feature-flag routing is **Unleash/GrowthBook/Flagsmith** and adaptive routing is
**MABWiser/Vowpal Wabbit** (README:273; AI-CONTEXT:361), not a hand-rolled splitter/bandit; (3) the
**promotion decision** ("becomes the default") — that is the **C50** Gas City formula + statistical gate
(README:276); C48 supplies evidence, not the policy; (4) a **bespoke cost *model*** — that is **C46**'s (G32 on
C46); C48 only *uses* C46's cost signal (G32 reading (b)); (5) the **counterfactual-replay driver** (C49) and
the **experiment/meta-metric registry** (C46/MLflow). What is **kept**: the **significance-determination wiring**
(the genuine P12 "actually better" capability), the **routing-strategy binding** (incl. the bandit + the G32
cost-aware reward), and the **verdict contract** — the load-bearing seam C50 and C55 contract against.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C48 reads **outcome statistics about** variants (C33 distributions, C46 meta-metrics) — not raw
  prompts/outputs — so it inherits C33/C46's access posture and adds little exposure. It performs **no** model
  call (no judge/coder credential). The router (Unleash) carries the live arm-assignment config; standard
  feature-flag access controls apply (inherited from the OSS engine, not re-invented).
- **Cost.** C48 is itself cheap — a flag lookup / bandit update + a scipy comparison over beads; **no model
  tokens**. But C48 is the component that makes the *factory's* self-opt cost **legible and bounded**: it is the
  enforcement point where the **G32 cost-aware routing** keeps A/B experimentation from over-spending the single
  $200/month Max seat (AI-CONTEXT:143) on losing arms — the cost-per-satisfaction headline (README:269) made
  operational. The cost *model* it consumes is C46's.
- **Scale.** Comparison cost is linear in arm/sample size and trivially handled by scipy; the bandit's update is
  O(arms). The only honest scale note: many concurrent experiments × arms × metrics multiply the comparison and
  the multiple-comparison-correction surface — a sweep-2 concern (OQ-2), not a Sweep-1 design force. No bespoke
  scaling machinery is warranted (the bar).
- **Observability.** C48 *is* a decision-support component — the verdict is a headline P12 signal. Its own
  health (experiments running, arm allocations, last-verdict per experiment, inconclusive-rate, excluded arms)
  is worth emitting for auditability, especially since P12 is "heaviest human review" (README:470). The verdict
  itself should be auditable evidence for C50's gate.
- **Ops.** Pack-delivered router + Python stats tool node, operated **behind a feature flag** with the rest of
  P12 in Phase 3d (README:470), **built last** (README:278). **Pin** scipy/statsmodels/Evidently and the router
  versions so the significance contract + routing behavior are reproducible (inherits the version-pin
  discipline). Heaviest human review applies (README:470) — the verdict is advisory evidence to a human-reviewed
  C50 gate, not an autonomous promote.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (significance, not higher-mean — INV-1, the P12 keep):** given two arms' outcome distributions, C48's
   verdict declares "better" **only** when the comparison is statistically significant (effect size + p/CI); a
   non-significant difference yields **inconclusive**, never a win (README:275; B63).
2. **AC-2 (routes between variants — I1):** C48 routes a unit of work to a variant arm via **feature flag**
   (Unleash) for a fixed split **or** via a **bandit** (MABWiser) for adaptive exploration (README:273;
   AI-CONTEXT:361).
3. **AC-3 (multi-metric — INV-2, F47):** the verdict is over **multiple metrics** (satisfaction + cost + the
   C46 set), never a single visible target — supporting C50's "multiple metrics moving together"
   (F-MODE-COVERAGE:174).
4. **AC-4 (aggregate-rate — INV-3, F60):** the comparison is over the **aggregate** per-arm distribution with
   **sample sizes surfaced**, not a single cycle (F-MODE-COVERAGE:64); small-/unequal-n yields **inconclusive**,
   not a win.
5. **AC-5 (verdict-only, no promotion — INV-4):** C48 emits a **verdict** and makes **no** promotion decision
   (that is C50), **no** model call, and computes **no** satisfaction/cost. (Verifiable: C50 consumes the
   verdict; C48 runs with no judge provider configured.)
6. **AC-6 (cost-aware — G32, INV-6):** C48 makes C46's **per-variant cost** a routing input (satisfaction-per-
   dollar / spend cap) **and** reports a **cost effect** in the verdict; with C46's cost model **absent**, it
   degrades to satisfaction-only and **declares cost unavailable** (no fabricated cost effect).
7. **AC-7 (engine-reuse, no custom router/stats — the bar, INV-5):** routing is **Unleash/MABWiser**;
   significance is **scipy/statsmodels/Evidently** (README:273/275); **no** bespoke splitter, bandit, or
   statistical test is present.
8. **AC-8 (consumable downstream — I4):** the verdict (per-metric significance + sample sizes + cost effect +
   overall reading) is consumable by **C50** (promotion gate evidence; inventory C50 `depends on C48`) and
   **C55** (methodology significance; D-19, spec/C55 §6).
9. **AC-9 (re-derivable — INV-4):** the same outcome population + config re-computes the **same** verdict (C48
   owns no source-of-truth; routing/bandit state lives in the OSS engine, re-derivable from the C33/C46 history).

**Test strategy.** An **A/B-comparison pack** that (a) seeds two+ synthetic variant arms with controlled C33
satisfaction + C46 cost distributions (including a *no-real-difference* pair, a *significant* pair, an
*unequal-/small-n* pair, and a *better-but-pricier* pair) and drives AC-1…AC-9 — in particular that a
no-difference pair returns **inconclusive** (AC-1), that the verdict is **multi-metric** (AC-3) and
**aggregate** with n surfaced (AC-4), that the **cost-aware** path flips a marginal winner that is far pricier
(AC-6), and that routing + stats are the **off-the-shelf** engines (AC-7); plus (b) a routing test that a
bandit shifts allocation toward the higher satisfaction-per-dollar arm. This suite **must pass before C50
consumes the verdict for promotion** and **before C55 consults C48 for methodology significance** (D-19), since
both treat C48's verdict as the canonical "actually better" answer.

## 9. Open questions

- **OQ-1 (→ review-log, top): G32 — the C46↔C48 cost-signal contract + cost model.** §6 binds C48 to
  reading C46's cost signal (G32 reading (b)) and to degrading-with-declaration when it is absent (INV-6).
  Confirm the **cost *model* is C46's** shared-G32 obligation (not C48's), and freeze the **per-variant
  cost-signal shape** (token/$ per unit, attributable to an arm) C48 consumes for routing + the verdict — the
  A/B-replay cost driver G32 calls out — at sweep-2 with C46. (The "$200/month" seat budget, AI-CONTEXT:143, is
  the only number v4 gives; the per-experiment cost is otherwise unmodeled.)
- **OQ-2 (→ review-log): test selection + multiple-comparison correction.** Which **scipy/statsmodels** test
  for which outcome shape (continuous satisfaction vs. rate vs. distribution-shift via **Evidently**), the
  **significance level (α)**, and the **multiple-comparison correction** across k arms × multiple metrics (so
  INV-2's multi-metric verdict is not itself a Goodhart hole). Freeze at sweep-2 with C50 (verdict consumer) +
  C33 (distribution shape).
- **OQ-3 (→ review-log): routing strategy default + the bandit reward (G32).** When to use **fixed-split flags
  (Unleash)** vs. an **adaptive bandit (MABWiser)**, and — for the bandit — the precise **reward definition**
  (satisfaction-per-dollar vs. satisfaction with a spend cap; how C46's cost enters the reward). The
  exploration/exploitation policy on a single $200/month seat is cost-sensitive (G32). Freeze at sweep-2.
- **OQ-4 (→ review-log): the C48→C50 verdict contract + the C55 consultation seam (D-19).** Freeze the exact
  **verdict record** C50 consumes for its statistical gate (what C50 needs to decide "promote": per-metric
  significance + effect + the multi-metric reading) **and** the **C55→C48** consultation contract (what
  comparison C55 poses; what verdict C48 returns — D-19, spec/C55 OQ-4) at sweep-2 when C50 is authored. C48 is
  the *home* of significance for both; the consumer-facing shape must satisfy both C50 and C55.
