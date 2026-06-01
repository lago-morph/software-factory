# Run summary — Phase 8 (2026-05-28)

This is the morning user's primary review artifact. The PR descriptions in the stack are the secondary review surface (per [`autonomous-run` skill § PR description discipline](.claude/skills/autonomous-run/SKILL.md#pr-description-discipline)).

## TL;DR

- **Phase 8 closed.** v3 synthesis pipeline is COMPLETE. Downstream simulator-harness execution is post-v3 scope.
- **DEC-1.a falsifying result pattern named verbatim pre-execution** (K=1 universal-negation falsifier; canonical-primitive guard used).
- **All 10 per-candidate lean-eval briefs landed**, all within their tier, all pass falsification-designer 4-item rubric (0 rewrite-§3 verdicts).
- **3 bias-guard cross-candidate audits + lead-agent cross-check artifact** complete.
- **Cross-candidate evaluator-brief** quotes DEC-1.a pattern verbatim + names 5 comparison axes + practitioner-relevance weighting per domain-practitioner audit's load-bearing finding.
- **8 PRs total against 15-PR phase budget**; 18 subagents (6 adversarial + 9 fanout + 3 bias-guards); 0 reject-with-counter-proposal across all subagents.
- **1 morning-review item:** Phase-8-followup advisory carry-forwards (5 non-blocking items in handoff §"Phase-8-followup carry-forward").

## Suggested merge order

Merge in stack-bottom order to preserve rewind boundaries. **Merge PR #194 first; subsequent PRs auto-rebase as their parents merge.**

| Order | PR | Title | Base |
|---|---|---|---|
| 1 | [#194](https://github.com/lago-morph/software-factory/pull/194) | phase 8: scope envelope | `main` |
| 2 | [#195](https://github.com/lago-morph/software-factory/pull/195) | phase 8: auto-008 dispatch shape brief (Round 1+2 + reviewer amendments) | `claude/phase-8-envelope` → auto-rebase to `main` |
| 3 | [#196](https://github.com/lago-morph/software-factory/pull/196) | phase 8: exemplar lean-eval brief for GF-M | `claude/phase-8-auto-008-4CZoC` → auto-rebase |
| 4 | [#197](https://github.com/lago-morph/software-factory/pull/197) | phase 8: Wave 8.1 lean-eval fanout omnibus (9 per-candidate briefs) | `claude/phase-8-exemplar` → auto-rebase |
| 5 | [#198](https://github.com/lago-morph/software-factory/pull/198) | phase 8: Wave 8.1.b bias-guards omnibus + cross-check artifact | `claude/phase-8-fanout-omnibus` → auto-rebase |
| 6 | [#199](https://github.com/lago-morph/software-factory/pull/199) | phase 8: Wave 8.2 cross-candidate evaluator-brief | `claude/phase-8-bias-guards` → auto-rebase |
| 7 | [#200](https://github.com/lago-morph/software-factory/pull/200) | phase 8: close handoff + AGENT-ENTRY.md rotation | `claude/phase-8-cross-candidate` → auto-rebase |
| 8 | TBD | phase 8: run summary + retrospective | `claude/phase-8-handoff` → auto-rebase |

No PR is safe to merge independently — they form a linear dependency chain. The DEC-1.a falsifying-pattern in #199 references the audit-hypothesis-falsifier output in #198; the audit references the per-candidate briefs in #197; #197 references the exemplar in #196 + the rubric in #195; #195 stacks on the envelope in #194.

## PRs opened (in stack order)

| PR | Branch | Title | Base | Status | Rewind point |
|---|---|---|---|---|---|
| #194 | `claude/phase-8-envelope` | scope envelope | `main` | open | revert `cce0f73` → pre-Phase-8 |
| #195 | `claude/phase-8-auto-008-4CZoC` | auto-008 dispatch brief | #194 | open | revert `99c334e`/`b61cbf5`/`577cea8`/`54438e3` (4 commits; pin each stage) |
| #196 | `claude/phase-8-exemplar` | GF-M exemplar | #195 | open | revert `36616a8` → no exemplar; fanout cannot run |
| #197 | `claude/phase-8-fanout-omnibus` | Wave 8.1 fanout omnibus | #196 | open | revert any of 4 fanout checkpoint commits to roll back partial set |
| #198 | `claude/phase-8-bias-guards` | Wave 8.1.b bias-guards | #197 | open | revert `b8de4cc`/`26c4190`/`ce70523` (3 audit commits) |
| #199 | `claude/phase-8-cross-candidate` | Wave 8.2 cross-candidate brief | #198 | open | revert `5de0bba` → no cross-candidate brief; downstream cannot run |
| #200 | `claude/phase-8-handoff` | Phase-8-close handoff | #199 | open | revert `d5cae02` → handoff + AGENT-ENTRY revert |
| TBD | `claude/phase-8-summary-retro` | summary + retro (this PR) | #200 | will-open | revert this PR's HEAD |

## Decision briefs written

| Brief | Rounds | Verdict |
|---|---|---|
| [`auto-008` Phase-8 dispatch shape](architectures/v3/decisions/auto-008-phase-8-dispatch-shape.md) | R1 (3 reviewers) + R2 (3 reviewers) + post-R2 patches | 6/6 `accept-with-named-amendments`; all amendments folded. Option A′: per-candidate parallel fanout + A.2′ 3 cross-candidate bias-guards serial-after-Wave-8.1 + lead-agent cross-check + lead-agent Wave-8.2. |

## Chain status

- Phase 7 closed at the prior run (2026-05-27) per [`SESSION-HANDOFF-2026-05-27-phase-7-close.md`](architectures/v3/SESSION-HANDOFF-2026-05-27-phase-7-close.md).
- **Phase 8 closed at this run** per [`SESSION-HANDOFF-2026-05-28-phase-8-close.md`](architectures/v3/SESSION-HANDOFF-2026-05-28-phase-8-close.md).
- **v3 synthesis pipeline COMPLETE.** No v3 phase remains.
- Downstream simulator-harness execution is post-v3 scope (likely a separate engineering project).

## Morning-review items (advisory only; none blocking)

5 items in the Phase-8-close handoff §"Phase-8-followup carry-forward (deferrals — none load-bearing, all advisory)":

1. **U-A / U-B / D7-U-1 practitioner-thin falsifiers** (per domain-practitioner audit). Downstream simulator-harness should track both **mechanical pass cleanly** AND **practitioner pass cleanly**. Lead-agent recommendation: ship as documented; the simulator-harness's two-tier report is the operational fix.

2. **U-B honest-degradation reconciliation** (per hypothesis-falsifier audit + Wave-8.2 §3). Simulator-harness must compare U-B's brief §2 at lean-eval-start-time vs result-time. Lead-agent recommendation: ship as documented in the cross-candidate brief.

3. **GF-M exemplar under-tier acknowledgement** (4434 vs Light 5000-6500). Wave 8.1 subagents targeted their own tier (all 9 within tier). Lead-agent recommendation: ship; exemplar's structural clarity is the priority. Non-recurring.

4. **Wave-8.1 fanout multi-checkpoint commits** (4 commits on fanout-omnibus branch due to stop-hook async coordination with subagent file landings). Final state is correct. Lead-agent recommendation: ship; consider a stop-hook adjustment for future runs (don't fire on untracked files that are being asynchronously written by tracked subagents).

5. **H-5 scaffold/harness C11 vocabulary** (Phase-7 historian deferred). Glossary addition opportunity for `decisions-captured.md` or future glossary. Lead-agent recommendation: ship without action; non-blocking; can be folded into any future glossary work.

## What I deliberately did NOT do

- **Did NOT execute the lean-evals.** Phase 8's deliverable is the **design** of 10 per-candidate lean-evals + the cross-candidate evaluator-brief. Execution is post-v3 simulator-harness work.
- **Did NOT adopt the 5 Phase-7 retro AGENTS-MD-* rules into canonical AGENTS.md** (user election at envelope-time via AskUserQuestion). The patterns are applied informally in auto-008 with citation by retrospective-directory path. Flagged in handoff §Honest acknowledgements.
- **Did NOT patch Phase-6 specs.** Wave 7.3 was NOT FIRED in the prior run (matrix-flag + Phase-8 cite-obligation alternative); Phase 8 honored that decision (cite obligations land in lean-eval briefs, not spec patches).
- **Did NOT modify the candidate registry.** The 10-candidate set is frozen post-Phase-4.
- **Did NOT trigger a Round 3 of auto-008 adversarial review.** Round-2 reviewers' amendments did not converge on a different option (all 3 returned `accept-with-named-amendments` with surgical patches to Option A′); folded inline as post-R2 patches.

## Rewind points (full chain)

| SHA | What it undoes |
|---|---|
| `cce0f73` | Phase-8 scope envelope; run is "pre-decision" |
| `54438e3` | auto-008 Round 1 brief |
| `7e685c5` | auto-008 Round 2 amendments |
| `577cea8` | auto-008 Round 2 SHA-pin |
| `b61cbf5` | auto-008 Round-2-reviewer amendments folded |
| `99c334e` | auto-008 final SHA-pin |
| `36616a8` | GF-M exemplar |
| `fd057db` | BF-S Wave 8.1 (first checkpoint) |
| `56928ad` | 7 Wave 8.1 briefs (second checkpoint) |
| `91baae2` | U-A new + 3 Wave 8.1 updates (third checkpoint) |
| `ce70523` | Wave 8.1.b falsification-designer audit |
| `26c4190` | Wave 8.1.b domain-practitioner audit |
| `b8de4cc` | Wave 8.1.b hypothesis-falsifier audit + lead-agent cross-check |
| `5de0bba` | Wave 8.2 cross-candidate evaluator-brief |
| `d5cae02` | Phase-8-close handoff + AGENT-ENTRY update |

## Session metadata

- **Branch chain at run end** (stack bottom → top): `claude/phase-8-envelope` → `claude/phase-8-auto-008-4CZoC` → `claude/phase-8-exemplar` → `claude/phase-8-fanout-omnibus` → `claude/phase-8-bias-guards` → `claude/phase-8-cross-candidate` → `claude/phase-8-handoff` → `claude/phase-8-summary-retro` (this PR's branch).
- **Subagent count: 18** (6 adversarial reviewers on auto-008 R1+R2 + 9 Wave-8.1 per-candidate fanout + 3 Wave-8.1.b bias-guards).
- **PR count: 8** (against 15-PR phase budget; 7-PR margin).
- **Phase**: 8 (final v3 synthesis phase).
- **Run start**: 2026-05-28 (after Phase-7 close at 2026-05-27).
- **Run end**: 2026-05-28 (this run; same-day execution).
