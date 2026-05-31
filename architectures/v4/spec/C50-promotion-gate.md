# C50 — Promotion gate (`promotion-gate`)  (Spec, canonical track)

> Source: README Part 4 §"Principle 12 — Self-optimization" (lines 272–280 — the P12 component table;
> row 276 "**Promotion gate** | New variant becomes default | Custom: Gas City formula with statistical
> gate | n/a (your work, small) | Gas City formula"; line 280 "P12 is the most ambitious and the most
> research-flavored … the driver is your most significant invention. **Build last**, after Layers 1-5 are
> solid"; line 272 "The system measures its own meta-performance and improves it over time"); README Part 5
> license row (Gas City formula, "your work"); AI-CONTEXT §7 "Layer 6 — self-optimization (P12)" (line 362
> "**Promotion gate | None | DIY | Small custom (formula)**"; line 286 "Layer 6: cost-routing covered;
> **A/B + promotion absent**"; line 516 "**Self-optimization meta-metrics: which specifically? Values
> question — needs operator input**"); F-MODE-COVERAGE §5/§8/§12 (line 103 "**F47 Goodhart on visible
> metrics … Multi-metric mandatory: no single visible target; P12 always tracks aggregate of multiple
> metrics; promotion gate requires multiple metrics moving together**"; line 174 "**Make F47 multi-metric
> mandatory … promotion gate requires multiple metrics moving coherently. Goodhart applies and v4 should
> not pretend otherwise**"; line 63 F47 row "variant testing measures multiple metrics simultaneously; no
> single visible target"); component-inventory C50 row (Self-Optimization subsystem; kind = **control-loop**;
> "Statistical, multi-metric gate deciding a new variant becomes the default; **guards Goodhart**"; maps
> **A72, B61, B78**; depends **C48, C12**; gap **G18**; foundational = no) + Batch-5 placement (L115 —
> "research frontier, built last"); component-inventory-A A72 ("New variant becomes default via statistical
> gate (Gas City formula)"; "**Multi-metric mandatory (FM F47)**"); component-inventory-B B61 ("Statistical
> gate deciding a new variant becomes the default … Custom Gas City formula with stat gate; **multi-metric
> mandated (F47)**"), B78 ("**F47 caution — Goodhart on meta-metrics** … Explicit visible meta-metrics
> invite Goodharting recursively. **Guard: multi-metric mandatory; no single visible target**").
> Binding decisions obeyed: **D-6** (single canonical track; no Track-A/B framing). **D-15 / G09:** C50 is a
> **cutline DECISION SITE** — the satisfaction-threshold *value* is operator policy; C50 *applies* it (it
> does not define it, and does not push it back into C33, which stays threshold-free). **D-19:** C50
> **consumes C48's significance verdict** ("was the variant actually better?") and does **not** re-run
> statistics. C50 is the **RECURRING promotion gate**, distinct from **C53** (one-time bootstrap go/no-go)
> and **C39** (fix-loop termination; **XC-3** — C39 owns the numeric N-attempts/oscillation/L5-ship policy).
> Companion specs: [`spec/C12-formula-pipeline-file.md`](./C12-formula-pipeline-file.md) (the **variant**
> being promoted *is* a formula — methodology is the variable), [`spec/C33-satisfaction-metric.md`](./C33-satisfaction-metric.md)
> (threshold-free distribution; routes the cutline to **C50**/C53/C39, C33 §6), [`spec/C39-fix-task-loop-closure.md`](./C39-fix-task-loop-closure.md)
> (the sibling G18 gate it is NOT), [`spec/C53-bootstrap-validation.md`](./C53-bootstrap-validation.md) (the
> sibling one-time gate it is NOT). [`spec/C48-ab-routing-stats.md`](./C48-ab-routing-stats.md) (A/B +
> significance) and [`spec/C46-meta-metrics.md`](./C46-meta-metrics.md) (meta-metric stream) are Batch-5
> peers (now on disk, sweep-1); C50's dependency on their contracts is per the inventory mandate.
> Inventory ID: C50   Kind: control-loop   Status: sweep-1
> Track: canonical

## 1. Purpose & responsibility

C50 is the **promotion gate** (P12): the **recurring, statistical, multi-metric gate that decides whether a
new variant becomes the default** (README:276; inventory C50). It is the closing arc of the
self-optimization loop — *meta-measure (C46) → identify a variant (C47) → A/B-test it + decide significance
(C48) → **promote the winner (C50)*** — the step that actually **flips the default config** from the
incumbent to a challenger once (and only once) the evidence clears the bar.

The **variant** C50 promotes is a **C12 formula** (the pipeline-file / methodology DAG): v4's central
inversion is *methodology is the variable, substrate is convergent* (README:29–33; C12 §1), so a
"variant" is a candidate formula (a different chain shape, loop topology, deterministic-vs-model split, or
gate placement) competing to become the default formula. C50 is therefore the component that turns a
**proven-better formula into the new default formula**.

C50 exists to add **one** 12-principle capability nothing else in the stack supplies: a **promotion
*criterion* that is multi-metric and Goodhart-guarded**, not a single satisfaction number. v4 mandates this
explicitly and repeatedly — *"promotion gate requires multiple metrics moving together"* (F-MODE-COVERAGE:103),
*"promotion gate requires multiple metrics moving coherently"* (F-MODE-COVERAGE:174), *"multi-metric
mandatory; no single visible target"* (component-inventory-B B78). The reason is **F47 (Goodhart)**:
v4's meta-metric layer (C46) creates **explicit visible metrics**, and "Goodhart applies and v4 should not
pretend otherwise" (F-MODE-COVERAGE:174). If C50 promoted on a single metric (e.g. satisfaction alone), the
self-optimization loop would **game that one metric** — buy satisfaction with cost, or with latency, or by
overfitting held-out scenarios. The genuine KEEP is the **multi-metric promotion rule + the Goodhart guard**
that forbids a promotion which improves one visible metric while silently regressing another.

**The bar's genuine KEEP (why C50 exists at all).** Everything *statistical* about "was the variant actually
better?" is **C48's** (the A/B routing + scipy/Evidently significance test — D-19); everything about *what
the metrics are* is **C46's** (cost-per-satisfaction, time-to-threshold, judge-FP-rate); the *satisfaction
distribution* is **C33's**; the *thing being swapped* is a **C12 formula**. What C50 uniquely adds is the
**decision rule that composes those signals into a promote / hold verdict under a Goodhart guard** — promote
**only** when **multiple** metrics move **coherently** (none materially regressed) **and** C48 says the move
is **significant** — and then **flips the default**. That rule, and the act of flipping the default, is the
load-bearing capability that does not exist anywhere else (the-bar, §6).

**Responsibilities (what C50 is the spec-of-record for):**
- **Define the multi-metric promotion criterion (I1, F47/B78 — the genuine KEEP).** The **decision rule** a
  challenger formula must clear to promote: **(a)** C48 reports the variant is **statistically better**
  (significance verdict, D-19) on the primary objective, **(b)** a **panel of C46 meta-metrics** moves
  **coherently** — the improvement is real across *multiple* metrics, **and (c)** the **Goodhart guard**
  holds — **no guard metric materially regresses** (improving satisfaction while cost-per-satisfaction or
  time-to-threshold degrades is **not** a promotion). C50 owns the *composition + the guard*; each
  *metric* is owned by C46 and the *significance* by C48.
- **Apply the satisfaction cutline as a decision-site (I2, D-15/G09).** C33 is **threshold-free** and
  **routes the "satisfied" cutline to the decision sites C50/C53/C39** (C33 §6). C50 is that decision site
  for promotion: it **applies** a satisfaction bar (and the guard-metric bars) to C46/C33's statistics. The
  cutline **value(s)** are **operator/integrator policy v4 does not fix** (G09; the "values question",
  AI-CONTEXT:516) — C50 owns *that bars are applied here and what the rule over them is*, not the numbers.
- **Decide promote / hold and flip the default (I3, README:276).** Emit a **`promote` | `hold`** verdict for
  a challenger formula; on `promote`, **make the challenger the new default** — the variant "becomes the
  default" by updating the **default formula reference** (the Gas City formula/config selection, C12/C03).
  This is the one action with a side effect on the live factory; it is the "Gas City formula with
  statistical gate" of README:276.
- **Record the promotion decision + its evidence (I4).** Persist the verdict with the **evidence it was
  computed over** (the C48 significance verdict, the C46 metric panel + the guard check, the C12 variant id
  + the incumbent it replaced) so a promotion is **auditable + reversible** — recorded on a bead (C20/C19),
  not a transient flip. Because P12 self-modifies the factory, the promotion record is a governance control
  (F54 relevance, §6).
- **Define the no-promote / hold branch (I5).** On `hold` (not significant, or a guard metric regressed),
  the incumbent default **stays**; the challenger is **not** promoted. C50 names *that a failed gate is a
  no-op on the default* (the loop simply keeps measuring / tries another variant) — it does not itself
  generate the next variant (that is C47) and does not force a rollback engine (the default reference is
  simply not changed).

**Explicitly NOT (boundaries):**
- **NOT the statistical-significance test.** Whether a variant is *actually better* — the A/B routing + the
  scipy/Evidently/`statsmodels` significance computation — is **C48's** ("determines whether a variant was
  actually better", inventory C48; D-19). C50 **consumes C48's significance verdict** as one rubric input;
  it runs **no** statistics and builds **no** estimator. *(Re-implementing significance here would be the
  exact over-build the bar forbids — and D-19 routes it to C48.)*
- **NOT the meta-metric definitions / the cost model.** *What* the metrics are (cost-per-satisfaction,
  time-to-threshold, judge-FP-rate) and how they are recorded over time is **C46's** (inventory C46; the cost
  model is C46/G32). C50 **reads** the C46 metric panel; it does not define a metric or own the cost model.
- **NOT the satisfaction metric.** The satisfaction *distribution* is **C33's** and is deliberately
  threshold-free (C33:INV-3). C50 is where a satisfaction *cutline is applied* (D-15/G09); it does **not**
  push the cutline back into C33 and does **not** recompute satisfaction.
- **NOT the variant identifier / generator.** *What to experiment with* — the prompt-program variants (DSPy)
  and hyperparameter variants (Optuna/Ray Tune) — is **C47's**; the candidate **formula** is authored/edited
  per C12. C50 **decides** whether a *given* challenger wins; it does not propose challengers.
- **NOT the counterfactual-replay driver.** Re-running a trajectory from a midpoint to produce comparable
  variant evidence is **C49's** (CXDB O(1) branching; the "most significant invention", G19). C50 consumes
  the *resulting* comparison via C48; it does not replay.
- **NOT the fix-task loop-closure gate (the OTHER G18 gate).** The **self-heal** "did the fix actually fix
  it?" loop and its **numeric termination policy** (N-attempts → escalate, F52 oscillation detection, L5
  ship-authorization) are **C39's** — explicitly (**XC-3**: "C39 OWNS the G18 numeric termination policy").
  C50 is the **steady-state promotion** gate; it shares the G18 tag but gates *which variant becomes default*,
  **not** *when a fix loop stops*. The two are different loops with different triggers (anomaly→fix vs.
  measure→variant→promote) and C50 owns **no** attempt-bound/oscillation/ship-auth policy (§6).
- **NOT the one-time bootstrap go/no-go.** The **once-only** Phase-2→Phase-3 milestone that ratifies the
  factory-builds-factory bet is **C53** (one-time, INV-6 there). C50 is **recurring** — it fires every time a
  challenger variant has accumulated enough A/B evidence to be judged. The three gates (C50/C53/C39) share
  the *apply-a-bar-to-C33's-distribution* pattern (each is a C33-deferred cutline owner, C33 §6) but differ
  in *what they gate* and *when*.
- **NOT the autonomy ladder.** *Whether* a promotion may flip the live default **without human review** is
  governed by the operator's declared autonomy level (**C56**, L0–L5). C50 **reads** the authorized level and
  gates the default-flip on it (a promotion at a low autonomy level surfaces for human ratification rather
  than auto-flipping); C50 does not define or set the ladder. *[FAITHFUL-FILL: v4 states promotion as "your
  work, small" (README:276) without naming the autonomy seam, but README:498/527 makes human review
  "required until P12 is mature and trusted" — gating the *flip* on C56 is the minimal consistent reading
  that does not let the self-optimizer silently re-default the factory.]*
- **NOT the canonical F-mode owner.** F-mode applicability is **C57**'s map. C50 *underwrites* the property
  that promotions are **multi-metric + Goodhart-guarded** (F47) and **recorded** (F54 — promotion is a
  self-modification of the factory) and significance-gated against overfitting (F9) — but defers the
  canonical mapping to C57.

## 2. Context & dependencies

| Direction | Component | Relationship (v4 source) |
|---|---|---|
| Upstream (depends on) | **C48** A/B routing & statistical comparison | Supplies the **significance verdict** — "was the variant actually better?" (inventory C48; **D-19**). C50 consumes the verdict as the *statistical* term of its rubric and runs no stats of its own. Hard inventory dependency (`Depends on: C48`). |
| Upstream (depends on) | **C12** Formula / pipeline-file | The **variant** C50 promotes **is a formula** (methodology is the variable, C12 §1); on `promote`, C50 updates the **default formula reference**. Hard inventory dependency (`Depends on: C12`). |
| Upstream (metrics) | **C46** Meta-metric stream | Provides the **panel of meta-metrics** (cost-per-satisfaction, time-to-threshold, judge-FP-rate) C50's multi-metric rule + Goodhart guard read (inventory C46). *(Concept dependency via the self-opt tier; C50's significance term comes through C48, the metric panel through C46.)* |
| Upstream (satisfaction) | **C33** Satisfaction metric | Produces the threshold-free **satisfaction distribution**; **routes the cutline to C50/C53/C39** (C33 §6). C50 applies the satisfaction bar here (D-15/G09). *(Reachable via C46, which itself reduces over C33; named because C50 is the cutline owner.)* |
| Upstream (comparable evidence) | **C49** Counterfactual replay | Produces midpoint-replayed variant trajectories that feed the A/B comparison (G19). C50 consumes the *result* via C48; not a direct edge. |
| Record host | **C20** Bead schema / **C19** Bead store | The **promotion decision + evidence** is recorded on a bead (mirroring how C39/C53 record on `factory_build`-style beads). C50 **requests a schema slot**; **C20 owns the schema** (D-3). *(Reference, not a new inventory edge.)* |
| Policy (autonomy) | **C56** Autonomy ladder (L0–L5) | Declares the authorized autonomy level; C50 gates whether a `promote` **auto-flips** the default or **surfaces for human ratification** (README:498/527). Not a hard inventory dependency (inventory lists C48/C12); the C50↔C56 tie is a policy seam (OQ-4). |
| Sibling (G18, NOT a dep) | **C39** Fix-task loop-closure | The **other** G18-tagged gate; owns the *fix-loop* numeric termination policy (XC-3). Same gap tag, different loop. C50 owns no fix-loop policy. |
| Sibling (cutline peer, NOT a dep) | **C53** Bootstrap validation | The **one-time** go/no-go milestone; a C33-deferred cutline owner like C50, but fires once. C50 is recurring. |
| Downstream (consumes the new default) | **C18** reconciler / **C05** dispatch | Once C50 flips the default formula reference, subsequent work instantiates the **new** default formula (C12 → C13 molecule → dispatch/run). C50 emits the new default; the run tier consumes it. *(Effect of the promotion, not an owned interface.)* |

**Position in the system.** C50 is **Batch-5** (component-inventory L115 — "self-optimization, research
frontier, built last") in the **Self-Optimization** subsystem, built **after Layers 1-5 are solid**
(README:280). It is **not foundational** (inventory C50: Foundational? = no) and is a **leaf control-loop**
that *composes* the self-opt tier (C46 metrics + C48 significance + C49 replay) over a **C12 variant** into
one promote/hold decision. The whole P12 layer "cannot close without" C49 (inventory critical-path #5), and
"A/B + promotion [is] absent" today (AI-CONTEXT:286) — C50 is the absent promotion half. It exists only when
the self-optimization pack is enabled (feature-gated, C03).

## 3. Interfaces / contracts

Sweep-1: interfaces **named + described**. The concrete promotion-rule schema, the metric-panel + guard
contract, the decision-record fields, the default-flip mechanism, and the exact cutline/decision-rule shape
defer to sweep-2 (frozen jointly with **C48** on the significance verdict, **C46** on the metric panel, and
**C12/C03** on the default-reference update).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Multi-metric promotion criterion + Goodhart guard** | internal (definition) | The named decision rule: **C48 significance-better** ∧ **C46 metric panel coherent** ∧ **Goodhart guard: no guard metric materially regressed**. C50 owns the *composition + guard*; each term is owned by its tier. **This is the genuine KEEP (F47/B78).** | C50 (this); C48/C46/C33 (terms) |
| I2 | **Satisfaction + guard-metric cutlines** | input (policy) | The **bars / decision rule** applied to C46/C33's statistics (the cutline C33 defers to this decision site, C33 §6). C50 owns *that bars are applied + the rule shape*; the **values** are operator/integrator policy v4 does not fix (G09; the "values question", AI-CONTEXT:516; OQ-1). | C50 (decision rule); operator (values) |
| I3 | **Promote/hold verdict + default-flip** | outbound (data + effect) | The **`promote` \| `hold`** verdict; on `promote`, **update the default formula reference** so the challenger C12 formula becomes the new default (README:276). Subject to the C56 autonomy gate (auto-flip vs. surface-for-ratification, OQ-4). | C50 (verdict + flip); C12/C03 (default reference); C56 (autonomy gate) |
| I4 | **Promotion decision record** | outbound (data) | The recorded verdict + **evidence bundle** (C48 significance verdict ref, C46 metric panel + guard check, the C12 variant id + the incumbent it replaced, sample count, timestamp/actor). Written to a bead (C20/C19), auditable + reversible. | C50 (shape); **C20** (slot), C41 (attribution) |
| I5 | **Significance-verdict intake (C48 → C50)** | inbound (read) | The C48 "was the variant actually better?" verdict + its sample/effect statistics (D-19). C50 reads it as the statistical term of I1; it computes no significance. | **C48** (verdict); C50 (consumer) |

**Invariants C50 must uphold:**
- **INV-1 (multi-metric, never single-metric — F47/B78, the load-bearing property).** A `promote` is computed
  from a **panel of ≥2 metrics moving coherently** plus the Goodhart guard — **never** from a single visible
  metric. A promotion that improves one metric while a guard metric materially regresses is **invalid**.
  *This is the whole reason C50 exists (F-MODE-COVERAGE:103/174; B78); a single-number gate would let the
  self-optimization loop Goodhart itself.*
- **INV-2 (no statistics of its own — reads C48's verdict, D-19).** C50 makes **no** significance computation
  and builds **no** estimator; "was it actually better?" is **C48's** verdict. C50 is a **decision over given
  signals** (deterministic given its inputs + the configured bars). *(Mirrors C33's reuse posture and D-19's
  routing; the bar forbids a second stats engine.)*
- **INV-3 (cutline at the decision site, not in the metric — D-15/G09).** The satisfaction (and guard-metric)
  cutlines live **in C50** (applied to C46/C33's statistics), **not** pushed into C33 (which stays
  threshold-free, C33:INV-3). C50 *applies* bars; it does not redefine the metric. The bar **values** are
  operator policy (G09; AI-CONTEXT:516), so a wrong value is a *policy* error, not a metric error.
- **INV-4 (promotion is the only act with a default-changing side effect; it is recorded + reversible).**
  Only a `promote` changes the live default formula reference; the change is **persisted with its evidence**
  (C20/C19), attributable (C41), and **reversible** (the prior default is recorded so a regressing promotion
  can be backed out). *(Because P12 self-modifies the factory, the promotion record is the audit checkpoint —
  F54 relevance, §6.)*
- **INV-5 (a failed gate is a no-op on the default).** On `hold`, the **incumbent default is unchanged** — a
  non-significant or guard-failing challenger simply does not promote; C50 does not degrade or roll back the
  incumbent and does not generate the next variant (that is C47). *(Keeps the gate conservative: the default
  only ever moves on positive multi-metric evidence.)*
- **INV-6 (recurring, not one-time; promotion-shaped, not heal-shaped).** C50 fires **whenever** a challenger
  has accumulated enough A/B evidence to be judged (recurring), distinguishing it from **C53** (one-time
  bootstrap). It owns **no** fix-loop attempt-bound / oscillation / L5-ship policy — that is **C39** (XC-3) —
  distinguishing it from the other G18 gate.

## 4. Data model / state

C50 **owns the promotion-decision contract + the default-formula selection it flips**, not durable
source-of-truth signal data. The **significance verdict** is C48's; the **metric panel** is C46's; the
**satisfaction distribution** is C33's; the **variant formula** is C12's. State C50 is the spec-of-record
for at sweep-1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Promotion decision record** | The **`promote` \| `hold`** verdict + the **evidence bundle** (C48 significance verdict ref, C46 metric panel + guard-check result, the C12 variant id + the incumbent it replaced, sample count) + timestamp/actor. The component's *output artifact*; auditable + reversible (INV-4). | Recorded on a bead (C20/C19) — a **C20 schema-slot request** (D-3), mirroring C39/C53's record-on-bead choice. | C50 (shape); **C20** (slot), C41 (attribution) |
| **Default-formula selection (the flip target)** | The **reference to the current default formula** (C12) that a `promote` updates to point at the challenger. C50 owns *that the promotion flips this reference*; the **reference itself lives in C12/C03 config** (the "Gas City formula" selection, README:276). | Config / formula selection (C03 model; C12 artifact). Prior value retained for reversibility (INV-4). | C12/C03 (reference); C50 (the flip) |
| **Promotion-rule config** | The composed rule (I1): which metrics form the panel, **which are guard metrics**, the **satisfaction + guard cutline values + decision rule** (I2), and the C56 autonomy gate for auto-flip. | Pack/config TOML (C03 model). The **cutline values are operator policy** (OQ-1), not v4-fixed constants. | C03 (model); C50 (binding) |
| **Significance verdict / metric panel (referenced, not owned)** | C48's "was it better?" verdict + C46's metric panel the rule reads. **Owned by C48 / C46**; read-only to C50. | Emitted by C48 / C46 (re-readable). | **C48**, **C46** |

> [FAITHFUL-FILL] v4 specifies the *promotion behavior* ("new variant becomes default … Gas City formula
> with statistical gate", README:276) but not C50's persisted state. The minimal faithful set is **the
> decision record** (so a self-modification of the factory is auditable + reversible, INV-4) plus the
> **default-formula reference it flips** (the observable effect of a promotion) and the rule config — **no**
> source-of-truth signal data, because the significance verdict (C48), metric panel (C46), satisfaction
> distribution (C33), and variant (C12) are owned upstream and re-readable. Recording on a bead (rather than
> a new store) mirrors C39/C53's record-on-bead choice and is a **C20 schema-slot request**, not a new C50
> store. The exact decision-record schema, the metric-panel + guard contract, the **cutline values + decision
> rule**, and the default-flip mechanism are **sweep-2**, frozen with C48 (verdict), C46 (panel), and
> C12/C03 (default reference).

**Consistency / lifecycle.** C50 stands up in **Phase 3c / Batch-5** with the self-optimization pack
(README:280, "build last"); it owns no durable truth beyond the decision record + the default-reference flip
(both derived assertions over upstream signals). The flip's consistency requirement is **evidence-coherence
+ reversibility**: a recorded `promote` must reference a real C48 significance verdict + C46 metric panel +
guard check that *existed at decision time*, and must retain the **prior default** so the promotion can be
backed out if a later measurement shows regression — the promotion is reconstructable (INV-4) even as the
factory evolves past it.

## 5. Behavior

C50 is a **control-loop** (inventory kind) but a **thin, gate-shaped** one: it has no measurement loop of its
own (that is C46→C48). Its behavior is **decision-time** — invoked **whenever** a challenger formula has
accumulated enough A/B evidence (via C48) to be judged for promotion.

**Stand up (Batch-5).** The promotion rule is configured: the **metric panel** (which C46 metrics gate),
**which metrics are guard metrics**, the **satisfaction + guard cutline values + decision rule** (I2,
operator policy), and the **C56 autonomy gate** for auto-flip. It is wired to read C48's significance verdict
and C46's metric panel, and to update the C12/C03 default-formula reference.

**Promotion evaluation (the promote/hold).**
1. **Read the evidence (I1/I5, no statistics — INV-2):** pull the **C48 significance verdict** ("was the
   challenger actually better?", D-19) + its sample/effect statistics, and the **C46 metric panel** for both
   the challenger and the incumbent default (cost-per-satisfaction, time-to-threshold, judge-FP-rate, the
   satisfaction summary from C33).
2. **Apply the multi-metric rule + Goodhart guard (I1/I2/INV-1):** evaluate **C48 significant-better** ∧
   **panel coherent (multiple metrics improved together)** ∧ **Goodhart guard: no guard metric materially
   regressed**. The satisfaction + guard bars are the **cutlines C33 defers to this decision site** (INV-3);
   their **values** are operator policy (OQ-1). Honour **sample-honesty** — a `promote` over a thin A/B
   sample must surface n (inheriting C33:INV-4 via C46); too little evidence holds (no promotion).
3. **Decide:**
   - **`promote`** → **flip the default formula reference (I3/INV-4):** subject to the **C56 autonomy gate**,
     update the default to the challenger C12 formula (auto-flip at high autonomy; **surface for human
     ratification** at lower autonomy, README:498/527). Retain the prior default for reversibility.
   - **`hold`** → **no-op on the default (I5/INV-5):** the incumbent stays; the loop keeps measuring / C47
     proposes the next variant. C50 does not generate the next challenger.
4. **Record the decision (I4/INV-4):** write **`promote` \| `hold`** + the **evidence bundle** (C48 verdict
   ref, C46 panel + guard check, variant id + replaced incumbent, sample count) to a bead (C20/C19),
   attributed (C41), auditable + reversible.

**Re-evaluation / recurrence (INV-6).** C50 is re-invoked for **each** challenger that accumulates enough
A/B evidence; each evaluation records its own decision. A promoted formula becomes the incumbent the **next**
challenger is measured against — the gate is the recurring choke point of the self-optimization loop. C50
owns no source-of-truth; re-reading current C48/C46 signals reproduces the verdict.

> The exact promotion-rule grammar, the **metric-panel + Goodhart-guard contract** (how "moving coherently"
> and "materially regressed" are operationalised over C46's statistics), the **cutline values + decision
> rule** (a satisfaction quantile? a per-metric bar vector? a dominance condition over the panel?), the
> **default-flip mechanism** (C12/C03 reference update), and the **C56 autonomy gate** are **sweep-2+**
> (frozen with C48 + C46 + C12/C03 + C56). C50 invokes **no** model and runs **no** significance test
> (significance is C48; D-19).

## 6. Failure modes & handling

C50 owns the **promotion-decision + Goodhart-guard half of G18** at this component — **distinct** from C39's
fix-loop termination half (the other G18-tagged gate).

**G18 (blocker) — handling at C50: the promotion gate, NOT the fix-loop termination.** The inventory tags
**both C50 and C39** with **G18**, but they address different halves of the same "a loop has no stated
bound" concern, and the routing is already settled:
- **C39 owns the *self-heal* loop's numeric termination policy** — N-attempts → escalate, F52 oscillation
  detection, L5 ship-authorization (**XC-3**: "C39 OWNS the G18 numeric termination policy"; D-18/C39 §1).
  C50 owns **none** of this — no attempt bound, no oscillation guard over fix cycles, no fix-ship authority.
- **C50 owns the *promotion-decision + Goodhart guard*** — the steady-state "does this variant become the
  default?" gate (README:276). C50's contribution to G18's spirit ("a loop with no stated bound") is that
  the **self-optimization loop terminates each cycle in a recorded, multi-metric, Goodhart-guarded
  promote/hold decision** (INV-1/INV-4) rather than drifting: a variant only becomes the default on
  **positive multiple-metric + significant** evidence, and the decision is **recorded + reversible** so a
  bad promotion can be backed out. C50 is the **choke point** that keeps the measure→variant→promote loop
  from silently re-defaulting the factory on a single gamed metric.
  > [AMBIGUITY: G18] G18 is stated as a **self-healing** loop-closure gap (ambiguities-and-gaps:51 —
  > "anomaly → diagnosis → fix → ship") yet is tagged on **both** C39 (self-heal) **and** C50 (promotion).
  > Two readings: **(a)** G18 is *only* the fix-loop bound, and its appearance on C50 is incidental
  > (C50 has nothing to add); **(b)** G18 generalises to *any* unbounded self-modifying loop, so the
  > **promotion loop** also needs a stated, recorded stopping rule. **Chosen: (b)**, scoped narrowly — the
  > *numeric fix-loop* policy is unambiguously **C39's** (XC-3, binding), so C50 does **not** duplicate it;
  > C50's G18 contribution is the **promotion-decision rule itself** (multi-metric + Goodhart-guarded +
  > recorded), which is the promotion loop's "stated bound" (it cannot promote without clearing the gate,
  > and every cycle ends in a recorded verdict). Reading (a) is rejected because the inventory **explicitly
  > tags C50 with G18** and frames C50 as a *gate* (a stopping rule by nature); reading (b) is the minimal
  > way to honour that tag **without** colliding with C39's owned numeric policy (XC-3). **Note** the G18 gap
  > *text* (ambiguities-and-gaps:51) names only the fix loop and says nothing of promotion — so C50's G18
  > tag rests on the **inventory tag + C50's gate-by-nature role**, not on the gap text; the **numeric
  > fix-loop** half (N-attempts / oscillation / L5-ship) stays entirely C39's, and C50 adds only the
  > promotion loop's recorded stopping rule.

**F47 (Goodhart on visible metrics) — ADDRESSED HERE (this is C50's reason to exist).** v4 mandates the
guard at C50 by name: *"promotion gate requires multiple metrics moving together"* (F-MODE-COVERAGE:103),
*"… moving coherently. Goodhart applies and v4 should not pretend otherwise"* (F-MODE-COVERAGE:174), B78
*"multi-metric mandatory; no single visible target"*. C50 closes F47 at the promotion site by making the
criterion **multi-metric + guard-checked** (INV-1): a challenger that buys one visible metric (satisfaction)
by regressing another of C46's named meta-metrics (cost-per-satisfaction, time-to-threshold, judge-FP-rate)
**does not promote**. C50 does **not** eliminate Goodhart — "Goodhart applies recursively to meta-metrics"
(F-MODE-COVERAGE:63) — it makes the *promotion decision* resistant to single-metric gaming and **recorded**
so a drift is auditable.

**What C50 does NOT resolve (honest residual).** C50 makes the *promotion* multi-metric + recorded but
inherits open questions: the **cutline values + which metrics are guard metrics** are operator policy
(G09/OQ-1, the "values question", AI-CONTEXT:516, shared with C33/C53/C39); **how "moving coherently" /
"materially regressed" is operationalised** over C46's statistics is a sweep-2 decision-rule choice (OQ-2);
**who authorizes an auto-flip vs. ratification** ties to C56's autonomy ladder (OQ-4); and **recursive
Goodhart on the meta-metrics themselves** (F47 applies to C46's metrics, F-MODE-COVERAGE:63) is *mitigated*
(multi-metric, no single target) but not *eliminated* — the residual lives at C57's F-mode map + the F54
audit pack (G35).

**Other failure cases.**
- **C48 verdict absent / inconclusive / not-significant.** → **`hold`** (no promotion) with the reason
  recorded; never a `promote` on missing or non-significant evidence (INV-1/INV-2). *[FAITHFUL-FILL: v4
  silent; refusing to promote without a significant C48 verdict is the minimal honest reading of "statistical
  gate", README:276, and is exactly D-19's significance→C48 boundary.]*
- **A guard metric regresses while the primary improves.** → **`hold`** — the Goodhart guard is part of the
  **conjunction** (INV-1): a satisfaction gain does **not** override a cost-per-satisfaction (or
  time-to-threshold) regression. *(This is the F47 guard made load-bearing, F-MODE-COVERAGE:174.)*
- **Thin A/B sample.** → n is surfaced (inheriting C33:INV-4 via C46); a too-small sample is weak evidence
  and holds (no promotion) until C48's significance verdict is credible. *(Sample-honesty mirrors C53:INV
  small-n handling.)*
- **A promotion later shows regression in production metrics.** → because the prior default is retained
  (INV-4), the promotion is **reversible**; backing it out is a default-reference flip back to the incumbent.
  *(C50 names reversibility; an automated regression-triggered rollback policy is a sweep-2/operator
  decision, OQ-3 — C50 does not build a rollback engine at sweep-1.)*

> F-mode applicability is owned by **C57**. C50 underwrites the property that promotions are **multi-metric +
> Goodhart-guarded** (F47), **significance-gated** (against F9 spec-overfitting — a variant that overfits the
> held-out scenarios should not clear **C48's significance verdict** computed over those held-out runs, so
> the F9-resistance flows through the C48 term, not a standing C46 metric), and **recorded +
> reversible** (F54 — promotion is a self-modification of the factory; the recorded, evidence-anchored,
> reversible decision *reduces blast radius* but does **not** *enforce* against objective drift — that is
> C43 / the F54 audit pack, G35). C50 defers the canonical F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C50 is held to *only* the 12-principle capability it
uniquely adds — the **multi-metric, Goodhart-guarded promotion decision + the default-flip + the recorded,
reversible verdict** — and **nothing the existing stack already does**. **Dropped / refused as non-principle
or not-C50's:** (1) the **statistical-significance test** ("was it actually better?") — that is **C48's**
(D-19); C50 *consumes* the verdict and re-runs no stats; (2) the **meta-metric definitions + cost model** —
that is **C46's** (G32); C50 *reads* the panel; (3) **recomputing satisfaction / owning the threshold-free
distribution** — that is **C33's**; C50 *applies* a cutline, it does not recompute the metric (D-15/G09);
(4) the **variant generator** (DSPy/Optuna) — that is **C47's**; C50 decides a *given* challenger, it does
not propose; (5) the **counterfactual-replay driver** — that is **C49's** (G19); (6) the **fix-loop numeric
termination policy** (N-attempts/oscillation/L5-ship) — that is **C39's** (XC-3); C50 owns no fix-loop
policy; (7) **inventing the cutline values / which metrics are guards** — operator/integrator policy v4 does
not fix (G09/OQ-1; AI-CONTEXT:516); (8) a heavyweight **rollback/experiment-registry engine** — MLflow/W&B
cover experiment tracking (AI-CONTEXT:362); C50 keeps only the **reversibility hook** (retain prior default),
not a bespoke registry. What is **kept**: the **multi-metric promotion rule + Goodhart guard** (the genuine
F47 KEEP), the **promote/hold verdict + default-flip**, the **recorded + reversible decision**, and the
**placement of the cutline at this decision site** (D-15/G09) — the genuinely load-bearing, currently-absent
promotion half (AI-CONTEXT:286 "A/B + promotion absent").

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C50 reads **verdicts/metric-panels about** variants (C48 significance, C46 metrics), not raw
  prompts/outputs; it inherits C19's access posture and adds no new exposure. It performs **no model call**
  (no judge credential). Its security *relevance* is that **a promotion self-modifies the live factory**
  (it flips the default formula) — so the **C56 autonomy gate** on the flip (OQ-4) and the **recorded +
  reversible** decision (INV-4) are governance controls (F54/G35), though C50 is not the RSI *enforcement*
  mechanism (that is C43 / the F54 audit pack).
- **Cost.** Negligible per decision — C50 reads already-computed signals (C48 verdict, C46 panel) and records
  one decision + (on promote) one reference flip; **no model tokens, no managed store**. The *A/B-test +
  replay* tokens are C48/C49's cost; C50 adds none. (The cost *model* itself — cost-per-satisfaction — is
  C46/G32, and *is* one of C50's guard metrics, so the gate is cost-aware by construction.)
- **Scale.** Low — one decision per challenger that clears C48 (recurring but not high-frequency; the
  measure→variant→A/B pipeline upstream sets the cadence). No bespoke scaling machinery is warranted at
  sweep-1 (the bar).
- **Observability.** C50 **is** a governance/observability artifact — the promote/hold decision + its
  evidence + guard check is the headline record of *every self-modification of the factory's default
  methodology*. The decision (and the prior-default it can revert to) is the thing being **audited** (INV-4);
  C50 emits the verdict as a recorded bead, not a heavy stream.
- **Ops.** Control-loop configured + evaluated with the self-optimization pack in Batch-5 (README:280, "build
  last"). The **cutline values, the guard-metric set, and the C56 autonomy gate** are operator-set config
  (C03; OQ-1/OQ-4). Pin the self-opt tier's versions (C46/C48) so a recorded promotion is reproducible.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep-2).

1. **AC-1 (multi-metric, never single-metric — INV-1/F47/B78):** a `promote` is computed from a **panel of
   ≥2 metrics moving coherently** + the Goodhart guard, **never** from a single visible metric; a promotion
   that improves one metric while a **guard metric materially regresses** is **rejected** (held).
2. **AC-2 (significance consumed from C48, not recomputed — INV-2/D-19):** C50 makes **no** significance
   computation and builds **no** estimator; "was it actually better?" is read as **C48's** verdict.
   (Verifiable: C50 runs with no stats library configured; a non-significant/absent C48 verdict ⇒ `hold`.)
3. **AC-3 (cutline at the decision site — INV-3/D-15/G09):** the satisfaction + guard bars are **applied in
   C50** to C46/C33's statistics (C33 stays threshold-free); the bar **values + which metrics are guards**
   are configurable operator policy, not hard-coded constants.
4. **AC-4 (promote flips the default; hold is a no-op — INV-4/INV-5):** a `promote` **updates the default
   formula reference** to the challenger C12 formula (subject to the C56 autonomy gate); a `hold` leaves the
   incumbent default **unchanged**.
5. **AC-5 (decision recorded + reversible — INV-4):** every verdict is persisted with its **evidence bundle**
   (C48 verdict, C46 panel + guard check, variant id + replaced incumbent, n) on a bead (C20/C19),
   attributable (C41); a promotion **retains the prior default** so it can be backed out.
6. **AC-6 (Goodhart guard is load-bearing — INV-1):** a satisfaction gain does **not** override a guard-metric
   (e.g. cost-per-satisfaction or time-to-threshold) regression — the rule is a **conjunction** including the guard.
7. **AC-7 (recurring, not one-time — INV-6):** C50 fires for **each** challenger that clears C48; a promoted
   formula becomes the incumbent the next challenger is measured against. (Distinct from C53's one-time gate.)
8. **AC-8 (no fix-loop policy — INV-6/XC-3):** C50 owns **no** N-attempts/oscillation/L5-ship policy — that
   is **C39's** (the other G18 gate). C50's only loop role is the promote/hold gate over A/B evidence.
9. **AC-9 (engine-reuse, no second stats/metric engine — the bar):** the gate composes **C48 (significance) +
   C46 (metrics) + C33 (satisfaction) over a C12 variant**; **no** bespoke significance test, metric
   definition, variant generator, replay driver, or experiment registry is present.
10. **AC-10 (autonomy-gated flip — OQ-4):** whether a `promote` **auto-flips** the default or **surfaces for
    human ratification** is gated on the **C56** authorized autonomy level (README:498/527); C50 does not
    self-authorize a silent re-default below the configured level.

**Test strategy.** A **promotion-gate harness** that drives a synthetic promote/hold decision over seeded
inputs — a **C48 significance verdict** (significant-better / not-significant / inconclusive / absent), a
**C46 metric panel** (challenger vs. incumbent, varied: all-metrics-up; satisfaction-up-but-cost-up — the
Goodhart case; thin-sample), a **C12 challenger formula id**, and a **C56 autonomy level** (auto-flip vs.
ratify) — and asserts AC-1…AC-10: in particular that the verdict is a **multi-metric conjunction with a
Goodhart guard** (AC-1/AC-6), that **significance is consumed not recomputed** (AC-2), that the **bars are
applied here and configurable** (AC-3), that **promote flips the default and hold is a no-op** (AC-4), that
the decision is **recorded + reversible** (AC-5), that it is **recurring** (AC-7) and owns **no fix-loop
policy** (AC-8), and that **no second stats/metric engine** exists (AC-9). The harness's headline assertion
is the **Goodhart case** (AC-1/AC-6): satisfaction up + cost-per-satisfaction up ⇒ **hold**, not promote.

## 9. Open questions

- **OQ-1 (→ review-log, top): G09 promotion cutline values + guard-metric set.** §6 binds C50 to **apply**
  the satisfaction + guard cutlines (D-15/G09) at this decision site, but the **values** + **which C46
  metrics are guard metrics** are operator/integrator policy v4 does not fix (the "values question",
  AI-CONTEXT:516). Confirm the cutline lives at C50 (not C33), that its values are policy (shared with
  C33:OQ-1, C53:OQ-1, C51:OQ-C51-3), and freeze the guard-metric set at sweep-2 with C46/C33.
- **OQ-2 (→ review-log): the multi-metric decision rule shape.** How "**moving coherently**" and "**materially
  regressed**" are operationalised over C46's statistics — a per-metric bar vector? a Pareto-dominance
  condition over the panel? a weighted composite under a no-regression constraint? — is unfixed at sweep-1.
  Freeze the decision rule at sweep-2 with C46/C48 (it must stay **multi-metric**, INV-1/F47).
- **OQ-3 (→ review-log): reversibility / regression-triggered rollback.** INV-4 requires the prior default be
  **retained** so a regressing promotion can be **backed out**, but whether back-out is **operator-manual**
  or an **automated regression-triggered rollback** (on a later C46 measurement) is unfixed. Freeze the
  rollback policy at sweep-2; do not build a rollback engine at sweep-1 (the bar).
- **OQ-4 (→ review-log): C56 autonomy gate on the default-flip.** Whether a `promote` **auto-flips** the live
  default or **surfaces for human ratification** is gated on C56's authorized autonomy level (README:498
  "required until P12 is mature and trusted"; :527). Confirm the C50↔C56 seam (parity with C39's L5
  ship-authorization gate, C39 §3.2) and who authorizes auto-flip — freeze at sweep-2 with C56.
