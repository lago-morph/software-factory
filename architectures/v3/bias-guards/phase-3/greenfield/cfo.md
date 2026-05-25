---
guard: cfo
target: draft-greenfield-synthesis
phase: 3.2
based-on-commit: e02d0ba
based-on-date: 2026-05-25
---

# Phase-3.2 CFO critique — greenfield draft

## §1 Persona stance

I am reading this architecture as the person who signs the cloud bill. The draft is unusually disciplined about *naming* cost ceilings (ROBUST-G13, D-5) but unusually careless about *budgeting against the primitives it mandates everywhere else*. Cross-model judge, paraphrase fan-out, AILCCP immutable log, STIR-cascade, four-guards perimeter, and operator labor stack multiplicatively at cold-start — and the draft treats each as if its cost were a methodology parameter rather than a structural commitment. The 10× CTR-E1 variance is described as "a parameter, not a contention" (ROBUST-G13), which is precisely the move that lets the architecture book the *low* end of the range as a default while structurally requiring the *high* end.

## §2 Top cost findings

### Finding C-1 — ROBUST-G10 + ROBUST-G15 force cross-family at cold-start with no cost budget declared (HIGH)

Cross-family judging is structurally ~2× per-cycle inference cost. Combined with GF-C's "cross-model judge with mandatory escalation on disagreement" at every cold-start cycle, this is ~2× tokens. CTR-D7 names a corpus-anchored alternative (Anthropic's "same-model judging is usually fine") which would cut judge cost by half. The draft adopts the *expensive* side at cold-start with the rationale that Anthropic presupposes a track record (ROBUST-G10), but does not declare the cost of that decision against a budget.

If GF-C's four graduation criteria each take W cycles to demonstrate (DPG-4: "≥M consecutive cycles agreement," "≥5 invocations × ≥3 scenarios"), then graduation-per-work-unit-class costs ≥ 15 cycles × 2× judge multiplier. Cold-start covers all work-unit-classes (5 in brief glossary §0). 15 × 2 × 5 = ~150 "judge units" *per factory* before any unit is automation-eligible. At Cherny's anchor that's ~6 figures; at the noosphr lower bound it's ~$15K *just to graduate*.

### Finding C-2 — Paraphrase fan-out (GF-M's F37 mitigation) compounds with cross-family judge (HIGH)

ROBUST-G8 makes contradiction detection dependent on "behavioural disagreement across model-family-diverse paraphrasers." With N paraphrasers (K=5 paraphrase robustness from report 09 §5.5, requiring 3-of-5 or 5-of-5 agreement), the spec-authoring step alone is 5× cost. Combined with ROBUST-G10's ~2× cross-family judge, one bootstrap cycle's *inference cost alone* is ~5× spec + 2× build-judge = 7× a naive cycle. GF-M OQ-T2 explicitly flagged this.

Jaymin's cost spread observation (report 09 §line 162): "10–20× cost spread; homogeneous model assignment is named an anti-pattern." Critically, the corpus describes the 10–20× spread as something a *smart* model-per-task assignment achieves — the draft's primitives instead *require* expensive models at *both* spec-authoring (paraphrase) *and* judge (cross-family) layers.

### Finding C-3 — D-7 trajectory capture + AILCCP immutable logging at multi-cycle parallelism (MEDIUM-HIGH)

OpenHands V1 measurement: per-event persist 0.20ms median / 0.31ms p95 on 433 SWE-Bench Verified replays / 39,870 events — a *single-stream* measurement, not multi-stream concurrency stress test. When cross-family judge says cross-family, AILCCP says immutable-log, ROBUST-G14 says STIR-cascade, and GF-M's paraphrase fan-out drives ~5× event volume, the per-event persist cost stays sub-ms but the *event count* per cycle multiplies. The draft cites this number "as feasibility evidence, not as normative dependency" per brief §0 — which is the *right* hedge, but the draft does not then bound the cost at the parallelism it actually proposes.

### Finding C-4 — CTR-E6 CaMeL 7-point utility tax across four-guards cascade is not budgeted (MEDIUM)

ROBUST-G9 declares CaMeL "with ~7-point utility tax accepted per CTR-E6," anchored as a *four-layer cascade* (lumper Cluster-10). Followup 08 §3 says verbatim: *"the figure is a headline number averaged across models and AgentDojo suites; per-suite and per-model variance is large (Travel suite is the dominant degradation; for some models/suites CaMeL even improves utility)."* Four-layer cascade utility-tax is not in the corpus; the draft has imported a single-layer number to defend a four-layer commitment.

### Finding C-5 — Operator labor as a cost is *named* but *not budgeted* (HIGH)

Three tracks converge on "operator labor is irreducible at bootstrap." Draft ROBUST-G14 hides this behind "substrate scaffolds the operator." The architecture mandates (at minimum, at cold-start): 9-field intent block authorship; ≥3 region-shaped Kaner scenarios; STIR-cascade reflection prompts; cross-model-disagreement escalations; F40 last-mile drift; RSI-declaration day-0 board reporting; regime declaration per work-unit-class. None quantified against operator hours. CTR-A6 (Willison "fire up four agents, by 11am I am wiped out") is the *only* corpus anchor for operator cognitive ceiling, and it is invoked nowhere in the draft.

Report 09 §line 224: *"the 25-agent swarm at $100/hour matches one senior engineer's daily loaded cost while delivering 25× parallel throughput — if work is decomposable."* The *if* is the load-bearing word.

## §3 What's actually cost-defensible

ROBUST-G13's elevation of D-5 to non-optional with three-axis ceilings (tokens, wall-clock, tool-call-count) is corpus-grounded (report 09 anchoring three-granularity ceilings: per-agent / per-task / daily-swarm). The acknowledgement that cold-start cycles must be bounded smaller than steady-state cycles (GF-C §1.2 sub-phase C "deliberately tiny") is sound. ROBUST-G6's deterministic GtWR/EARS lint at "zero marginal cost" is genuinely cheap — it correctly refuses LLM-judge at the authoring boundary and so escapes the cost-stacking problem.

The draft's *bootstrap protection set* (§1.4 ROBUST-G15 through G19) is correct in shape but mis-priced as a *package*. Each protection is individually defensible; stacked at the bootstrap regime they are unbudgeted.

## §4 Concrete recommendations for Phase-3.4

1. **A cost-per-graduation specification is missing and must be added to DPG-4.** GF-C's four graduation criteria carry a *measured* cost-per-criterion column. The Phase-5 wave-1 ADR DPG-4 names ("Empirical-bar source for automation-eligibility") must declare cost-per-graduation per work-unit-class as a first-class parameter.

2. **A Phase-5 ADR is needed: "Per-work-unit-class cost ceiling under stacked guards."** D-5 currently says ceilings are enforced; the ADR must specify how the ceiling accommodates the multiplicative load of ROBUST-G8 paraphrase fan-out (N×), ROBUST-G10 cross-family judge (2×), ROBUST-G14 STIR-cascade per-cycle (operator-time), ROBUST-G19 AILCCP immutable log (storage + audit replay).

3. **A Phase-5 ADR is needed: "Cascade utility tax under four-guards stacking."** ROBUST-G9 has imported CaMeL's 7-point single-layer tax to defend a four-layer cascade. Phase-5 must declare either (a) budget for cascade-level utility tax measured *as cascade*, or (b) cheaper non-CaMeL implementations at the inner three.

4. **A Phase-8 lean-evaluation brief must measure cost-per-cycle under realistic load.** Briefs should require: token spend per cycle by phase; judge cost as a fraction of total; paraphrase fan-out cost as separate line item; operator-minutes per cycle; AILCCP storage cost per 1000 cycles.

5. **DPG-7 must absorb a cost dimension.** STIR-cascade-as-substrate fires reflection prompts on *every* structural moment; at Willison's 4-agent ceiling that operator runs out of attention budget. Substrate-fired escrow is *not free* even if substrate-typed.

6. **ROBUST-G13's "10× variance is a parameter, not a contention" is the wrong framing.** A 10× variance in a non-optional ceiling means the architecture *commits to enforcing the lower end as policy*. Phase-3.4 should require the draft to *commit* to a default ceiling (noosphr $500/day floor, Jaymin $100/hour Gas Town anchor, or Cherny $100K/month ceiling).

**Bottom line.** The draft has correctly named most of the cost-relevant primitives but treats their cost as a Phase-5/6 problem to be deferred. The cost-stacking at cold-start (paraphrase × cross-family judge × immutable log × STIR × operator attention × CaMeL cascade) is the architecture's single largest unsurfaced exposure.
