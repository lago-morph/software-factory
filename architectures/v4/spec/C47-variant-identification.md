# C47 — Variant Identification  (Spec, canonical track)

> Source: README §"Principle 12 — Self-optimization" (line 264 heading; line 266 "The system measures its
> own meta-performance and improves it over time"; line 271 table row "**Variant identification (prompt) |
> Identifies what to experiment with | DSPy compilers | MIT | Python tool node**"; line 272 "**Variant
> identification (hyperparameter) | Optimization over configuration | Optuna, Ray Tune | MIT / Apache 2.0 |
> Python tool node**"; line 278 "CXDB + DSPy + Optuna + scipy + Unleash compose into the layer … Build last,
> after Layers 1-5 are solid"; line 470 Phase 3d "**factory builds … the variant identification pack
> (transfusion from DSPy)** … This is the highest-risk layer; heaviest human review"; line 499
> "Self-optimization's scenarios verify that variant selection actually picks winners"); AI-CONTEXT §"Layer 6
> — self-optimization (P12)" (line 354 "**Manual variant identification | Git branches + tags | n/a |
> Trivial**"; line 355 "**Auto variant — prompt-program | DSPy | MIT | Mature in narrow domain**"; line 356
> "**Auto variant — hyperparameter | Optuna, Ray Tune | MIT/Apache 2.0 | Mature generic**"; line 357 "**Auto
> variant — methodology/topology | None | DIY | Research frontier**"), §9.1 Layer-6 transfusion map (line 418
> "Prompt optimization: **DSPy compilers (Bootstrap, BootstrapFewShot, MIPRO)**, Anthropic prompt-improver
> patterns"; line 419 "Hyperparameter search: **Optuna, Ray Tune**"), §8 multi-capability (line 377 "**DSPy |
> L6 variant identification + L6 statistical comparison (prompt-programs) | MIT**"), §15 repos (line 642
> "DSPy: `github.com/stanfordnlp/dspy`"; line 643 "Optuna: `github.com/optuna/optuna`"); README §"Part 5 —
> License hygiene" (line 315 "DSPy | MIT | Clean"; line 316 "Optuna | MIT | Clean"; line 317 "Ray Tune |
> Apache 2.0 | Clean"); component-inventory C47 row (line 59 "Identifies prompt (DSPy) + hyperparameter
> (Optuna/Ray Tune) variants to experiment with"; maps A67/A68/B64; depends **C46**; gap **—**; foundational
> no) + Batch-5 note (line 115 "Self-optimization … built last … Meta-metrics, variant ID, A/B + stats");
> component-inventory-B B64 (line 76 "Variant identification (prompt + hyperparameter) … **Up: meta-metrics
> (B12). Down: A/B routing (B60)**"); F-MODE-COVERAGE §5 "F-modes addressed by Layer 6 (P12)" (line 63 F47
> Goodhart Partial; line 64 F60 parallel-cycle Addressed) + §"cross-cutting" F47 (line 103
> "**Multi-metric mandatory** … promotion gate requires multiple metrics moving together"), F52 caution
> (line 100 the Layer-6 "more controller patches" trap); spec/C55 §1/§2 (the C47/C48/C50 boundary it names:
> "open-ended prompt/hyperparameter variant *discovery* (DSPy/Optuna) is **C47**"); review-log D-6 (canonical
> track), D-19 (significance testing → C48).
> Inventory ID: C47   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C47 is the factory's **variant identifier**: a **Python tool node** (README:271–272) that, informed by the
**C46 meta-metric stream**, **proposes the candidate variants the self-optimization loop should experiment
with** — both **prompt variants** (via **DSPy** compilers) and **hyperparameter / configuration variants**
(via **Optuna / Ray Tune**). It sits at the **front of Principle 12** ("the system measures its own
meta-performance and improves it over time", README:266): C46 says *how the factory is currently performing*
(cost-per-satisfaction, time-to-threshold, judge-FP-rate over time); C47 turns that signal into a concrete,
bounded **set of candidate variants worth trying**; C48 then A/B-routes + statistically compares them and C50
promotes a winner to default. C47 answers exactly one question: **"given how we're doing, what should we
experiment with next?"** — and emits a typed **variant set** for C48.

C47 is **deliberately thin and almost entirely off-the-shelf**. The two capabilities it needs already exist in
mature, permissively-licensed libraries that v4 names explicitly: **prompt-program optimization is DSPy**
(MIT, "Mature in narrow domain", AI-CONTEXT:355; compilers Bootstrap/BootstrapFewShot/MIPRO, AI-CONTEXT:418)
and **hyperparameter search is Optuna / Ray Tune** (MIT / Apache-2.0, "Mature generic", AI-CONTEXT:356,419).
C47 introduces **no bespoke optimizer and no bespoke search algorithm**. Its *genuine*, load-bearing custom
surface is **the wiring**: (a) **defining the factory's variant space** — *which* prompt programs and *which*
hyperparameters/config knobs are candidates for optimization, and how the optimizable surface is expressed to
DSPy/Optuna; (b) **feeding that search the C46 meta-metric signal** as the objective/prior (what "better"
points at); and (c) **emitting the resulting candidate variants as a typed set handed to C48** (B64 "Down:
A/B routing").

**Responsibilities (what C47 is the spec-of-record for):**
- **Read the meta-metric signal (I1).** Consume the **C46 meta-metric stream** (cost-per-satisfaction,
  time-to-threshold, judge-FP-rate over time; inventory C46) as the input that *informs* which variants are
  worth proposing — the optimization objective / prior the search is pointed at. C46 is C47's sole declared
  dependency (inventory C47 `depends on C46`; B64 "Up: meta-metrics").
- **Define the variant space (I2).** Own the **declaration of what is optimizable**: which **prompt programs**
  (the DSPy-compilable templates / signatures) and which **hyperparameters / config knobs** (the Optuna/Ray
  Tune search space) the factory may vary. This is **pack configuration + a thin binding**, not a search
  algorithm — the search space is *named here*, the search is *run by the library*.
- **Run off-the-shelf variant search (I3).** Drive **DSPy** compilers over the prompt space and **Optuna / Ray
  Tune** over the hyperparameter space, with the **C46 signal as the objective**, to produce candidate
  variants. C47 **configures + invokes** these engines; it **implements neither**.
- **Emit the candidate variant set (I4).** Produce a typed **variant set** — each entry being a concrete,
  testable change (a prompt-program variant and/or a hyperparameter-config variant) with its provenance back
  to the search that proposed it — **handed to C48** (A/B routing + statistical comparison, B64 "Down: A/B
  routing"). This is C47's load-bearing output: the hand-off that opens the experiment.
- **Run as a pack tool node (I5).** Packaged + invoked per the pack / tool-node ABI (C02/C17) as a **Python**
  tool node (README:271–272), feature-gated with the self-optimization pack in Phase 3d (README:470).

**Explicitly NOT (boundaries):**
- **NOT a custom optimizer / search algorithm.** Prompt optimization is **DSPy**; hyperparameter search is
  **Optuna / Ray Tune** (AI-CONTEXT:355–356,418–419). C47 introduces **no novel prompt-optimization method, no
  bespoke hyperparameter search, no hand-rolled Bayesian/bandit/evolutionary optimizer**. Per the bar, that
  capability already exists in the named stack; any reimplementation is **DROPPED** (§6). C47's custom surface
  is *variant-space definition + objective wiring + the C48 hand-off*, nothing more.
- **NOT A/B traffic routing.** Routing live traffic between variants (Unleash / GrowthBook / Flagsmith,
  README:273) is **C48** (inventory C48 "Routes traffic between variants"). C47 *proposes* variants; it does
  **not** route to them.
- **NOT the statistical-comparison / "was it better?" engine.** Deciding whether a variant is *actually
  better* (scipy.stats / Evidently, README:275) is **C48** (inventory C48 "determines whether a variant was
  actually better"; review-log **D-19** routes all self-optimization significance to C48). C47 *poses*
  candidates; the **significance verdict is C48's**. C47 builds **no** p-value / CI / regression machinery.
- **NOT the promotion gate.** Deciding a variant *becomes the default* — the statistical, **multi-metric**
  gate that guards Goodhart (README:276; F47 "multi-metric mandatory", F-MODE-COVERAGE:103) — is **C50**
  (inventory C50). C47 neither promotes nor demotes; it only proposes.
- **NOT the counterfactual-replay driver.** Re-running a trajectory from a midpoint to *test* a variant via
  CXDB O(1) branching (README:274; "your most significant invention", largely unsolved, G19) is **C49**. C47
  identifies *what* to test; **how a variant is executed/replayed** is C49/C48's substrate, not C47's.
- **NOT meta-metric definition or tracking.** *What "better" means* and the **recording** of meta-metrics over
  time (MLflow / Aim, README:269–270) is **C46** (inventory C46; "needs a defined cost model"). C47 **reads**
  C46's signal as its objective; it does **not** define or store the meta-metric. ("What better means is a
  values question", B12.)
- **NOT methodology / topology variant search.** v4 marks **"Auto variant — methodology/topology | None | DIY
  | Research frontier"** (AI-CONTEXT:357) — explicitly *no* turnkey tool and *out of scope* for the named
  stack. C47 covers only the two **mature** auto-variant rows (prompt = DSPy, hyperparameter = Optuna/Ray
  Tune). Methodology-as-config experiments (running v3's candidate pipeline files and selecting per work-type)
  are **C55** (inventory C55; spec/C55 names "the general self-optimization / variant-search loop … prompt/
  hyperparameter variant *discovery* (DSPy/Optuna) is C47"). C47 does **not** search the methodology/topology
  space — that is the unsolved research frontier, deliberately excluded.
- **NOT manual variant identification.** The **trivial** baseline — git branches + tags (AI-CONTEXT:354) —
  needs no component. C47 is the **automated** identifier (the DSPy/Optuna rows); it does not re-implement, nor
  preclude, the manual git-branch workflow.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (sole dep) | **C46** Meta-metric stream | The meta-performance signal (cost-per-satisfaction, time-to-threshold, judge-FP-rate over time) C47 **reads** as the optimization objective / prior — "given how we're doing, what to try next". Inventory C47 `depends on C46`; B64 "**Up: meta-metrics (B12)**". *(C46's cost model is itself open — G09/G32 at C46 — so C47's objective is only as well-defined as C46's metric; §6, OQ-1.)* |
| External (prompt-variant engine) | **DSPy** (`github.com/stanfordnlp/dspy`, MIT) | The v4-named prompt-program optimizer C47 wraps — compilers **Bootstrap / BootstrapFewShot / MIPRO** (AI-CONTEXT:355,418; README:271). "Mature in narrow domain." Engine reuse — **not** custom code. |
| External (hyperparameter engine) | **Optuna** (`github.com/optuna/optuna`, MIT) **/ Ray Tune** (Apache-2.0) | The v4-named hyperparameter / config search engines C47 wraps (AI-CONTEXT:356,419; README:272). "Mature generic." Engine reuse — **not** custom code. |
| Downstream (consumer) | **C48** A/B routing & statistical comparison | Consumes C47's **variant set**: routes traffic between the proposed variants and runs the significance test (inventory C48; B64 "**Down: A/B routing (B60)**"; D-19 significance → C48). C47's variant-set contract (I4) is the hand-off; whether C47's set also carries the *experiment design* C48 routes, or only the candidate list, is the C47↔C48 seam — **OQ-2**. |
| Downstream (via C48 → C50) | **C50** Promotion gate | Reached **through** C48: a proposed variant only becomes default after C48 compares and C50's multi-metric gate (F47) approves. C47 reaches C50 transitively, not directly. |
| Sibling (variant execution substrate) | **C49** Counterfactual replay | The CXDB-branching driver that *executes/replays* variant tests (README:274; G19). C47 names *what* to test; C49 is *how* a variant test runs. Related substrate, not a C47 dependency edge. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C47 is a **Python** tool node in a Gas City pack (README:271–272), invoked via the tool-node protocol. *(Related interface, not a dependency edge; mirrors how C36/C55 name C02/C17.)* |

**Position in the system.** C47 is **Batch-5** (component-inventory line 115; "Self-optimization (research
frontier, built last)"), built in **Phase 3d** as part of the highest-risk, heaviest-human-review layer
(README:470). It is **not foundational** (inventory C47: Foundational? = no) — nothing upstream contracts
against it; it is a mid-pipeline producer that reads C46 and feeds C48. It is **feature-flag-gated** with the
self-optimization pack: it exists only when **P12** is enabled, and only once **Layers 1–5 are solid**
(README:278 "Build last, after Layers 1-5 are solid") and the **C46 meta-metric stream is standing** (its sole
input). Within the self-optimization batch the canonical chain is **C46 → C47 → C48 → C50** (with C49 as the
replay substrate C48 uses), and C47 owns the first transform: *signal → candidate variants*.

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete signatures / the variant-space schema / the variant-set
record shape / the C46-read wire / the DSPy/Optuna invocation surface defer to sweep 2 (frozen with C46 as the
input and C48 as the consumer).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Meta-metric read** | inbound (read) | Read the **C46 meta-metric stream** (cost-per-satisfaction, time-to-threshold, judge-FP-rate over time) as the optimization objective / prior that informs which variants to propose. C46 owns the metric + its store; C47 reads it. | C47 (this); **C46** (source) |
| I2 | **Variant-space declaration** | input (config) | The factory's **optimizable surface**: which **prompt programs** (DSPy-compilable templates/signatures) and which **hyperparameters / config knobs** (the Optuna/Ray Tune search space) may be varied — **pack TOML + a thin binding**, not code. Defines *what can vary*; the search over it is the engine's. | C02/C03 (model); C47 (binding) |
| I3 | **Off-the-shelf variant search** | internal | Drive **DSPy** compilers over the prompt space and **Optuna / Ray Tune** over the hyperparameter space, with the **C46 signal as the objective**, to produce candidate variants. C47 **configures + invokes**; **no custom optimizer** (the bar). | C47 (this); **DSPy / Optuna / Ray Tune** (engines) |
| I4 | **Variant set (hand-off to C48)** | outbound (data) | Emit a typed **variant set**: each entry a concrete, testable change (prompt-program variant and/or hyperparameter-config variant) + provenance back to the search that proposed it. The hand-off **C48** routes + compares (B64 "Down: A/B routing"). C47's load-bearing custom surface. *(Whether the set also carries an experiment design C48 routes, or only the candidate list, is OQ-2.)* | C47 (this); **C48** (consumer) |
| I5 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as a **Python** Gas City tool node (C02/C17 ABI); configured via pack TOML; operated with the self-optimization pack in Phase 3d (README:271–272,470). | C02/C17 (ABI); C47 (config) |

**Invariants C47 must uphold:**
- **INV-1 (off-the-shelf search — the bar).** Variant search is **DSPy** (prompt) + **Optuna / Ray Tune**
  (hyperparameter) (AI-CONTEXT:355–356,418–419). C47 contains **no bespoke optimizer and no bespoke search
  algorithm**; the custom surface is *only* variant-space definition + objective wiring + the C48 hand-off.
  This is the load-bearing "keep-minimal" property (§6).
- **INV-2 (propose-only — no route, no compare, no promote).** C47 emits *candidate variants*; it renders
  **no A/B routing (C48), no significance verdict (C48, D-19), and no promotion decision (C50)**. It is a pure
  proposer + hand-off. (It does not even *run* the experiment — execution/replay is C48/C49.)
- **INV-3 (every variant is concrete + testable + attributed).** Each emitted variant is a **concrete,
  applyable change** (a specific prompt program and/or a specific config assignment), carries **provenance**
  back to the search/objective that proposed it, and is **testable by C48** without C47 re-deriving it. A
  variant C48 cannot route + compare is of no use.
- **INV-4 (objective is C46's signal — does not invent "better").** The optimization target C47 points the
  search at is **the C46 meta-metric** (INV reads C46, does not define it). C47 **does not** decide *what
  better means* (that is C46's values question, B12) nor whether a result *is* better (C48). It only
  *searches toward* C46's signal.
- **INV-5 (multi-metric-aware, Goodhart discipline — F47).** Because the self-optimization layer creates
  explicit visible metrics, **Goodhart applies** and v4 mandates **multi-metric, no single visible target**
  (F47, F-MODE-COVERAGE:103). C47 must propose variants **against C46's multi-metric signal, never a single
  optimized number**, so the eventual gate (C50) can require *multiple metrics moving together*. C47 does not
  *enforce* the gate (C50 does), but it must not collapse the objective to one metric — the upstream half of
  the F47 discipline. *(Relatedly, F52, F-MODE-COVERAGE:100, warns the self-optimization layer is prone to
  "more controller patches" / discipline-without-purpose; C47's answer is INV-3 — every variant is a concrete
  hypothesis C48 can falsify, no variant proposed without a testable change.)*
- **INV-6 (read-side proposer, owns no source-of-truth).** C47 **reads** C46 and **emits** a variant set; the
  meta-metrics live in C46, the experiment/routing state lives in C48, the promoted-default config lives
  downstream (C50). C47 holds **no durable store of its own** beyond transient search state (re-derivable by
  re-running the search over the same C46 signal + variant-space declaration).

## 4. Data model / state

C47 **owns the variant-space declaration + the variant-set contract**, not durable source-of-truth data. The
**meta-metric signal** is C46's; the **experiment/routing/promotion state** is C48/C50's. State C47 is the
spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Variant set** | The emitted hand-off: a list of concrete candidate variants (prompt-program and/or hyperparameter-config changes) + provenance back to the search/objective. The component's *output*, consumed by C48 (I4). | Emitted as a typed record / event handed to C48 (a candidate C20 bead type or a C23 event — **OQ-2**, parity with the C36 carrier question); re-derivable by re-running the search. | C47 (shape); **C48** (consumer); **C20** (iff bead-typed) |
| **Variant-space declaration** | What is optimizable: the prompt programs (DSPy-compilable) + the hyperparameter / config search space (Optuna/Ray Tune). | Pack TOML + thin binding (C02/C03 model). | C02/C03 (model); C47 (binding) |
| **Search state** | DSPy compile state / Optuna study / Ray Tune trials the engine maintains while searching. Owned by the **engine**, not custom; re-derivable from the C46 signal + the variant-space declaration. | Engine-managed (in-pack / engine store, e.g. an Optuna study); re-runnable. | **DSPy / Optuna / Ray Tune** (engine); C47 (lifecycle) |
| **Meta-metric signal (read-only input)** | The C46 meta-metric stream C47 reads as its objective. **Owned by C46**, read-only to C47. | C46's store (MLflow/Aim, README:270). | **C46** (source) |

> [FAITHFUL-FILL] v4 names the *capability* ("variant identification … DSPy / Optuna / Ray Tune … Identifies
> what to experiment with", README:271–272; AI-CONTEXT:355–356) but not C47's persisted state. The minimal
> faithful set is **none that is source-of-truth**: the search state is the engine's (re-runnable), and the
> variant set is a derived record re-computable by re-running the search over the same C46 signal +
> variant-space declaration. So C47 holds no independent store. The exact **variant-space schema**, the
> **variant-set record shape**, and **whether the variant set is a C20 bead type or a C23 event** are
> **sweep-2** (frozen with C46 as input and C48 as the principal consumer — OQ-2).

**Consistency / lifecycle.** C47 stands up in **Phase 3d** with the self-optimization pack (README:470), once
**Layers 1–5 are solid** (README:278) and the **C46 meta-metric stream** is standing. It owns no durable
truth: the **meta-metrics** survive in C46, the **experiment state** in C48 — so a re-run of C47 over the same
C46 signal + variant-space re-derives an equivalent variant set (modulo the engines' own stochasticity, which
is itself re-runnable / seedable). C47 is therefore a **stateless-by-design proposer** — exactly what "wrap
DSPy/Optuna + emit a candidate set" implies, which is why the bar keeps it thin (no store, no custom
optimizer; §6).

## 5. Behavior

**Stand up (Phase 3d).** The self-optimization pack is installed; the Python tool node is configured with the
**variant-space declaration** (which prompt programs are DSPy-compilable; which hyperparameters/config knobs
form the Optuna/Ray Tune search space), the **C46 read seam** (the meta-metric objective), and the
**variant-set sink** (C48). It is wired downstream of C46 and upstream of C48.

**Propose path (steady state).**
1. **Read the meta-metric signal (I1):** pull the current C46 meta-metric stream (cost-per-satisfaction,
   time-to-threshold, judge-FP-rate) — the objective / prior the search optimizes toward (INV-4).
2. **Search the variant space (I3):** drive **DSPy** compilers over the declared prompt programs and/or
   **Optuna / Ray Tune** over the declared hyperparameter space, with the C46 signal as the objective, to
   produce candidate variants. No bespoke optimizer (INV-1); the objective stays **multi-metric** (INV-5,
   F47).
3. **Assemble the variant set (I4):** collect the engines' candidates into a typed variant set — each entry a
   concrete, applyable change (prompt-program and/or config) + provenance back to the search that proposed it
   (INV-3).
4. **Emit to C48 (I4):** hand the variant set to the A/B-routing + comparison stage (C48). C47 does **not**
   route, run, replay, compare, or promote (INV-2) — it stops at the hand-off.
5. **No worthwhile variant → nothing downstream:** if the search yields no candidate worth experimenting with
   (e.g. the objective is already at a local optimum, or the C46 signal is too thin to optimize against), C47
   emits an **empty / no-op variant set** rather than a fabricated change — the loop is driven by *real*
   candidate variants, not a constant drip (parity with C36's clean-window → no-signal discipline).

**Re-computation.** Because C47 owns no source-of-truth (INV-6), the same C46 signal + variant-space
re-searched yields an equivalent variant set (engine stochasticity is re-runnable / seedable). There is no
checkpoint to recover and nothing load-bearing to lose on restart — a restarted C47 re-reads C46 and re-runs
the search.

> The exact DSPy compiler selection (Bootstrap / BootstrapFewShot / MIPRO, AI-CONTEXT:418) and Optuna/Ray-Tune
> sampler/scheduler choice per variant class, the search signatures, the variant-set record schema, the
> variant-space declaration grammar, and whether the search runs **on a schedule / on a C46-signal trigger /
> on operator demand** are **sweep-2+** (frozen with C46 + C48). C47 builds **no** custom optimizer and runs
> **no** model call of its own beyond what DSPy's compile loop intrinsically performs (and that token cost is a
> known self-optimization-layer cost — G32 thread; §7).

## 6. Failure modes & handling

**No assigned Gxx.** The component-inventory C47 row lists its Key-gaps column as **"—"** (line 59): C47 has
**no assigned Gxx** and **no blocking gap**. C47's job is wiring two mature, license-clean libraries
(DSPy MIT, Optuna MIT, Ray Tune Apache-2.0 — README:315–317, all "Clean") onto the C46 signal and the C48
hand-off; the v4 docs assign it no open adversarial finding. The relevant **F-modes** for C47's layer are F47
and F60 (below), and two batch-level threads (G32 cost, G09 threshold) **touch** C47's pipeline but are
**owned upstream/downstream** (C46/C48/C50), not at C47.

**F-modes (Layer 6 / P12 — F-MODE-COVERAGE §5).**
- **F47 — Visible-metric drift / Goodhart (Partial).** "Meta-metric definition is values-question; variant
  testing measures multiple metrics simultaneously; no single visible target" (F-MODE-COVERAGE:63); the
  cross-cutting remedy is **multi-metric mandatory — promotion gate requires multiple metrics moving
  together** (F-MODE-COVERAGE:103). C47 underwrites the **upstream half**: it proposes variants against C46's
  **multi-metric** signal and **never collapses the objective to a single optimized number** (INV-5). The
  *enforcement* — that a variant only promotes when multiple metrics move coherently — is **C50's** gate; F47
  stays **Partial** because Goodhart applies recursively to the meta-metrics themselves (a values question
  owned at C46, not closeable by C47). C47 detects nothing and decides nothing here; it keeps the search
  multi-objective so the downstream gate *can* hold.
- **F60 — Parallel-cycle compounding error (Addressed).** "Aggregate-rate tracking in meta-metric set …
  A/B harness reports aggregate not single-cycle" (F-MODE-COVERAGE:64). This is **C46** (aggregate-rate
  tracking) + **C48** (the A/B harness reporting aggregate). C47 is a beneficiary, not an owner: it proposes
  against C46's aggregate signal and hands variants to the C48 harness that reports aggregate. C47 introduces
  no per-cycle-only metric that would undercut F60.

> F-mode applicability is owned by **C57** (coverage map). C47 contributes the **variant-proposal half** of the
> P12 picture (it does not own any F-mode's full closure); it defers the canonical F-mode mapping to C57.

**Other failure cases.**
- **Thin / cold-start meta-metric signal (C46 not yet rich).** If C46 has too little history to optimize
  against (early Phase 3d, or a just-introduced metric), C47 emits **no fabricated variant** — it surfaces
  "insufficient signal to optimize" and proposes an empty set, rather than searching against noise.
  *[FAITHFUL-FILL]: minimal honest choice; mirrors C36's cold-start "insufficient data → no false flag" and
  C55's withhold-the-claim discipline. v4 states the dependency (C46) but not the cold-start rule.]*
- **C46 unreachable.** C47 **skips the search cycle without crashing** and re-runs when C46's signal is again
  readable (the signal is re-readable from C46, INV-6; no variant is permanently lost — only delayed). C47
  adds **no** durable queue of its own (durability of the meta-metric stream is C46's, which inherits the
  C24/C21 G33 posture). *[FAITHFUL-FILL]: read-side fail-open/skip-and-re-run, mirroring C36's inherited-G33
  reader posture; inventing a C47-side buffer would exceed faithful scope — the bar, DROP.]*
- **Search yields a degenerate / untestable variant.** A variant the engine proposes that is not concretely
  applyable (e.g. references a knob no longer in the config surface) is **dropped with a recorded reason**, not
  emitted — INV-3 requires every emitted variant be testable by C48. *[FAITHFUL-FILL]: fail-closed-per-variant;
  mirrors C36's per-value exclusion-with-count.]*
- **DSPy compile token cost (the self-optimization cost thread, G32).** DSPy's compile loop itself spends model
  tokens, and a wide hyperparameter grid multiplies experiment cost. v4's **G32** ("cost is essentially
  unmodeled … A/B variant replays … no cost model", ambiguities G32) is the relevant thread, **owned at C46**
  (cost-per-satisfaction is C46's headline metric) and at **C48** (variant-replay cost). C47's faithful posture
  is **bounded fan-out**: the variant-space declaration (I2) is the natural place to **bound how many variants
  per cycle** are proposed, so the experiment cost C48/C49 then incurs is capped at C47's source. C47 does
  **not** model cost (that is C46/G32); it **bounds the proposal count** so the unmodeled cost stays bounded.
  *[FAITHFUL-FILL]: G32 is not assigned to C47; the minimal honest C47-side mitigation for an unmodeled-cost
  layer is to cap the proposal fan-out at the declaration, deferring the cost *model* to C46/G32. v4 names no
  C47 cost model.]*

**The bar — what got DROPPED.** Per the ruthless bar, C47 is held to *only* the P12-tied wiring (define the
variant space, point the search at the C46 signal, hand the candidates to C48) plus selection/config of the
v4-named engines. **Dropped / refused as non-principle or already-in-the-stack:** (1) **any custom optimizer /
search algorithm** — prompt optimization is **DSPy** (Bootstrap/BootstrapFewShot/MIPRO) and hyperparameter
search is **Optuna / Ray Tune** off-the-shelf (AI-CONTEXT:355–356,418–419); a hand-rolled Bayesian / bandit /
evolutionary search is the textbook DROP for this component; (2) **A/B routing + statistical comparison** —
those are **C48** (README:273,275; D-19 routes significance to C48), and a C47-side comparator would duplicate
C48; (3) **the promotion gate** — **C50** (README:276); (4) **the counterfactual-replay driver** — **C49**
(README:274; G19), the variant-*execution* substrate, not C47's; (5) **meta-metric definition / tracking** —
**C46** (README:269–270); C47 reads the signal, it does not define or store it; (6) **methodology / topology
variant search** — v4 marks it **"None / DIY / Research frontier"** (AI-CONTEXT:357) and routes
methodology-as-config experiments to **C55**; C47 does **not** enter the unsolved frontier. What is **kept**:
the **variant-space declaration**, the **C46-signal-as-objective wiring**, and the **variant-set hand-off to
C48** (the one genuinely load-bearing custom surface), plus the DSPy/Optuna/Ray-Tune selection/config the
off-the-shelf engines need.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C47 reads the **C46 meta-metric signal** (aggregate numbers about the factory's own
  performance) and emits **variant proposals** (prompt-program / config changes). It touches no held-out
  scenarios and no raw user payloads. A proposed variant is a *candidate* only — it is **never auto-applied**;
  C48 routes + compares and C50 (a multi-metric gate under heavy human review, README:470) decides default
  promotion. The "highest-risk layer; heaviest human review" framing (README:470) lands on the *promotion*
  decision (C50), not on C47's proposal; C47's blast radius is bounded to *what gets experimented with*, gated
  downstream.
- **Cost.** The honest cost note for C47 is **G32** (cost is unmodeled at the self-optimization layer): **DSPy's
  compile loop spends model tokens**, and the **hyperparameter grid is multiplicative** on experiment cost
  (each candidate becomes a C48/C49 replay). C47 itself owns no cost *model* (that is C46's
  cost-per-satisfaction + G32), but its **variant-space declaration is the natural fan-out bound** — capping
  proposals-per-cycle caps the downstream experiment spend (§6). Quantifying the per-cycle token/compute budget
  is a sweep-2 concern with C46 (OQ-3 / G32).
- **Scale.** Search cost grows with the **size of the variant space** (number of prompt programs × size of the
  hyperparameter grid) and the engines' iteration budget — handled by **DSPy / Optuna / Ray Tune** (Ray Tune in
  particular scales hyperparameter search across workers). No bespoke scaling machinery is warranted (the bar);
  C47's scale lever is the declaration (how big a space, how many candidates), not custom infrastructure.
- **Observability.** C47's own health (cycles run, variants proposed per cycle, empty/no-op cycles, dropped
  degenerate variants with reason, the objective the search was pointed at) is worth emitting as events for
  auditability — the self-optimization loop must be inspectable since it tunes the factory itself. C47 is both a
  *reader* of C46's meta-metrics and an *emitter* of the proposal that opens an experiment.
- **Ops.** Pack-delivered **Python** tool node operated with the self-optimization pack in **Phase 3d**
  (README:271–272,470), built **last** after Layers 1–5 are solid (README:278). **Pin DSPy / Optuna / Ray Tune
  versions** so the variant-search contract is reproducible (inherits the eval/P11/P12-tier version-pin
  discipline; mirrors C36's PyOD/Anomalib pin). Whether the search runs on a schedule, on a C46-signal trigger,
  or on operator demand is a sweep-2 ops choice (OQ-3).

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (proposes variants from the signal — I1/I3/I4):** given a C46 meta-metric signal and a declared
   variant space, C47 produces a **non-empty set of concrete candidate variants** (prompt and/or
   hyperparameter); given a signal already at a local optimum (or too thin), it produces an **empty / no-op
   set** rather than a fabricated variant (README:271–272; AI-CONTEXT:355–356).
2. **AC-2 (off-the-shelf search — INV-1, the bar):** prompt-variant generation is **DSPy**; hyperparameter
   search is **Optuna / Ray Tune**; **no bespoke optimizer / search algorithm** is present
   (AI-CONTEXT:355–356,418–419). *(Verifiable: the search path is a configured call into the named engines, not
   a custom optimizer.)*
3. **AC-3 (emits a testable, attributed variant set — I4/INV-3):** each emitted variant is a **concrete,
   applyable change** carrying **provenance** back to the search/objective, and is **consumable by C48**
   (B64 "Down: A/B routing") without C47 re-derivation.
4. **AC-4 (propose-only — INV-2):** C47 renders **no** A/B routing, **no** significance verdict, and **no**
   promotion decision; it only proposes + hands off (D-19 significance→C48; routing/promotion = C48/C50).
   *(Verifiable: C47 runs with no routing target, no comparator, and no promotion writer configured.)*
5. **AC-5 (objective is C46's signal, multi-metric — INV-4/INV-5, F47):** the search is pointed at the **C46
   meta-metric** as objective and **does not collapse to a single visible target** (multi-metric mandatory,
   F-MODE-COVERAGE:103); C47 does **not** define "better" (that is C46).
6. **AC-6 (read-side / no source-of-truth — INV-6):** C47 reads C46 and owns no durable store; re-running the
   search over the same C46 signal + variant-space re-derives an equivalent variant set (engine stochasticity
   seedable/re-runnable).
7. **AC-7 (cold-start / unreachable-signal honesty):** a too-thin C46 signal yields **no fabricated variant**
   ("insufficient signal to optimize"); C46 unreachable → **skip-cycle without crashing** and re-run on
   recovery, with **no C47-side durable queue** added.
8. **AC-8 (bounded fan-out — G32 thread):** the **variant-space declaration bounds proposals-per-cycle**, so
   the downstream experiment cost (C48/C49 replays) is capped at C47's source; C47 itself models **no** cost
   (that is C46/G32).
9. **AC-9 (scope boundary):** C47 does **not** route traffic (C48), run the significance test (C48), promote
   (C50), drive counterfactual replay (C49), define/track meta-metrics (C46), or search the **methodology /
   topology** space (AI-CONTEXT:357 "None / DIY / Research frontier"; that loop is C55). It covers only the two
   **mature** auto-variant rows — prompt (DSPy) + hyperparameter (Optuna/Ray Tune).

**Test strategy.** A **variant-identification pack** that seeds synthetic C46 meta-metric signals (a signal
with headroom, a signal at a local optimum, a too-thin/cold-start signal, an unreachable C46) and a synthetic
variant-space declaration (a small prompt-program set + a small hyperparameter grid), and drives AC-1…AC-9 — in
particular that a signal-with-headroom yields **concrete, attributed variants consumable by C48** (AC-1/AC-3),
that the search is the **off-the-shelf DSPy/Optuna/Ray-Tune engine** (AC-2), that C47 is **propose-only**
(AC-4, run with no router/comparator/promoter), that the objective stays **multi-metric** (AC-5, F47), that a
local-optimum/thin signal yields **no fabricated variant** (AC-1/AC-7), and that the **fan-out is bounded at
the declaration** (AC-8, the G32 thread). This suite is built **after** the C46 meta-metric stream stands
(C47 reads what C46 produces), and **C47's variant-set contract must be frozen before C48 builds on it**, since
C48 assumes C47's set is the canonical experiment input (B64; D-19).

## 9. Open questions

- **OQ-1 (→ review-log, top): the C46-objective definition (inherits G09/G32).** C47 points its search at the
  **C46 meta-metric** as the optimization objective, but C46's metric is itself underdefined — **G09** (no
  threshold / "satisfied" semantics, ambiguities:29) and **G32** (cost-per-satisfaction unmodeled,
  ambiguities:83) are **C46's** open gaps. So C47's search is only as well-defined as C46's signal. Confirm the
  faithful reading: C47 **reads** whatever multi-metric signal C46 exposes and optimizes toward it **without**
  resolving C46's metric-definition gaps (those stay at C46); and confirm **which C46 metrics** form the
  Sweep-1 objective (cost-per-satisfaction / time-to-threshold / judge-FP-rate, or a subset). Freeze with C46.
- **OQ-2 (→ review-log): the C47→C48 hand-off contract + variant-set carrier.** The canonical **variant-set
  record shape** (each entry = a concrete prompt-program and/or hyperparameter-config change + provenance) and
  **whether it is a C20 bead type or a C23 event** (the carrier to C48 — parity with C36's OQ-2 carrier
  question). Also: does C47's set carry **only the candidate list**, or also the **experiment design** (sample
  size / which scenarios / replay plan) that C48 routes? v4 states the *boundary* (C47 identifies, C48 routes +
  compares) but not the hand-off shape. Freeze at sweep 2 **with C48** (the principal consumer) + C20/C23 (the
  carrier).
- **OQ-3 (→ review-log): search trigger + engine selection + fan-out budget.** When does C47 search — **on a
  schedule, on a C46-signal trigger, or on operator demand**? Which **DSPy compiler** (Bootstrap /
  BootstrapFewShot / MIPRO, AI-CONTEXT:418) and which **Optuna/Ray-Tune sampler/scheduler** per variant class?
  And the **proposals-per-cycle budget** that bounds downstream experiment cost (the G32 fan-out lever, §6/§7).
  All sweep-2, against the pinned engine versions.
- **OQ-4 (→ review-log): the variant-space declaration grammar + ownership.** *What is optimizable* — which
  prompt programs are DSPy-compilable and which config knobs form the Optuna/Ray-Tune search space — must be
  declared somewhere (pack TOML + binding, I2). Confirm this declaration's **home** (a C47 pack-config surface
  vs a shared self-optimization config owned via C03) and its **grammar**, and that **DSPy/Optuna/Ray-Tune are
  license-clean** to wrap (README:315–317 all "Clean" — confirmed; no transfusion-license blocker, parity with
  C36's clean PyOD/Anomalib). Sweep-2.
- **OQ-5 (→ review-log): methodology/topology variant search is explicitly excluded — confirm the boundary.**
  v4 marks "Auto variant — methodology/topology | None | DIY | Research frontier" (AI-CONTEXT:357). Confirm C47
  covers **only** the two mature rows (prompt = DSPy, hyperparameter = Optuna/Ray Tune) and that
  **methodology-as-config experimentation is C55** (not a C47 responsibility), so the unsolved frontier is not
  silently folded into C47's scope.
