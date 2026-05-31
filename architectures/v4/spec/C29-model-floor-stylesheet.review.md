# Adversarial review — C29 Model floor & stylesheet routing (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Agent Loop / model routing
Target: spec/C29-model-floor-stylesheet.md (+ plan-faithful/C29-model-floor-stylesheet.md)
Charter: single canonical track. Track-A posture in force — attack FIDELITY and COMPLETENESS, NOT the
design — PLUS the capability-for-principle bar (HANDOFF §2 / SURVIVOR-PASS): flag any addition that is
hardening on existing stack capability rather than new capability tied to a 12-principle.

Grounding for the bar on this component (SURVIVOR-PASS C29 row): the only KEEP-MINIMAL survivors are
**DELTA-01** (`model_family` [+ `independence_class`] as a registry field — serves **P2** provider-
abstraction) and **DELTA-02** reduced to *"policy is gradable, L1 default"* (serves **P5**; the L1
baseline is already in via **D-1**). The four DROPs / over-builds to flag if present: a **compiled
deterministic routing function** (DELTA-04), **cost-tier as a live budget-aware input** (DELTA-05), a
**fail-closed + `degraded_eval` escape** (DELTA-06), and a **metered-API judge-seat credential**
(DELTA-03 = FE-1). Cross-family/cross-provider judging is **FE-1**, not Phase-0 (D-1).

## Findings

### RC29-01 — major — Plan freezes "family at PROVIDER granularity (resolves G08 reading (a))" as the Phase-0 contract — contradicts D-1 and the spec's own §9
**Claim.** `plan-faithful` §4 contract-milestone 1 (line ~39) says: *"`modeldb` entry shape `{id, family,
cost_tier}` with **family at provider granularity** (resolves G08 reading (a)). Freeze first."* and T2
(line ~11) types it *"family(provider-level)"*. **Evidence/reasoning.** D-1 resolves the Phase-0 baseline
to the **same-provider** judge; the spec §9 states this explicitly — *"effectively reading (b) for Phase
0"* — and reclassifies the **provider-level reading (a)** (the literal README:189 cross-provider rule) to
**FE-1**. Reading (a) / provider-granularity cross-family enforcement is precisely the deferred FE-1 thing
(FUTURE-ENHANCEMENTS FE-1; SURVIVOR-PASS C29-03 DROP). So the plan freezes, as the *Phase-0* contract, the
very reading D-1 pushed to the future, and it directly disagrees with its own spec on which G08 reading is
canonical for Phase-0 (plan says (a); spec says (b)). This is a D-1 fidelity violation **and** a cross-
artifact contradiction. **Fix (applied).** Reworded milestone 1 and T2: the `family` label is stored on
every registry entry (granularity is a sweep-2 detail), Phase-0 uses **reading (b)** / same-provider per
D-1, and **provider-granularity cross-family/cross-provider enforcement is FE-1** — not the frozen Phase-0
contract. The field still freezes early as the FE-1 seam; only the "(a)" framing was wrong.

### RC29-02 — major — Spec encodes its KEPT "gradable, L1-default" capability only by POINTING at the frozen optimized sibling, not natively in the canonical track
**Claim.** The survivor-pass keep for C29 DELTA-02 is *"policy is gradable, L1 default"* (P5). In the
faithful spec the **only** place "L1" appears is §6's ruling block (line ~78): *"see the optimized
sibling's L1 default, which D-1 confirms is correct."* The canonical spec never states, in its own voice,
that the judge-independence policy is gradable or that **L1 (same-provider, prompt/role/rig-isolated) is
the Phase-0 default**. **Evidence/reasoning.** `spec-optimized/` is **frozen reference** (HANDOFF; the
per-dir READMEs); the single canonical track must carry its own kept capability rather than delegate the
definition to a frozen doc a future reader is told *not* to author against. This is a completeness gap on
the one P5 capability the survivor pass kept — and a fidelity weakness (the canonical artifact's behaviour
is defined by reference to an archived sibling). **Fix (applied).** Stated the kept capability natively in
§6 and §3: the judge-independence policy is **gradable**, and **L1 — same-provider, prompt/role/rig-
isolated — is the Phase-0 default per D-1**; cross-family/cross-provider (the stronger levels) are FE-1.
Kept the D-1 grounding; demoted the optimized-sibling mention to a non-load-bearing "cf." pointer.

### RC29-03 — minor — §3 `crossFamilyRule` invariant is stated in its strong (fail-closed-shaped) form before I2 relaxes it
**Claim.** §3 lists `crossFamilyRule(coderModel) → constraint` with **"Invariant: … `family(judge) ≠
family(coder)`"** stated unconditionally (line ~36); I2 three lines later relaxes it to advisory at
Phase 0 (D-1/FE-1). **Evidence/reasoning.** Stating the invariant in absolute form at the interface, then
relaxing it in the invariants list, reads as a latent contradiction and risks a downstream consumer
(C32/C34) binding to the strong form. Keeping the `crossFamilyRule` *emitter* as the FE-1 seam is correct
(FUTURE-ENHANCEMENTS asks for exactly this hook) — only the unconditional invariant wording is off.
**Fix (applied).** Annotated the `crossFamilyRule` interface line to mark the `family(judge) ≠
family(coder)` constraint **advisory/relaxed at Phase-0 (active enforcement = FE-1)**, cross-referencing
I2, so the interface and the invariant list agree.

### RC29-04 — minor — §6 F1 row cites the (deferred) cross-family rule as the active Phase-0 guard
**Claim.** §6 F1 row: *"Cross-family judge rule (on the stylesheet) is part of the guard | Addressed."*
**Evidence/reasoning.** Under the Phase-0 L1 baseline the **cross-family** rule is *not* active (it is
FE-1); the active guard is prompt/role/rig isolation of the same-provider judge — which is exactly how the
F27/F46 rows in the same table were (correctly) rewritten. Citing the deferred mechanism as the live guard
for F1 is stale wording, not a status error (F-MODE-COVERAGE marks F1 Addressed at the v4 level; the spec
mirrors that). **Fix (applied).** Reworded the F1 mechanism to the Phase-0 guard (judge-independence
policy ≥ prompt/role isolation; cross-family strengthening = FE-1), consistent with the F27/F46 rows.

### RC29-05 — minor — `independence_class` registry field named in the survivor keep is absent from the spec's `modeldb` shape (consistent with the adopted apply outcome — recorded, not a defect)
**Claim.** SURVIVOR-PASS DELTA-01 title keeps *"model_family **+ independence_class** as registry
fields"*, and the dispatch brief names *"a `model_family`/`independence_class` registry field."* The
faithful registry is `{id, family, cost_tier}` (§4 / plan T2) — no `independence_class`.
**Evidence/reasoning.** The binding **APPLY RESULTS** (SURVIVOR-PASS Phase-2, line ~485) mapped the C29
keep to exactly `{id, family, cost_tier}` and declared it already-present with *no edit*; the capability-
to-principle table (line ~444) reduces the keep to the `model_family` field alone. So the spec is
**consistent with the adopted outcome**; `independence_class` is the *optimized* sibling's orthogonal axis
(its §3b), which is an L2/L3 (FE-1) construct. Adding it to the canonical Phase-0 registry would import
FE-1 structure the apply pass deliberately did not pull in. **Recorded, not fixed.** Flagged here only so
the orchestrator is aware the brief's "/`independence_class`" half was dropped at apply time; see
DEFERRED note below.

## Over-build / capability-for-principle audit (the bar) — PASS

The faithful C29 correctly stays on the right side of all four DROP triggers; no scope-creep finding:
- **Compiled deterministic routing fn (DELTA-04) — absent.** I3 keeps determinism as a *property*
  ("same node + same stylesheet → same model … lintable/auditable like other v4 deterministic rules,
  cf. F51"), not a compiled decision function. Faithful and within v4.
- **Cost-tier as live budget-aware input (DELTA-05) — absent.** §7 keeps `cost_tier` a *preference label*
  and defers the cost model to C46; plan §5 explicitly says *"Keep cost-tier a preference label only; do
  NOT build a cost model here."* Correct.
- **Fail-closed + `degraded_eval` escape (DELTA-06) — absent.** I2 / §6 ruling block state the constraint
  is *"advisory/relaxed at Phase 0, **not fail-closed**."* Correct (D-1).
- **Metered-API judge-seat credential (DELTA-03 = FE-1) — absent.** §6/§9 treat sourcing the second
  family as an upstream dependency / **FE-1 (future)**; no judge seat proposed. Correct.

Independence is **not over-claimed** under L1: F46 and F48 are marked **Partial at Phase-0** (cross-family
ensembles / shared-training residual deferred to FE-1), F27 "Addressed at Phase-0 isolation level
(cross-provider strengthening = FE-1)." G32 is **deferred with reason** (C46 owns cost-per-satisfaction
per inventory). Source header (README:189/427, §304, §514; AI-CONTEXT §4.1/§6.2; F-MODE §6 F19/F31)
verified line-by-line against the v4 docs — accurate.

## Deferred (needs orchestrator decision)

- **DEFERRED — `independence_class` field (RC29-05).** Whether the canonical Phase-0 `modeldb` should
  carry `independence_class` (per the dispatch brief + DELTA-01 *title*) or stay `{id, family, cost_tier}`
  (per the adopted APPLY RESULTS) is an architecturally-significant labeling call that the survivor-pass
  apply already decided one way. Not applied unilaterally — left for the orchestrator to confirm whether
  the apply-time reduction stands or the field should be reinstated as the FE-1 seam.

## Verdict
**accept-with-fixes.** Faithful and well-traced; the bar is respected (zero over-build — all four DROP
triggers correctly avoided, independence honestly hedged at Phase-0, G08/G20 routed to D-1/FE-1, G32
deferred to C46). Two real defects fixed in place: a **plan↔spec contradiction that froze the FE-1
provider-granularity reading as the Phase-0 contract** (RC29-01, the most serious — a D-1 fidelity
violation) and the **kept "gradable, L1-default" capability being defined only by reference to the frozen
optimized sibling** (RC29-02); two minor wording fixes applied (RC29-03/04). One labeling question
(`independence_class`) deferred to the orchestrator. No fidelity blockers; nothing else architectural.
