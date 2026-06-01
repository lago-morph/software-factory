# Session handoff — 2026-05-28 (Phase 8 closed; v3 synthesis pipeline complete)

This is the pickup brief for the next agent. **Phase 8 is fully closed** as of the 2026-05-28 autonomous run. All 10 per-candidate lean-eval briefs are landed (1 exemplar lead-agent-authored + 9 sibling subagent-authored); all 3 cross-candidate bias-guard audits are complete (domain-practitioner + falsification-designer + hypothesis-falsifier); the lead-agent falsifier cross-check artifact is committed (R5 #1 mandatory); the cross-candidate evaluator-brief is authored with the DEC-1.a falsifying result pattern named verbatim before downstream simulator-harness execution.

**The v3 synthesis pipeline is now complete.** Downstream work (simulator-harness execution of the lean-evals; cross-candidate verdict computation; final architecture selection) is post-v3 scope.

Supersedes the [Phase-7-close handoff](SESSION-HANDOFF-2026-05-27-phase-7-close.md). The Phase-7-close handoff carried the binding gate "Phase 8 lean-eval design UNBLOCKED"; that gate is consumed by this handoff.

## Where we are

| Concern | State | Detail |
|---|---|---|
| Phase 8 dispatch shape | **Closed** | [`auto-008`](decisions/auto-008-phase-8-dispatch-shape.md) (Round 1 + Round 2 + post-Round-2 reviewer amendments closed; 6 adversarial reviewers across 2 rounds) |
| Phase 8 exemplar | **Closed** | [`lean-evals/gf-m.md`](lean-evals/gf-m.md) (lead-agent-authored; self-check gate PASS on load-bearing item d) |
| Phase 8 Wave 8.1 (per-candidate fanout) | **Closed** | 9 sibling lean-eval briefs at [`lean-evals/`](lean-evals/) (gf-s, gf-c, bf-s, bf-m, bf-l, u-a, u-b, u-c, d7-u-1) |
| Phase 8 Wave 8.1.b (cross-candidate bias-guards) | **Closed** | [`audit-domain-practitioner.md`](lean-evals/audit-domain-practitioner.md) + [`audit-falsification-designer.md`](lean-evals/audit-falsification-designer.md) + [`audit-hypothesis-falsifier.md`](lean-evals/audit-hypothesis-falsifier.md) (3 cross-candidate auditors A.2′ shape per auto-008) |
| Lead-agent falsifier cross-check (R5 #1 mandatory) | **Closed** | [`cross-check-falsifier.md`](lean-evals/cross-check-falsifier.md) — 0 rewrite-§3 verdicts; Phase-8-followup deferral NOT FIRED |
| Phase 8 Wave 8.2 (cross-candidate evaluator-brief) | **Closed** | [`lean-evals/00-cross-candidate.md`](lean-evals/00-cross-candidate.md) (lead-agent-authored; subagent-fallback NOT TRIGGERED) |
| DEC-1.a falsifying result pattern | **Named verbatim, pre-execution** | Per [`audit-hypothesis-falsifier.md`](lean-evals/audit-hypothesis-falsifier.md) + [`00-cross-candidate.md §2`](lean-evals/00-cross-candidate.md) — K=1 universal-negation falsifier; canonical-primitive guard used |
| Phase-8-followup deferral | **NOT FIRED** | 0 unified-attempt rewrite-§3 verdicts; threshold (≥1 unified-attempt) not breached |
| v3 synthesis pipeline | **COMPLETE** | Downstream simulator-harness execution is post-v3 scope (no v3 phase remains) |

## Phase 8 deliverables (all in this commit's tree)

### Per-candidate lean-eval briefs (10 files; 1 lead-agent exemplar + 9 subagent-authored)

| Candidate | Mandate | Tier | Brief file | Words | Falsifier (one-line) |
|---|---|---|---|---|---|
| GF-M (exemplar) | greenfield | Light | [`lean-evals/gf-m.md`](lean-evals/gf-m.md) | 4434 | Paraphrase-divergence MCC ≤0.55 (P-21 F37 defense) |
| GF-S | greenfield | Light | [`lean-evals/gf-s.md`](lean-evals/gf-s.md) | 5111 | P-15 four-guard ensemble MCC ≤0.55 |
| GF-C | greenfield | Light | [`lean-evals/gf-c.md`](lean-evals/gf-c.md) | 5986 | P-17 substance-check ensemble MCC ≤0.55 |
| BF-S | brownfield | Light | [`lean-evals/bf-s.md`](lean-evals/bf-s.md) | 5188 | P-25 perimeter bypass-rate ≥80% OR trifecta cascade |
| BF-M | brownfield | Heavy | [`lean-evals/bf-m.md`](lean-evals/bf-m.md) | 5604 | P-27 archaeological brief recall MCC ≤0.55 |
| BF-L | brownfield | Heavy | [`lean-evals/bf-l.md`](lean-evals/bf-l.md) | 5919 | P-13 drift-detection rate <80% (1M+LOC repo) |
| U-A | unified-attempt | Heavy | [`lean-evals/u-a.md`](lean-evals/u-a.md) | 6032 | Zero methodology-delta promotions per ≥3 cycles on either bloc |
| U-B | unified-attempt | Heavy | [`lean-evals/u-b.md`](lean-evals/u-b.md) | 5589 | LayerInferenceConfidence <0.7 on ≥2 of 3 brownfield + degradation count 0 |
| U-C | unified-attempt | Heavy | [`lean-evals/u-c.md`](lean-evals/u-c.md) | 5570 | Dispatcher regime-distribution divergence >40 pp between blocs |
| D7-U-1 | unified-attempt | Heavy | [`lean-evals/d7-u-1.md`](lean-evals/d7-u-1.md) | 5714 | Opposing-side kind distribution KL >1.0 or mandate-asymmetric clustering |

All 10 briefs:
- Pass the falsification-designer 4-item rubric (per [`audit-falsification-designer.md`](lean-evals/audit-falsification-designer.md): 10/10 PASS, 0 rewrite-§3).
- Honor their Phase-7 cite obligations verbatim per the [auto-008 mapping table](decisions/auto-008-phase-8-dispatch-shape.md#high-confidence-mandatory-cite-obligations-3-cells--n-candidates).
- 4 unified-attempts carry `mandate-scenario-split: {greenfield: 3, brownfield: 3}` per R6 #1.
- All within their tier (median Light 5188; median Heavy 5714; GF-M exemplar 4434 acknowledged below tier-floor with rationale).

### Bias-guard audits (3 files)

- [`audit-domain-practitioner.md`](lean-evals/audit-domain-practitioner.md) — 2235w. Verdict tally: 3 accept-as-is (GF-C, BF-S, BF-M) + 7 accept-with-named-amendments + 0 reject. **Load-bearing cross-cutting finding**: U-A / U-B / D7-U-1 are falsifier-mechanically-sound but **practitioner-thin** (measure substrate-emitted distributions vs software-quality outcomes).
- [`audit-falsification-designer.md`](lean-evals/audit-falsification-designer.md) — 1122w. 10/10 PASS on 4-item rubric. R5 #3 verdict-token format applied (greppable by `grep -c "verdict: rewrite-§3"`).
- [`audit-hypothesis-falsifier.md`](lean-evals/audit-hypothesis-falsifier.md) — 1985w. DEC-1.a falsifying result pattern named verbatim with R2 #4 canonical-primitive guard account. K=1 universal-negation falsifier; mandate-aligned candidates NOT admissible witnesses.

### Lead-agent artifacts

- [`cross-check-falsifier.md`](lean-evals/cross-check-falsifier.md) — 0 rewrite-§3 verdicts; Phase-8-followup deferral NOT FIRED; lead-agent-authored Wave-8.2 path active.
- [`00-cross-candidate.md`](lean-evals/00-cross-candidate.md) — 2221w. Cross-candidate evaluator-brief with §1 5 axes + §2 DEC-1.a falsifying pattern verbatim + §3 U-B honest-degradation reconciliation + §4 practitioner-relevance weighting + §5 per-candidate engagement + §6 H-1 reconciliation + §7 downstream-simulator-harness handoff.

## DEC-1.a working hypothesis status (committed pre-execution; explicitly UN-decided)

The DEC-1.a falsifying result pattern is named verbatim in [`00-cross-candidate.md §2`](lean-evals/00-cross-candidate.md) BEFORE the simulator-harness executes the lean-evals:

> DEC-1.a ("no methodology serves both mandates") is falsified iff ≥1 unified-attempt candidate (U-A / U-B / U-C / D7-U-1) passes cleanly per the partitioned form (≥80% greenfield-bloc + ≥80% brownfield-bloc + falsifying-outcome NOT triggered + no escape-hatches + no R6 #5 structural-rider violation). K=1 universal-negation falsifier. Mandate-aligned candidates are NOT admissible witnesses.

**Lead agent does NOT pre-judge.** Per [auto-008 §Bias-direction discipline](decisions/auto-008-phase-8-dispatch-shape.md#bias-direction-discipline): Phase-8 has a SYMMETRIC bias direction (do-not-pre-judge). The downstream simulator-harness executes the 10 lean-evals + computes the cross-candidate verdict.

## H-1 stable-ID lettering convention (BOTH U-C and D7-U-1 adopted)

Per [`00-cross-candidate.md §6`](lean-evals/00-cross-candidate.md): the historian's recommendation was "ONE candidate adopts" but **BOTH U-C and D7-U-1 volunteered with complementary mechanisms**:

- **U-C** maps H-1 lettering (R/A/F/AE/U/S/K) onto `anchor.kind` enum per [ADR 0059](../docs/adr/0059-p-28-anchor-envelope.md).
- **D7-U-1** maps H-1 lettering onto FC envelope IDs (`F-<scenario-id>-<seq>`).

Lead-agent verdict: both adoptions are valid and complementary; not a defect. **Downstream-simulator-harness carry**: choose either lettering convention or a unified mapping.

## Phase-8-followup carry-forward (deferrals — none load-bearing)

Per [`cross-check-falsifier.md`](lean-evals/cross-check-falsifier.md): no Phase-8-followup deferral fired (0 unified-attempt rewrite-§3 verdicts; threshold not breached). Per [`AGENTS-MD-2adf78e54a`](../AGENTS.md#deferred-work-binding-artifact-triple): binding-artifact triple NOT instantiated.

**Advisory carry-forwards from this run (NOT downstream blockers):**

1. **U-A / U-B / D7-U-1 practitioner-thin falsifiers** (per domain-practitioner audit). The downstream simulator-harness should track both **mechanical pass cleanly** and **practitioner pass cleanly** per [`00-cross-candidate.md §4`](lean-evals/00-cross-candidate.md) — a unified-attempt that achieves only mechanical-pass-cleanly is a **partial DEC-1.a falsification witness**, reported as "DEC-1.a mechanically falsified but practitioner-readable evidence is missing; further pressure-testing recommended".

2. **U-B honest-degradation reconciliation** (per [`00-cross-candidate.md §3`](lean-evals/00-cross-candidate.md)). The downstream simulator-harness MUST compare U-B's brief §2 text at lean-eval-start-time (frozen at `based-on-spec-commit` SHA) against any honest-degradation invocation at result-time. Mid-run scope claims = escape-hatch; pre-committed = legitimate.

3. **GF-M exemplar word-count under Light tier floor** (4434 vs 5000-6500). Exemplar prioritized structural clarity over tier-floor compliance per its self-check note. Wave 8.1 subagents targeted their own tier, NOT the exemplar's length (all 9 within tier). Non-recurring concern.

4. **Multiple in-flight checkpoint commits on Wave 8.1 fanout omnibus** — 4 commits on the fanout branch due to stop-hook async coordination with subagent file landings. Final state at PR-open time is the canonical Wave 8.1 close state. Non-recurring concern.

5. **H-5 scaffold/harness C11 vocabulary** (per [Phase-7 historian H-5 gap](backfill-notes.md#41-load-bearing-gaps-5--phase-8-lean-eval-inputs)) — glossary addition opportunity for [`decisions-captured.md`](decisions-captured.md) or future glossary; non-blocking; deferred from Phase 7.

None of these block downstream work.

## The next work — downstream simulator-harness execution (post-v3 scope)

Per [`00-cross-candidate.md §7`](lean-evals/00-cross-candidate.md): the simulator-harness picks up this work and:

1. Reads all 10 per-candidate lean-eval briefs.
2. Reads the cross-candidate evaluator-brief (`00-cross-candidate.md`) for axes + DEC-1.a pattern + U-B reconciliation + practitioner-relevance weighting.
3. Reads the 3 bias-guard audits for verdict-tokens + practitioner-relevance + canonical falsifying pattern.
4. Executes each lean-eval per its §5 protocol (~1 day per candidate per v1.2 plan).
5. Computes the cross-candidate DEC-1.a verdict using §2 pattern + §4 strength gradient.
6. Reports: DEC-1.a verdict (strong / mechanical-only / not-falsified); per-candidate falsifying-outcome trigger count; per-candidate escape-hatch invocation count; per-candidate practitioner-relevance score.

The simulator-harness MAY execute lean-evals in any order; cross-candidate verdict is order-independent.

### Entry blockers (user-input territory)

None known at Phase-8 close. The downstream simulator-harness shape is post-v3 scope; v3 synthesis pipeline is complete.

### Work that doesn't need user input

None. v3 synthesis pipeline is complete. Downstream simulator-harness execution is its own discrete work-unit (likely a separate engineering project).

## Task-aware reading lists

### Downstream simulator-harness picker (post-v3 entry point)

- Read: [`AGENTS.md`](../AGENTS.md), [`AGENT-ENTRY.md`](../AGENT-ENTRY.md), this handoff, [`lean-evals/00-cross-candidate.md`](lean-evals/00-cross-candidate.md), all 10 `lean-evals/<id>.md` briefs (in any order), 3 bias-guard audits at `lean-evals/audit-*.md`, [`cross-check-falsifier.md`](lean-evals/cross-check-falsifier.md), [DEC-1.a working hypothesis](decisions-captured.md#d1--unification-verdict-no-methodology-serves-both-mandates-working-hypothesis-falsifiable-by-phase-8).
- Skip: per-candidate `specs/` (referenced from lean-eval briefs; drill on demand); Phase-7 backfill notes (referenced from lean-eval briefs); ADRs (referenced from per-candidate briefs; drill on demand).

### Retrospective reviewer (this run's morning review)

- Read: [`AGENTS.md`](../AGENTS.md), [`run-summary-2026-05-28-phase-8.md`](../../archive/PR-201-run-summary-2026-05-28-phase-8.md) (when authored at PR 8), [`retrospective/2026-05-28-NNN.md`](../retrospective/) (when authored at PR 8), this handoff. The morning summary's "suggested merge order" + "morning-review items" are the primary review surface.
- Skip: per-candidate briefs (review by sampling 1-2 candidates against the cross-candidate brief; full per-candidate review is downstream-simulator-harness territory, not morning review).

### Future phase planning (if Phase-9 emerges)

No v3 phase remains. If a future synthesis emerges (e.g., simulator-harness execution surfaces a primitive gap that requires v3-rewrite), it would be a NEW synthesis project per the archive-and-rebuild discipline, not Phase 9.

## What carried forward (load-bearing material)

### This run's outputs

- **PR #194 (scope envelope).** Phase-8 run contract.
- **PR #195 (auto-008 dispatch brief).** Phase-8 wave shape + rubric + Phase-7 cite-obligation propagation + falsifier discipline; 6 adversarial reviewers across 2 rounds.
- **PR #196 (GF-M exemplar).** Lead-agent-authored exemplar; pre-fanout self-check PASS on load-bearing item.
- **PR #197 (Wave 8.1 fanout omnibus).** 9 sibling per-candidate lean-eval briefs. All within tier; all PASS falsification-designer rubric; all honor Phase-7 cite obligations.
- **PR #198 (Wave 8.1.b bias-guards omnibus + cross-check).** 3 cross-candidate audits + R5 #1 mandatory cross-check artifact.
- **PR #199 (Wave 8.2 cross-candidate evaluator-brief).** Lead-agent-authored DEC-1.a falsifying pattern verbatim + 5 comparison axes + practitioner-relevance weighting + downstream-simulator-harness handoff.
- **This handoff PR.** Phase-8-close handoff + AGENT-ENTRY.md Section-2 update.
- **Morning summary + retrospective PR (to follow).** PR 8.

### Inherited binding material (unchanged from Phase 7)

- [`AGENTS.md`](../AGENTS.md) — project conventions; 17 active rules (5 Phase-7 retro AGENTS-MD-* rules NOT adopted per user election; applied informally in auto-008 with citation pattern through retrospective directory).
- [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) — v1.2 plan (Phase 8 is the last v3 phase; pipeline complete after this run).
- [`AGENT-ENTRY.md`](../AGENT-ENTRY.md) — root navigation; Section 2 updated by this handoff PR to point here.
- [`phase-3.4-decisions-resolved.md`](phase-3.4-decisions-resolved.md) — Tier-1 binding decisions.
- [`candidate-registry.md`](candidate-registry.md) — 10-candidate registry.
- All 55 Phase-5 ADRs at [`docs/adr/`](../docs/adr/).
- 10 Phase-6 architecture specs at [`specs/`](specs/) — NOT patched in Phase 7 OR Phase 8.
- [`mandate-fit-matrix.md`](mandate-fit-matrix.md) — Phase-6 mandate-fit matrix.
- 10 Phase-7 per-candidate back-fill notes + 2 Phase-7 bias-guard audits + Phase-7 aggregation matrix at [`backfill-notes.md`](backfill-notes.md).
- All Phase-8 deliverables above.
- Prior decision briefs: [auto-001 through auto-008](decisions/).

## Current git state — Phase-8 PR chain

PRs opened this run (in stack order, top to bottom):

- **This handoff PR (PR 7 in flight at handoff-write time)** — Phase-8-close handoff + AGENT-ENTRY.md Section-2 update.
- PR #199 (Wave 8.2 cross-candidate evaluator-brief).
- PR #198 (Wave 8.1.b bias-guards omnibus + cross-check artifact).
- PR #197 (Wave 8.1 fanout omnibus — 9 sibling per-candidate briefs).
- PR #196 (GF-M exemplar).
- PR #195 (auto-008 dispatch brief).
- PR #194 (scope envelope).

Subagents dispatched this run: **18 total** (6 adversarial reviewers on auto-008 R1+R2 + 9 Wave-8.1 per-candidate fanout + 3 Wave-8.1.b bias-guards). The auto-008 PR-cap math (8-9 PRs) is met at 8 PRs (this handoff is PR 7; morning summary + retro is PR 8).

## Honest acknowledgements

- **Phase-7 retro AGENTS-MD-* rules NOT adopted into canonical AGENTS.md** (user election at envelope-time). auto-008 applied the patterns informally with cite-by-retrospective-path; cannot ground reviews by stable AGENTS-MD-<hash> in canonical AGENTS.md. Non-blocking; flagged in auto-008 §Honest acknowledgements (Round 1).
- **GF-M exemplar under Light tier floor** (4434 vs 5000-6500). Exemplar prioritized structural clarity; Wave 8.1 subagents targeted their own tier (all 9 within tier). Acknowledged in exemplar's self-check section.
- **Multiple in-flight checkpoint commits on Wave 8.1 fanout omnibus** (4 commits). Stop-hook async coordination with subagent file landings produced multiple checkpoints rather than one omnibus commit. Final state is correct; checkpoint count is a process artifact of unattended-run + async-subagent + git-hook interaction.
- **No `reject-with-counter-proposal` from any of the 18 subagents.** Both rounds of adversarial review on auto-008 + all 9 fanout subagents + all 3 bias-guard subagents returned `accept-as-is` or `accept-with-named-amendments`. The brief + dispatch shape pattern (per-candidate parallel fanout + A.2′ cross-candidate bias-guards + lead-agent cross-check + lead-agent cross-candidate evaluator-brief) appears robust under per-candidate execution AND cross-candidate aggregation.
- **DEC-1.a working hypothesis is explicitly UN-decided.** Phase-8 produces design artifacts only; the falsifying-result-pattern is named pre-execution; the simulator-harness will compute the verdict. Lead agent honored the symmetric bias-direction discipline throughout.
- **R6 #1 + R6 #2 + R6 #5 partitioned-mandate amendments are load-bearing for DEC-1.a falsification.** The cross-mandate attacker (R6) reviewer in auto-008 Round 2 surfaced the structural defect where the DEC-1.a falsifying pattern presupposed two lean-eval files per unified-attempt while the file model has one. The Round-2 amendments fixed this by partitioning the §1 scenario set into mandate-blocs within a single brief + redefining "pass cleanly" per-bloc for unified-attempts + adding the R6 #5 structural rider preventing scope-claim escape-hatches. All 4 unified-attempts honor this discipline (3 GF + 3 BF each).
