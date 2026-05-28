# Falsification-designer audit — Phase 8 Wave 8.1 cross-candidate roll-up

**Auditor.** Phase-8 Wave-8.1.b falsification-designer subagent (cross-candidate roll-up per auto-008 §Decision Round 2 A.2′).
**Inputs.** 10 finalized lean-eval briefs at [`architectures/v3/lean-evals/<id>.md`](.) (gf-s, gf-m, gf-c, bf-s, bf-m, bf-l, u-a, u-b, u-c, d7-u-1).
**Method.** Each brief evaluated against the 4-item rubric per [`auto-008 §Falsifier discipline R2 #1`](../decisions/auto-008-phase-8-dispatch-shape.md#r2-1-falsification-designer-concreteness-rubric-3-item-mechanical): (i) names a metric; (ii) names a directory/artifact-state/trajectory class; (iii) names a threshold; (iv) §3-vs-YAML consistency MANDATORY. Pass = ≥2 of (i)-(iii) AND mandatory pass on (iv). Unified-attempts additionally evaluated for `mandate-scenario-split-verified` per R6 #1 (`mandate-scenario-split` YAML field with N≥3 AND M≥3; `### Greenfield-mandate scenarios` + `### Brownfield-mandate scenarios` subsections in §1; partitioned "pass cleanly" form applied).

## Cross-candidate summary

**Headline finding: 10 of 10 briefs PASS the 4-item rubric. 0 trigger rewrite-§3.** Every brief carries a populated `falsifying-outcome:` YAML field with concrete metric + artifact-path + numeric threshold, and every §3 statement is verbatim consistent with its YAML field (item (iv) passes mandatorily across all 10). All 4 unified-attempts (U-A / U-B / U-C / D7-U-1) honor the R6 #1 mandate-partition requirement: `mandate-scenario-split: {greenfield: 3, brownfield: 3}` populated; §1 partitioned into the two named subsections; §3 falsifiers framed in unified-attempt-distinctive form (mandate-asymmetric collapse pattern, not implementation noise).

**Cross-candidate patterns:**

1. **MCC ≤0.55 / detection-rate <80% is the dominant falsifier form** (gf-s, gf-m, gf-c, bf-m, bf-l) — five briefs use the Larbi single-judge MCC ≤0.55 ceiling as the comparison floor for their distinctive load-bearing wager. This is mechanically auditable: a single metric + threshold pair, identical across briefs.
2. **Unified-attempts use mandate-asymmetric collapse falsifiers** (u-a, u-b, u-c, d7-u-1) — all 4 unified-attempt §3 statements frame "the unified claim collapses if one mandate-bloc fails while the other succeeds" rather than mandate-blind aggregate failure. This is exactly the form auto-008 R2 #3 + R6 #2 partitioned "pass cleanly" definition calls for; the DEC-1.a falsification surface is well-formed.
3. **BF-S uses a per-cycle bypass-rate + cascade-count two-disjunction falsifier** — slightly different shape (perimeter-bypass + trifecta-cascade) but mechanically equivalent (two single-direction comparisons OR'd together).
4. **Artifact-state paths are consistent in shape** — all 10 use `solutions/audit/<primitive-id>/<scenario-id>.json` (or `.jsonl` in d7-u-1's case). Lead-agent cross-check via `grep -h "^  measured" <briefs>` will return uniformly shaped lines.

**No rewrite-§3 verdicts. No unified-attempt failure → Phase-8-followup deferral threshold (≥1 unified-attempt rewrite) NOT triggered. No subagent-fallback condition (≥3 unified-attempt rewrites) triggered for Wave 8.2.**

## Per-candidate verdicts

## gf-s

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: Ensemble MCC ≤0.55 OR detection rate <80% on F37/F27/F48 prompt pairs; artifact `solutions/audit/p-15-runs/`; YAML 62 words; §3 verbatim quotes YAML and names identical metric+threshold+location.

## gf-m

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: Paraphrase-divergence detection rate <80% OR MCC ≤0.55 on F37 corpus; artifact `solutions/audit/p-21-runs/`; YAML 46 words; §3-vs-YAML identical metric/path/threshold.

## gf-c

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: P-17 substance-check MCC ≤0.55 OR vacuous-flag detection <80% on thin/rich blind set; artifact `solutions/audit/p-17-substance-check/`; §3 verbatim repeats YAML; consistent.

## bf-s

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: P-25 bypass-event rate ≥80% per cycle OR trifecta-cascade ≥1 with perimeter on; artifacts `solutions/audit/p-25-bypass/` + `solutions/audit/p-24/`; two-disjunction form; YAML/§3 identical.

## bf-m

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: P-27 archaeological brief misses ≥1 load-bearing invariant on ≥4 of 6 scenarios OR brief-recall MCC ≤0.55; artifact `solutions/audit/p-27-briefs/`; consistent.

## bf-l

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: n/a (non-unified-attempt)
notes: P-13 maintenance-loop drift-detection rate <80% within one reconciliation cycle OR MCC ≤0.55 on seeded-drift set; artifact `solutions/audit/p-13-runs/`; §3 explicitly repeats YAML with parameter-set match.

## u-a

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: pass
notes: Mandate-asymmetric promotion failure: ≤0 `kind: methodology-delta` entries per ≥3 cycles on EITHER greenfield OR brownfield bloc; artifact `docs/solutions/` + ADR-0051 envelope; mandate-split 3/3 honored; §1 partitioned subsections present.

## u-b

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: pass
notes: `LayerInferenceConfidence <0.7` on L0/L1 on ≥2 of 3 brownfield scenarios AND `degradation-event-count == 0`; artifact `solutions/audit/x-unm-b-runs/`; mandate-split 3/3; partitioned §1; honest-degradation-theatre form.

## u-c

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: pass
notes: Dispatcher-regime-distribution divergence >40 percentage-points between mandate-blocs OR brownfield <80% while greenfield ≥80%; artifact `solutions/audit/p-19-dispatch/`; mandate-split 3/3; partitioned subsections; structural-rider clause honored.

## d7-u-1

verdict: pass
rubric-items:
  (i)-metric: pass
  (ii)-artifact-state: pass
  (iii)-threshold: pass
  (iv)-§3-yaml-consistency: pass
mandate-scenario-split-verified: pass
notes: Opposing-side `kind` distribution KL >1.0 between greenfield-bloc and brownfield-bloc OR ≥80%/≥80% mandate-asymmetric clustering; artifact `solutions/audit/fc-ledger/<scenario-id>.jsonl`; mandate-split 3/3; partitioned §1; mandate-symmetric-substrate claim targeted.

## Lead-agent cross-check guidance

**Counting rewrite verdicts.** Run the equivalent of `grep -c <REWRITE_VERDICT_TOKEN> audit-falsification-designer.md` against the Per-candidate verdicts section, where `<REWRITE_VERDICT_TOKEN>` is the literal `verdict` + colon + space + `rewrite` + the section-mark dash + `3` token specified in auto-008 R5 #3. The grep is best run with `--include="## *"` scoping or against just the "Per-candidate verdicts" block to avoid matching the literal token in this guidance prose. Expected count under the Per-candidate verdicts heading: **0**. If non-zero, the brief whose rewrite-verdict matches must be re-authored before Wave 8.2 dispatches.

**Identifying which candidates would need re-authoring (none in this run).** The equivalent `grep -B 2` against the same scoped region would surface the candidate-ID heading preceding the verdict line. Under the Per-candidate verdicts section, no such match exists in this audit, so no candidate triggers the lead-agent falsifier cross-check re-author step before Wave 8.2.

**Phase-8-followup deferral threshold check** (per auto-008 R1 #5): the threshold for Phase-8-followup deferral is **≥1 unified-attempt** rewrite verdict. With 0 unified-attempt rewrites (U-A / U-B / U-C / D7-U-1 all pass), the deferral does NOT fire; no `Phase-8-followup carry-forward` section is owed in the Phase-8-close handoff.

**Cross-candidate evaluator-brief subagent-fallback check** (per auto-008 §Honest acknowledgements (Round 2) item 4): the threshold for switching Wave 8.2 cross-candidate evaluator-brief from lead-agent-authored to subagent-dispatched is **≥3 unified-attempt** rewrite verdicts. With 0, the lead-agent-authored default holds.

**Caveats.**

1. This audit applies the 4-item rubric mechanically. It does not adjudicate whether each falsifier is the *most* distinctive load-bearing wager for its candidate — only whether it passes the concreteness gate. The hypothesis-falsifier (Wave 8.1.c, serial after this audit) and the cross-candidate evaluator-brief (Wave 8.2) are the venues for cross-candidate distinctiveness analysis.
2. Two briefs (gf-m and u-a) use slightly more elaborate consistency mechanisms (gf-m's `§3-vs-YAML consistency` self-attests via 4-of-4 enumeration; u-a's verbatim YAML quotation as the §3 opening). Both pass; flag is informational only.
3. The R6 #5 structural-rider clause (a unified-attempt with <3 scenarios scored in a mandate-bloc fails by construction) is preventively honored by all 4 unified-attempts via their mandate-scenario-split of 3/3 — no candidate is at risk of construction-failure on this clause.
