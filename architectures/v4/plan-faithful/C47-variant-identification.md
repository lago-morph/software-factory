# C47 — Variant Identification  (Build Plan, canonical track)

> Source / Spec ref: spec/C47-variant-identification.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the variant seam contract (M1)** — the input contract (the **C46 meta-metric read**, I1: which meta-metrics form the objective — cost-per-satisfaction / time-to-threshold / judge-FP-rate, B12); the **variant-set output** contract (I4: each entry = a concrete prompt-program and/or hyperparameter-config change + provenance); and the signal **carrier** (C20 bead type vs C23 event — OQ-2). This is the interface **C48** builds against (B64 "Down: A/B routing"; D-19). | S | C46 meta-metric shape, C48 consumer shape |
| T2 | **Python pack/tool-node skeleton** — package C47 as a **Python** Gas City tool node per C02/C17 ABI; config surface (variant-space declaration, search trigger, fan-out budget) per C03 model (README:271–272 "Python tool node"). | S | C02/C17 ABI, T1 |
| T3 | **Variant-space declaration (I2)** — declare *what is optimizable*: the **prompt programs** (DSPy-compilable templates/signatures) and the **hyperparameter / config knobs** (the Optuna/Ray-Tune search space) — pack TOML + a thin binding. **Bound proposals-per-cycle** here (the G32 fan-out lever, §6/§7). | M | T2, C03 model |
| T4 | **C46 meta-metric read + objective wiring (I1/INV-4/INV-5)** — read the C46 signal as the search **objective / prior**; keep it **multi-metric** (no single visible target — F47, INV-5); cold-start/thin-signal → surface "insufficient signal", do not search against noise. | M | T1, T2, C46 stream standing |
| T5 | **Off-the-shelf prompt-variant search — DSPy (I3/INV-1)** — wrap **DSPy** compilers (Bootstrap / BootstrapFewShot / MIPRO; `github.com/stanfordnlp/dspy`, MIT; AI-CONTEXT:355,418) over the prompt space, objective = C46 signal. **No custom prompt optimizer** (the bar). Transfusion from DSPy (README:470). | M | T3, T4, DSPy pinned |
| T6 | **Off-the-shelf hyperparameter search — Optuna / Ray Tune (I3/INV-1)** — wrap **Optuna** (`github.com/optuna/optuna`, MIT) **/ Ray Tune** (Apache-2.0) (AI-CONTEXT:356,419) over the hyperparameter space, objective = C46 signal. **No custom search algorithm** (the bar). | M | T3, T4, Optuna/Ray Tune pinned |
| T7 | **Variant-set assembly + emit (I4/INV-3)** — collect DSPy + Optuna/Ray-Tune candidates into a typed **variant set**; each entry concrete + applyable + carrying provenance; **drop degenerate/untestable variants with a recorded reason**; emit to the C48 sink (carrier per T1). | M | T5, T6, T1 (carrier frozen) |
| T8 | **Propose-only guard (INV-2)** — confirm C47 runs with **no routing target, no comparator, no promotion writer** configured (routing/significance = C48 per D-19; promotion = C50); emit empty/no-op set when no worthwhile variant exists. | S | T7 |
| T9 | **Cold-start / unreachable-signal resilience (INV-6)** — too-thin C46 signal → **no fabricated variant**; **C46 unreachable → skip-cycle without crashing**, re-run on recovery; **no C47-side durable queue** (durability is C46's, inheriting C24/C21 G33). Plus health events (cycles run / variants per cycle / empty cycles / dropped variants + reason / the objective searched). | S | T4, T7 |
| T10 | **Variant-identification pack (AC-1…AC-9)** — synthetic-signal harness (signal-with-headroom / at-local-optimum / too-thin / C46-unreachable) + synthetic variant-space (small prompt set + small hyperparameter grid) driving all acceptance tests, especially proposes-concrete-attributed-variants, off-the-shelf-search, propose-only, multi-metric-objective, no-fabricated-variant, and bounded-fan-out. | L | T3–T9, C46 meta-metric stream standing |

## 2. Dependency graph

**Must precede C47:**
- **C46** (the meta-metric stream C47 reads as its optimization objective — standing, with its metric shape
  frozen enough for C47 to point a search at it; inventory C47 `depends on C46`; B64 "Up: meta-metrics").
- **DSPy / Optuna / Ray Tune** (the variant-search engines, version-pinned; all license-clean — README:315–317)
  + **C02/C17** (pack + tool-node ABI to package/invoke the Python tool node).

**C47 must precede (its consumer assumes the variant set is the canonical experiment input):**
- **C48** A/B routing & statistical comparison (routes traffic between the proposed variants + runs the
  significance test — B64 "Down: A/B routing"; D-19 significance→C48), and through C48 → **C50** promotion gate.
  **C49** (counterfactual replay) is the variant-*execution* substrate C48 uses, not a C47 dependency.

**Critical path inside C47:** T1 → T4 → (T5 ∥ T6) → T7 → T10. The load-bearing tasks are **T3 (variant-space
declaration)** + **T7 (variant-set assembly + emit)** — the genuinely custom surface (define the optimizable
space, point the search at C46, hand candidates to C48). Note **T5/T6 (the search engines) are *thin*: they
wrap DSPy / Optuna / Ray Tune, build **no** custom optimizer, and own **no** durable state** (C47 is a
read-side proposer, INV-6). The **bounded-fan-out** in T3 is the one explicit cost-discipline lever (the G32
thread; C47 owns no cost model — that is C46/G32).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, the build fans out concurrently:
- **WS-A (the two searches):** **T5 (DSPy prompt search)** and **T6 (Optuna/Ray-Tune hyperparameter search)**
  are **fully independent** workstreams — different engines, different parts of the variant space — and build in
  parallel once **T3 (variant-space declaration)** + **T4 (C46 objective wiring)** are in place. Each can build
  against a synthetic C46 signal fixture while C46's real stream firms up.
- **WS-B (assembly/resilience/ops):** **T7 (variant-set assembly + emit)** → **T8 (propose-only guard)** →
  **T9 (cold-start / unreachable resilience + health events)**. Can build against synthetic engine output before
  WS-A's real searches land.
- **T10** (variant-identification pack) joins both. WS-A and WS-B meet at the T5/T6 → T7 handoff (engine
  candidates becoming the emitted variant set).

The two-engine split (T5 ∥ T6) is the cleanest fan-out: prompt-variant generation (DSPy) and hyperparameter
search (Optuna/Ray Tune) share only the T3 declaration + T4 objective and the T7 sink — they can be built and
tested in isolation against the same synthetic C46 signal.

## 4. Interfaces-first / contract milestones

- **M1 — variant seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **input** = the C46 meta-metric read shape (which metrics form the objective, I1);
  (b) **output** = the `variant`-set record (each entry = a concrete prompt-program and/or hyperparameter-config
  change + provenance, I4);
  (c) **carrier** = C20 bead type vs C23 event (OQ-2, parity with C36's carrier question).
  Freezing M1 lets WS-A (the two searches) build against a synthetic C46 signal and WS-B build against synthetic
  engine output in parallel, and lets **C48** stub against the variant-set shape.
- **M2 — engines + variant-space fixed (T3/T5/T6):** DSPy compiler choice (Bootstrap / BootstrapFewShot /
  MIPRO) + Optuna/Ray-Tune sampler/scheduler choice per variant class, **off-the-shelf, no custom optimizer**
  (the bar / AC-2), and the variant-space declaration + **proposals-per-cycle bound** (the G32 fan-out lever),
  before C48 reasons over the proposed variants.
- **M3 — propose-only boundary fixed (T8/INV-2):** C47 emits candidates only — **no** routing / significance /
  promotion (D-19 significance→C48; routing=C48; promotion=C50) — so C48/C50 own those stages cleanly and C47's
  blast radius stays bounded to *what gets experimented with*.

## 5. Risks & de-risking order

1. **Confirm first — the C46 objective (T1/T4/OQ-1).** Resolve **which C46 metrics** form the Sweep-1 objective
   (cost-per-satisfaction / time-to-threshold / judge-FP-rate, or a subset) and confirm C47 **reads** C46's
   signal **without** resolving C46's own metric-definition gaps (**G09** threshold + **G32** cost are *C46's*,
   not C47's — ambiguities:29,83). A wrong call here mis-points the whole search. This retires the highest seam
   uncertainty and fixes C47's input.
2. **Pin — DSPy / Optuna / Ray Tune (T5/T6/AC-2).** Confirm the engine APIs + which DSPy compiler / Optuna-Ray
   sampler fits which variant class against the **pinned** versions (all license-clean — README:315–317), so the
   variant-search contract is reproducible and **no custom optimizer creeps in** (the bar / AC-2). Mirrors C36's
   PyOD/Anomalib version-pin discipline.
3. **Spike — the C47→C48 hand-off (T7/T1/OQ-2).** Freeze the **variant-set record shape** + **carrier** (C20
   bead vs C23 event). Per the spec's narrowed OQ-2, the **experiment/routing design is C48's** (routing
   strategy, arm-mapping, sample-size/α — C48 §3/§4), so the spike scope is **how much provenance/metadata each
   candidate carries** for C48 to build its design, **not** whether C47 owns the design. C48 is unbuilt
   (Batch 5) — name the seam and stub against it; do not block on C48.
4. **Confirm — propose-only boundary (T8/INV-2).** Verify C47 renders **no** routing, **no** significance
   verdict, **no** promotion — the clean P12-pipeline split (C47 proposes → C48 routes+compares → C50 promotes;
   C49 replays). Run C47 with no router/comparator/promoter configured (AC-4).
5. **Confirm — bounded fan-out + multi-metric objective (T3/T4/INV-5/G32).** Verify the variant-space
   declaration **bounds proposals-per-cycle** (so downstream C48/C49 experiment cost is capped — the G32 thread,
   C47 owning no cost model) and that the objective stays **multi-metric** (no single visible target — F47,
   F-MODE-COVERAGE:103), the upstream half of the Goodhart discipline the C50 gate enforces.
6. **Confirm — methodology/topology exclusion (OQ-5).** Confirm C47 covers **only** the two mature auto-variant
   rows (prompt = DSPy, hyperparameter = Optuna/Ray Tune) and that **methodology/topology** variant search
   ("None / DIY / Research frontier", AI-CONTEXT:357) is **out of scope** — methodology-as-config experiments
   are **C55** — so the unsolved frontier is not silently folded into C47.

## 6. Definition of done

**Per-component DoD:** the variant-identification pack (T10) passes **AC-1…AC-9** against synthetic C46 signals
+ a synthetic variant space — proposes-concrete-variants-from-the-signal (empty set when at optimum/too thin),
**off-the-shelf search** (DSPy + Optuna/Ray Tune, **no custom optimizer**), **testable + attributed variant
set** consumable by C48, **propose-only** (no routing/significance/promotion — D-19), **objective is C46's
multi-metric signal** (F47, does not define "better"), **read-side / no source-of-truth** (re-derivable),
**cold-start / unreachable-signal honesty** (no fabricated variant; skip-cycle-no-crash; no C47-side queue),
**bounded fan-out** (the G32 thread, C47 owns no cost model), and the **scope boundary** (no
routing/significance/promotion/replay/meta-metric-definition; no methodology/topology search — that loop is
C55). C47 is a **Python** tool node in a Gas City pack.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C46 (input) and C48 (consumer) owners; sub-streams + C48 can stub
  against them.
- T3: variant-space declaration expresses the prompt + hyperparameter surface and **bounds proposals-per-cycle**
  (the fan-out lever).
- T4: C46 signal read as a **multi-metric** objective (AC-5, F47); thin signal → "insufficient signal", no
  search against noise (AC-1/AC-7).
- T5/T6: prompt variants via **DSPy**, hyperparameter variants via **Optuna/Ray Tune** (AC-1/AC-2); **no custom
  optimizer** present (the bar / AC-2).
- T7: emitted variant set carries **concrete, applyable, attributed** entries consumable by C48 (AC-3);
  degenerate variants dropped-with-reason.
- T8: C47 runs with **no** router/comparator/promoter; emits empty/no-op set when warranted (AC-4).
- T9: AC-7 — thin signal → no fabricated variant; C46 down → skip-cycle/no-crash → re-run on recovery; **no
  custom durable queue** introduced; health events visible.
- T10: full AC suite green; built **after** the C46 meta-metric stream stands; **C47's variant-set contract must
  be frozen before C48 builds on it**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (the C46-objective definition —
which metrics; C47 reads, does not resolve C46's G09/G32), OQ-2 (the C47→C48 hand-off contract + variant-set
carrier [C20 bead vs C23 event] + candidate-list-only vs candidate-list-plus-experiment-design), OQ-3 (search
trigger [schedule / C46-signal / operator demand] + DSPy compiler & Optuna/Ray-Tune sampler selection +
proposals-per-cycle budget), OQ-4 (the variant-space declaration grammar + ownership [C47 pack-config vs shared
C03-owned self-opt config]; DSPy/Optuna/Ray-Tune license-clean confirmed), OQ-5 (methodology/topology search is
**excluded** — C47 = prompt+hyperparameter only; methodology-as-config = C55 — confirm the boundary).

**No assigned Gxx / no blocking gap.** The component-inventory C47 row lists **"—"** in the Key-gaps column
(line 59): C47 carries **no assigned gap** and **no blocking gap**. The G09 (threshold) and G32 (cost) threads
that touch C47's pipeline are **owned upstream/downstream** (C46/C48/C50), not at C47; C47's faithful posture is
to **read C46's signal as-is** and **bound its proposal fan-out**, deferring those gaps to their owners.
