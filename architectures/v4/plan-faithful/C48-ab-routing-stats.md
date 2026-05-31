# C48 — A/B routing & statistical comparison  (Build Plan, canonical track)

> Source / Spec ref: [C48 spec](../spec/C48-ab-routing-stats.md)
> Track: canonical   Status: sweep-1

C48 is the **two-faced P12 component**: it (1) **routes traffic between variants** (feature flags —
**Unleash/GrowthBook/Flagsmith**, README:273 — or an adaptive **bandit** — **MABWiser/Vowpal Wabbit**,
AI-CONTEXT:361) and (2) **determines whether a variant was *actually* better** (significance, not a higher
mean — **scipy.stats/statsmodels + Evidently**, README:275). It is **not** a routing engine, **not** a
statistics engine, **not** the promotion decision (that is **C50**, which *consumes* C48's verdict), and
**not** the cost model (that is **C46** — C48 only *uses* C46's cost signal, G32). The custom surface is small
and entirely **wiring + contract**: the **routing-strategy binding** (incl. the G32 cost-aware bandit reward),
the **significance-determination wiring** (test selection over off-the-shelf scipy/Evidently), and the
**verdict contract** that **C50** (promotion evidence) and **C55** (methodology significance, **D-19**)
consume. The load-bearing work is therefore **freezing the verdict contract** and **resolving the G32
cost-signal use** — not building any engine. C48 is **Batch 5** (built last, behind a feature flag,
README:278/470); its only upstreams are **C47** (variant set) and **C46** (cost/meta-metrics), plus **C33**
(satisfaction outcome).

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1 — Verdict contract (the keep)** | Define the **comparison-verdict record** (I4): per metric — winning arm, effect size, p/CI, sample sizes; overall **multi-metric** reading (INV-2); **cost effect** (G32). The contract C50 + C55 consume. **Freeze early** (Task is the critical interface). | M | C47/C46/C33 shapes (named); C50/C55 consumer needs |
| **T2 — Routing-strategy binding (I1)** | Wrap the OSS router: bind a C47/C55 variant set to a **feature-flag split (Unleash)** *or* an **adaptive bandit (MABWiser)**; expose the per-unit **route call**. Config in pack TOML (I6). No custom splitter/bandit (INV-5). | M | T1 (arm identity in verdict); Unleash/MABWiser pinned |
| **T3 — Outcome read (I2)** | Read per-arm **C33 satisfaction distribution** + **C46 meta-metrics/cost**, keyed by arm + experiment. Read-only; computes neither (INV-4). | S | C33/C46 output shapes (sweep-2 freeze) |
| **T4 — Significance determination (I3)** | Wire **scipy.stats/statsmodels** (hypothesis test) + **Evidently** (distribution-shift/regression) over the arms' distributions → per-metric effect + p/CI + significance decision (INV-1), multi-metric (INV-2), aggregate (INV-3). Off-the-shelf engine; C48 owns **test selection** + **multiple-comparison correction**, not the math. | M | T1, T3; scipy/statsmodels/Evidently pinned |
| **T5 — Cost-aware routing (G32, I5/INV-6)** | Make C46's per-variant cost a first-class input: a bandit **satisfaction-per-dollar reward** (or flag spend-cap) in T2, and a **cost effect** in the T1 verdict. **Degrade-with-declaration** when C46's cost model is absent (no fabricated cost effect). | M | T2, T4; C46 cost-signal shape (OQ-1 freeze) |
| **T6 — Pack + feature-flag gating (I6)** | Package as a Gas City **router pack** + **Python stats tool node** (C02/C17 ABI), **feature-flag-gated** (C03); pin all engine versions for reproducibility (§7 ops). | S | T2, T4; C02/C17/C03 |
| **T7 — Acceptance pack (AC-1…AC-9)** | The A/B-comparison test pack: seed synthetic arms (no-difference / significant / unequal-small-n / better-but-pricier), drive AC-1…AC-9; routing test that a bandit shifts toward higher satisfaction-per-dollar. | M | T1–T6 |

## 2. Dependency graph

- **Upstream (must exist / shape known):** **C47** (variant set, I1), **C46** (cost + meta-metrics, I2/I5 —
  **owns the G32 cost model**), **C33** (satisfaction outcome, I2). C48 reads all three; it computes none.
- **Downstream (consume C48):** **C50** (promotion gate — the **principal verdict consumer**; inventory C50
  `depends on C48`) and **C55** (methodology significance — **consults** the verdict, D-19).
- **Critical path:** **T1 (verdict contract) → T4 (significance) → T7 (acceptance)**. T1 is the gating
  interface: C50 and C55 both contract against the verdict, so it must freeze before they can build against a
  stub. Routing (T2) and cost-aware wiring (T5) are on a parallel path that rejoins at T4/T1.
- **Batch position:** **Batch 5**, built last (README:278). Nothing in Batch 5 is upstream of C48 except
  C47/C46; C48 is upstream of C50 (and consulted by C55, which is Batch 4 and **names but does not block on**
  the seam — spec/C55 OQ-4).

## 3. Parallelization

Two independent workstreams after T1 freezes:
- **WS-A (routing):** T2 (router binding) → T5 (cost-aware reward/spend-cap). Can build against the OSS router
  (Unleash/MABWiser) immediately once the arm identity from T1 is fixed.
- **WS-B (significance):** T3 (outcome read) → T4 (significance wiring). Can build against synthetic per-arm
  distributions immediately once the verdict shape from T1 is fixed.
- **WS-A and WS-B rejoin** at the **verdict** (T1/T4) and at **T5** (cost effect appears in both the route and
  the verdict). T6 (packaging) and T7 (acceptance) follow.
Explicit fan-out: **T1 first** (serializing interface), then **WS-A ∥ WS-B**, then T5 (joins cost into both),
then T6, then T7.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs in parallel:
1. **The comparison-verdict record (T1, I4) — the load-bearing contract.** Per-metric significance + effect +
   sample sizes + overall multi-metric reading + cost effect. **C50** (promotion evidence) and **C55**
   (methodology significance, D-19) both build against this. *Freeze with C50 + C55 (OQ-4).*
2. **The route call (T2, I1).** `route(unit, variant_set) → arm` — the surface C47/C55 experiments invoke.
   Stub with a fixed split; swap in the bandit later.
3. **The cost-signal contract (T5, I5 — G32).** The **per-variant cost shape** C48 consumes from **C46** (token/$
   per unit, attributable to an arm). *Freeze with C46 (OQ-1) — the cost *model* is C46's; C48 freezes only the
   *signal it reads*.*
4. **The outcome read keys (T3, I2).** How C33 distributions + C46 meta-metrics are keyed by arm + experiment.
   *Freeze with C33/C46.*

## 5. Risks & de-risking order

Prototype/spike in this order to retire the most uncertainty:
1. **G32 cost-signal contract (OQ-1) — highest uncertainty.** The cost model is unmodeled corpus-wide
   (AI-CONTEXT:143 is the only number); spike the **C46↔C48 cost-signal shape** first so T5 (cost-aware
   routing) and the verdict's cost effect have ground to stand on. Confirm the **model** is C46's (G32 reading
   (b)) and C48's **degrade-with-declaration** path (INV-6) when it is absent.
2. **Test selection + multiple-comparison correction (OQ-2).** Spike which **scipy/statsmodels** test fits the
   C33 satisfaction-distribution shape (continuous vs. rate vs. **Evidently** distribution-shift) and the
   correction across k arms × multiple metrics — so INV-2's multi-metric verdict is not itself a Goodhart hole.
3. **Routing strategy default + bandit reward (OQ-3).** Spike flag-split vs. bandit, and the **satisfaction-per-
   dollar reward** on a single $200/month seat (cost-sensitive exploration). Validate the bandit shifts
   allocation correctly on synthetic arms (T7's routing test).
4. **The C48→C50 / C55 verdict consumption (OQ-4).** Validate the verdict satisfies **both** C50's statistical
   gate and C55's methodology-significance consultation before either builds against it.

## 6. Definition of done

- **Per-task:** each Task meets its tied acceptance criterion — T1↔AC-8 (verdict consumable by C50/C55),
  T2↔AC-2 (routes via flag/bandit), T4↔AC-1/AC-3/AC-4 (significance, multi-metric, aggregate), T5↔AC-6
  (cost-aware + degrade-with-declaration), T6↔AC-7 (engine-reuse, no custom router/stats), T7↔AC-1…AC-9.
- **Per-component:** AC-1…AC-9 pass; the verdict asserts "better" **only on significance** (INV-1) and is
  **multi-metric** (INV-2) over **aggregate** distributions (INV-3); C48 makes **no** promotion decision and
  **no** model call (INV-4); routing + stats are the **off-the-shelf** engines (INV-5); **cost is in the loop**
  (INV-6, G32). The **acceptance pack must pass before C50 consumes the verdict for promotion and before C55
  consults C48 for methodology significance** (D-19).
- **Gaps/decisions discharged:** **G32** addressed at C48's scope (cost as a first-class routing/comparison
  input; cost-*model* deferred to C46 per reading (b)); **D-19** honored (C48 is the home of significance for
  the self-opt loop **and** for C55); **D-6** (canonical track), **D-15** (holistic satisfaction as the primary
  outcome) respected.
- **Open seams to sweep-2:** the **verdict-record schema** + **test-selection/correction table** (OQ-2), the
  **cost-signal contract** (OQ-1, with C46), the **routing default + bandit reward** (OQ-3), and the
  **C48→C50 / C55→C48** consumer contracts (OQ-4) — all frozen when C50 is authored and C46's cost model lands.
