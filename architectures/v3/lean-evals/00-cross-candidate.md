# Cross-candidate evaluator-brief — Phase 8 Wave 8.2

**Author.** Phase-8 lead agent, post-Wave-8.1.b close (2026-05-28).
**Authorship path.** Lead-agent-default per [`auto-008 §Decision (Round 2)`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2). Subagent-fallback condition (≥3 unified-attempt rewrite-§3 verdicts) NOT TRIGGERED per [`cross-check-falsifier.md`](cross-check-falsifier.md) — 0 unified-attempt rewrites.
**Inputs.** 10 finalized per-candidate lean-eval briefs at [`lean-evals/<id>.md`](.) (gf-s, gf-m, gf-c, bf-s, bf-m, bf-l, u-a, u-b, u-c, d7-u-1) + 3 cross-candidate bias-guard audits at [`audit-*.md`](.) + the [`auto-008` dispatch brief](../decisions/auto-008-phase-8-dispatch-shape.md).

---

## TL;DR (≤200 words)

This brief is the cross-candidate read of Phase-8's 10 per-candidate lean-evals. It names: (a) the **DEC-1.a falsifying result pattern** (verbatim from the [hypothesis-falsifier audit](audit-hypothesis-falsifier.md) — the load-bearing pattern Wave 8.2 must commit BEFORE downstream simulator-harness execution per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing)); (b) the **5 cross-candidate comparison axes** (mandate-coverage / falsifier-discipline / practitioner-relevance / cite-obligation-honoring / scenario-set-source) used by the downstream simulator-harness to pressure-test candidates against each other; (c) the **practitioner-relevance weighting** (per the [domain-practitioner audit](audit-domain-practitioner.md) load-bearing finding: 3 unified-attempts are falsifier-mechanically-sound but practitioner-thin); (d) the **per-candidate engagement matrix** (which candidates can falsify DEC-1.a and how; which carry implementation noise risk); (e) the **U-B honest-degradation reconciliation** flagged by the hypothesis-falsifier; (f) the **downstream simulator-harness handoff posture**. The brief does NOT pre-judge the DEC-1.a outcome — Phase-8 lean-eval execution is the falsification surface, not this design layer.

## §1 Cross-candidate comparison axes

Per [`auto-008 §Decision (Round 2) Wave 8.2`](../decisions/auto-008-phase-8-dispatch-shape.md#decision-round-2): the cross-candidate evaluator-brief names the comparison axes a downstream simulator-harness uses to pressure-test the 10 candidates against each other. 5 axes:

1. **Mandate-coverage axis.** Does the candidate's lean-eval cover its declared mandate (per `candidate-mandate` YAML)? For mandate-aligned candidates (GF-S/GF-M/GF-C/BF-S/BF-M/BF-L), the single-bloc form applies. For unified-attempts (U-A/U-B/U-C/D7-U-1), both blocs must be covered with ≥3 scenarios each per [R6 #1 amendment](../decisions/auto-008-phase-8-dispatch-shape.md#round-2-reviewer-amendments-folded-post-round-2-patches). **All 10 candidates passed this axis at Wave 8.1.b** per [falsification-designer audit](audit-falsification-designer.md).

2. **Falsifier-discipline axis.** Does the candidate's §3 falsifying-outcome pass the 4-item rubric (metric / artifact-state / threshold / §3-vs-YAML consistency)? **All 10 candidates passed** per the falsification-designer audit (0 rewrite-§3 verdicts).

3. **Practitioner-relevance axis.** Would a domain practitioner who builds software for a living agree that the lean-eval's verdict is worth listening to? Per the [domain-practitioner audit](audit-domain-practitioner.md): 3 candidates **accept-as-is** (GF-C, BF-S, BF-M) with high practical relevance; 7 candidates **accept-with-named-amendments**; 0 reject. **Load-bearing cross-cutting finding**: U-A / U-B / D7-U-1 are falsifier-mechanically-sound but **practitioner-thin** — their falsifiers measure substrate-emitted distributions/confidences/counts rather than software-quality outcomes. This axis is asymmetric: a candidate can pass the mechanical falsifier rubric (axis 2) while failing the practitioner-relevance axis (axis 3) — the downstream simulator-harness should track both.

4. **Cite-obligation-honoring axis.** Did the brief honor its Phase-7 cite obligations from the [auto-008 mapping table](../decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates)? **All 10 candidates passed** (verified verbatim by lead-agent at Wave 8.1 close). Cite-obligation distribution: GF-S/GF-C (0 cites); GF-M/U-B/U-C (1 cite each: Compound-Engineering 4-step loop); BF-L (1 cite: 4-architecture taxonomy); BF-S/BF-M/D7-U-1 (2 cites each); U-A (3 cites — highest absorption surface).

5. **Scenario-set-source axis.** Does the candidate draw scenarios from corpus, candidate-derived primitives, or hybrid? Distribution across the 10 briefs:
   - **Corpus-primary**: GF-S, GF-C (F-mode pressure-tests dominate)
   - **Candidate-derived-primary**: GF-M (Regime-A cycle is the scenario-derivation primitive), U-A (Compound-Knowledge Atelier intervals), U-B (mandate-as-traversal-direction-parameter scenarios), U-C (anchor.kind dispatcher tests), D7-U-1 (FC ledger scenarios)
   - **Hybrid**: BF-S, BF-M, BF-L (corpus F-mode anchors + candidate-specific brownfield primitive engagement)

Scenario-set-source affects falsifier interpretability — corpus-primary scenarios are practitioner-readable; candidate-derived-primary scenarios may require methodology-specific judgment to interpret a "pass" or "fail". The downstream simulator-harness should weight evaluators with corpus-familiarity for corpus-primary scenarios and methodology-familiarity for candidate-derived-primary scenarios.

## §2 DEC-1.a falsifying result pattern (verbatim from hypothesis-falsifier audit)

This is the load-bearing pattern named BEFORE downstream simulator-harness execution per [`auto-008 §Falsifier discipline`](../decisions/auto-008-phase-8-dispatch-shape.md#falsifier-discipline-load-bearing). Wave 8.2 quotes it verbatim from [`audit-hypothesis-falsifier.md`](audit-hypothesis-falsifier.md):

> **DEC-1.a falsifying result pattern.** DEC-1.a ("no methodology serves both mandates") is falsified iff, when the 10 lean-evals execute, **≥1 unified-attempt candidate** (U-A / U-B / U-C / D7-U-1) **passes cleanly** under the canonical R2 #3 + R6 #2 partitioned "pass cleanly" definition for unified-attempts — i.e., ALL of: (a′) ≥80% of that candidate's `greenfield-mandate-scenarios` (§1 partition) pass the brief's §2 success criteria AND ≥80% of that candidate's `brownfield-mandate-scenarios` (§1 partition) pass the brief's §2 success criteria; (b) the candidate's brief §3 `falsifying-outcome` is NOT triggered on any scenario in either bloc — AND the lean-eval result for that candidate **invokes none of the 3 canonical escape-hatches** (R2 #2: out-of-mandate scope claim; scenario-skip mid-run; criterion-substitution) NOR the R6 #5 structural rider (a unified-attempt with <3 scenarios scored in either mandate-bloc fails by construction). One such witness suffices; the hypothesis is universal-negation. If 0 of 4 unified-attempts meet this conjunction, DEC-1.a is NOT falsified by Phase-8 evidence. Mandate-aligned candidates (GF-S/GF-M/GF-C/BF-S/BF-M/BF-L) are NOT admissible witnesses — they serve only one mandate by design and cannot falsify the hypothesis whatever their lean-eval result.

**K=1.** The hypothesis-falsifier audit explicitly named K=1 as the universal-negation-falsifier threshold — one passing witness suffices to falsify the universal "no methodology serves both mandates" claim. The K=1 threshold is the strongest/weakest-sufficient falsifier of a universal negation and cannot be tuned to match the corpus.

**Honest framing (per R2 #4).** The pattern was named AFTER reading the 10 finalized briefs (not in absolute advance). The hypothesis-falsifier audit guarded against fitting the observed pattern via the **canonical-primitive constraint**: the falsifier is composed only from terms committed in [auto-008](../decisions/auto-008-phase-8-dispatch-shape.md) BEFORE per-candidate brief authoring. Pattern skeleton was drafted from hypothesis text + canonical terms before reading the 10 briefs; reading the briefs only fixed K=1, which is dictated by the universal-negation logical form, not by the brief corpus.

## §3 U-B honest-degradation reconciliation

The hypothesis-falsifier audit flagged one concern: **U-B's §2 honest-degradation-to-greenfield clause could be misread as R2 #2 hatch 1 (out-of-mandate scope claim) at result-time.** Wave 8.2 reconciliation:

- **Legitimate (NOT an escape-hatch):** U-B's lean-eval brief §2 names the honest-degradation clause **in advance** (in the brief itself, before evaluation runs). If U-B's evaluator declares "X_UNM_B inference confidence too low → degrading to greenfield-only" during execution, AND this degradation behavior was committed verbatim in U-B's §2 BEFORE the evaluator ran, the degradation is **NOT** an escape-hatch — it is a pre-committed scope clause that the lean-eval result correctly reports.
- **Escape-hatch (out-of-mandate scope claim per R2 #2):** If U-B's lean-eval result claims "this brownfield scenario is out-of-mandate" without a corresponding pre-committed clause in §2, OR if the degradation behavior was added to §2 mid-run, this IS an escape-hatch and triggers the falsifier.

**Downstream simulator-harness operational guidance:** the harness MUST compare the U-B brief's §2 text at lean-eval-start-time (frozen at the YAML `based-on-spec-commit` SHA) against any honest-degradation invocation at result-time. Any expansion of §2's degradation clause between start and result is an escape-hatch by construction.

This reconciliation also applies to any other candidate (especially unified-attempts) that uses honest-carve-out language in its brief §2. The general rule: **pre-committed scope clauses = legitimate; mid-run scope claims = escape-hatch.**

## §4 Practitioner-relevance weighting (per domain-practitioner audit)

The domain-practitioner audit named a load-bearing cross-cutting finding: U-A / U-B / D7-U-1 falsifiers pass the mechanical 4-item rubric (axis 2) but are **practitioner-thin** (axis 3). This is the asymmetry the downstream simulator-harness MUST track.

**Operational guidance for the harness:**

- **Weight practitioner-felt scenarios more heavily** when computing the cross-candidate verdict. A unified-attempt that passes the falsification-designer rubric but produces a substrate-emitted-evidence-only verdict is a **partial witness** — it satisfies the mechanical criterion for DEC-1.a falsification but doesn't deliver the practitioner-readable "this methodology actually serves both mandates" claim.
- **Two-tier "pass cleanly" report.** For each unified-attempt:
  - **Mechanical pass cleanly:** per R2 #3 + R6 #2 (≥80% per-bloc + falsifying-outcome NOT triggered + no escape-hatches).
  - **Practitioner pass cleanly:** AND the falsifier was practitioner-relevant (per the domain-practitioner audit's per-candidate scoring).
  - A unified-attempt that achieves only mechanical-pass-cleanly is a partial DEC-1.a-falsification witness; one that achieves both is a strong witness.
- **DEC-1.a falsification strength gradient.**
  - **Strong falsification:** ≥1 unified-attempt achieves practitioner-pass-cleanly (mechanical + practitioner).
  - **Mechanical falsification only:** ≥1 unified-attempt achieves mechanical-pass-cleanly but no unified-attempt achieves practitioner-pass-cleanly. Reported as "DEC-1.a is mechanically falsified but practitioner-readable evidence is missing; further pressure-testing recommended before claiming a unified methodology has been found."
  - **No falsification:** 0 unified-attempts achieve mechanical-pass-cleanly.

The practitioner-relevance weighting does NOT change the K=1 threshold for mechanical falsification (per the hypothesis-falsifier audit's universal-negation logic). It adds a strength gradient on top.

## §5 Per-candidate engagement with the falsifying pattern

For each of the 4 unified-attempts, names whether the lean-eval surfaces the DEC-1.a falsifying pattern if it occurs.

### U-A (Compound-Knowledge Atelier)

- **Mandate-partition**: 3 GF + 3 BF ✓
- **Falsifier**: Compound-Knowledge Atelier promotes zero `methodology-delta` intervals on EITHER greenfield OR brownfield bloc → mandate-asymmetric promotion failure.
- **DEC-1.a falsification surface**: If U-A passes ≥80% per-bloc + no falsifying-outcome triggered + no escape-hatch invoked, U-A is a witness for DEC-1.a falsification.
- **Practitioner-thin (per domain-practitioner)**: Falsifier measures substrate-emitted promotion counts (`docs/solutions/` directory state) rather than methodology-quality outcomes. A passing U-A is a **mechanical witness** for DEC-1.a falsification but a thin practitioner witness.

### U-B (mandate-as-traversal-direction)

- **Mandate-partition**: 3 GF + 3 BF ✓
- **Falsifier**: `LayerInferenceConfidence <0.7` on ≥2 of 3 brownfield scenarios AND fails to degrade to greenfield-only → unified-attempt claim collapses on both legs.
- **DEC-1.a falsification surface**: Subtle — U-B's honest-degradation clause means the candidate can "honestly carve out" brownfield work and remain a greenfield candidate. Per §3 above, pre-committed degradation is legitimate; mid-run degradation is an escape-hatch.
- **Practitioner-thin (per domain-practitioner)**: Falsifier measures `LayerInferenceConfidence` distributions and degradation-event counts — substrate-emitted evidence rather than practitioner-felt outcomes.

### U-C (mandate-as-parameter)

- **Mandate-partition**: 3 GF + 3 BF ✓
- **Falsifier**: Dispatcher regime-distribution divergence >40 pp between mandate-blocs OR brownfield <80% / greenfield ≥80%.
- **DEC-1.a falsification surface**: U-C's dispatcher IS the mandate-handler; if regime distributions are mandate-symmetric AND ≥80% per-bloc, U-C is a strong DEC-1.a falsification witness.
- **Practitioner-relevance**: Higher than U-A/U-B/D7-U-1 per the domain-practitioner audit's accept-with-named-amendments verdict — U-C's dispatcher scenarios engage anchor.kind enum + Brier pace-layer subsumption, which are practitioner-readable.

### D7-U-1 (Tournament-primary)

- **Mandate-partition**: 3 GF + 3 BF ✓
- **Falsifier**: Cross-mandate opposing-side `kind` distribution KL >1.0 between blocs OR ≥80% brownfield deterministic-checker + ≥80% greenfield operator-as-opposing-side.
- **DEC-1.a falsification surface**: D7-U-1's opposing-side kind distribution IS the mandate-symmetry test — if the distribution is genuinely mandate-symmetric, D7-U-1 is a DEC-1.a falsification witness.
- **Practitioner-thin (per domain-practitioner)**: Falsifier measures KL divergences on substrate-emitted distributions — mechanical-rigorous but practitioner-thin.

### Mandate-aligned candidates (NOT admissible DEC-1.a falsification witnesses)

Per the hypothesis-falsifier audit: GF-S / GF-M / GF-C / BF-S / BF-M / BF-L cannot falsify DEC-1.a because they serve only one mandate by design. Their lean-eval results are graded against their own candidate-specific falsifiers (per [audit-falsification-designer.md](audit-falsification-designer.md)), not against the cross-mandate DEC-1.a pattern.

## §6 H-1 stable-ID lettering convention reconciliation

[`auto-008`](../decisions/auto-008-phase-8-dispatch-shape.md#historian-load-bearing-design-inputs-5-gaps--n-candidates) said "recommend ONE candidate (U-C or D7-U-1) adopts" — but **BOTH** U-C and D7-U-1 volunteered. Their adoption mechanisms differ:

- **U-C** maps the H-1 lettering (R/A/F/AE/U/S/K) onto `anchor.kind` enum (per [ADR 0059 P-28 anchor envelope](../../docs/adr/0059-p-28-anchor-envelope.md) content-hash preimage discipline).
- **D7-U-1** maps the H-1 lettering onto FC envelope IDs (`F-<scenario-id>-<seq>` per the FC ledger).

**Lead-agent verdict.** Both adoptions are valid and complementary — they apply the convention at different layers (anchor envelope vs FC ledger). H-1 is now **more widely adopted than the historian's "ONE candidate" suggestion**; this is not a defect. The downstream simulator-harness can use either lettering convention or a unified mapping. Wave 8.2 names this as a non-blocking carry-forward to the Phase-8-close handoff for the post-v3 substrate-harness work.

## §7 Downstream simulator-harness handoff posture

Phase 8's deliverable is the **design** of 10 per-candidate lean-evals + this cross-candidate evaluator-brief. **Execution** is post-v3 simulator-harness work (out-of-scope for this run).

When the simulator-harness picks up this work, its tasks:

1. **Read all 10 lean-eval briefs** at [`lean-evals/<id>.md`](.) — each carries the candidate's YAML `falsifying-outcome:` + `phase-7-cite-obligations:` + `mandate-scenario-split:`.
2. **Read this cross-candidate brief** — for the comparison axes (§1), the DEC-1.a falsifying result pattern (§2 verbatim), the U-B honest-degradation reconciliation (§3), and the practitioner-relevance weighting (§4).
3. **Read the falsification-designer audit** — for the per-candidate verdict-tokens (all 10 PASS at Wave-8.1.b time).
4. **Read the hypothesis-falsifier audit** — for the canonical falsifying pattern + R2 #4 guard account.
5. **Read the domain-practitioner audit** — for the per-candidate practitioner-relevance verdicts.
6. **Execute each lean-eval per its §5 protocol** (~1 day per candidate, per the v1.2 plan). Record per-scenario pass/fail, falsifying-outcome trigger, and escape-hatch invocation.
7. **Compute the cross-candidate DEC-1.a verdict** using the pattern in §2 + the strength gradient in §4. Report:
   - DEC-1.a falsification verdict (strong / mechanical-only / not-falsified)
   - Per-candidate falsifying-outcome trigger count
   - Per-candidate escape-hatch invocation count
   - Per-candidate practitioner-relevance score
8. **Surface any unanticipated escape-hatches** (R2 #2 enumeration is canonical but not exhaustive in practice) for review against the discipline.

The simulator-harness MAY execute lean-evals in any order; the cross-candidate verdict is order-independent. Parallel execution is feasible (each lean-eval is ~1-day evaluator-time; harness budget permitting).

## §8 References

**Phase-8 dispatch and rubric:**

- [`auto-008` dispatch shape brief](../decisions/auto-008-phase-8-dispatch-shape.md) — Phase-8 wave shape + falsifier discipline + Phase-7 cite-obligation propagation + tier-table.
- [Phase-8 scope envelope](../scope-envelope-2026-05-28-phase-8.md) — run contract.

**Wave 8.1 per-candidate briefs:**

- [`lean-evals/gf-s.md`](gf-s.md), [`lean-evals/gf-m.md`](gf-m.md), [`lean-evals/gf-c.md`](gf-c.md), [`lean-evals/bf-s.md`](bf-s.md), [`lean-evals/bf-m.md`](bf-m.md), [`lean-evals/bf-l.md`](bf-l.md), [`lean-evals/u-a.md`](u-a.md), [`lean-evals/u-b.md`](u-b.md), [`lean-evals/u-c.md`](u-c.md), [`lean-evals/d7-u-1.md`](d7-u-1.md).

**Wave 8.1.b bias-guard audits:**

- [`audit-domain-practitioner.md`](audit-domain-practitioner.md) — practitioner-relevance verdicts; load-bearing finding on U-A/U-B/D7-U-1 practitioner-thin falsifiers.
- [`audit-falsification-designer.md`](audit-falsification-designer.md) — 10/10 PASS on 4-item rubric; verdict-token format.
- [`audit-hypothesis-falsifier.md`](audit-hypothesis-falsifier.md) — DEC-1.a falsifying result pattern (quoted verbatim above); canonical-primitive guard account.
- [`cross-check-falsifier.md`](cross-check-falsifier.md) — lead-agent cross-check artifact (R5 #1); 0 rewrite-§3 verdicts; Phase-8-followup deferral NOT FIRED.

**Cross-cutting v3 docs:**

- [DEC-1.a working hypothesis](../decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8) — the hypothesis Phase-8 is the falsification surface for.
- [Phase-7 §6.4 NEUTRAL observation](../backfill-notes.md#64-dec-1-a-working-hypothesis-observation-neutral-pre-phase-8) — pre-Phase-8 stance.
- [Candidate registry](../candidate-registry.md) — 10-candidate enumeration with mandate scoping.
- [v1.2 plan § Phase 8](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-8--lean-eval-design-one-brief-per-candidate-first-pressure-test-surface-revised-in-v12) — phase scope + ~1-day evaluator-time bound.
