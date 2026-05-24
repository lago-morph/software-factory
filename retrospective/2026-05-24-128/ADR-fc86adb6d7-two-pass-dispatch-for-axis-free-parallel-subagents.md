# ADR: Two-pass dispatch for axis-free parallel subagents

- **ID**: ADR-fc86adb6d7
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-24
- **Source retrospective**: ../2026-05-24-128.md
- **PRs covered**: #128

## Context

Phase 2 of the v3 architecture synthesis dispatched 9 parallel subagents in three groups: 3 greenfield, 3 brownfield, and 3 unified-mandate "no-axis-prescribed" tracks. The unified tracks all received the same brief: "Find ONE architecture that addresses both mandates; pick your own organizing axis; defend the choice." The expected design signal was the divergence-vs-convergence pattern across the three independent picks — convergence indicates a corpus-supported axis, divergence indicates multiple defensible architectures.

In practice, two of three unified tracks picked the same tier-based axis. The axis-divergence auditor later showed the convergence was at least partly prompt-anchoring (an F-mode wording in a primary artifact had named the tier pattern; the prompt's candidate-axis list included "stakes / risk-tier"; both of these biased the subagents toward the tier choice). An off-list supplementary track dispatched after the contamination was identified found a defensible alternative axis (verification-topology), retroactively proving the original convergence was not pure corpus signal.

The structural failure: single-pass independent dispatch can't distinguish corpus-signal convergence from prompt-anchored convergence after the fact, and the lead agent can't tell which has occurred without an additional test. The blind-axis test (D7 of the v3 work) catches it after the fact, but only after the expensive full dispatch has already happened.

The user proposed a "Claude team" alternative: let the subagents coordinate before they start. The Agent tool dispatches subagents in isolated contexts; they cannot directly communicate. But the lead agent can orchestrate a multi-pass dispatch that approximates coordination: pass 1 = each subagent proposes its axis in a short paragraph without doing the architecture work; lead agent reviews; pass 2 = each subagent does the architecture work with the prior picks visible (or with convergent picks prohibited for the convergent subagents).

## Decision

When N parallel subagents are dispatched on the same axis-selection problem with no prescribed axis, use a two-pass design:

1. **Pass 1 — axis proposal.** Dispatch all N subagents in parallel with a short brief: "Propose your organizing axis in one paragraph and defend it. Do NOT do the architecture work yet."
2. **Lead-agent coordination.** Read the N proposals. If two or more converged on the same axis, decide whether to (a) allow the convergence and proceed to pass 2 as-is (corpus-signal-likely case), (b) prohibit the convergent axis for the convergent subagents on their pass-2 dispatch (forced divergence), or (c) dispatch a supplementary off-list track in parallel with pass 2.
3. **Pass 2 — execution.** Dispatch all N subagents in parallel with the full architecture brief, the prior axis proposals visible, and any prohibitions applied per step 2.

This replaces single-pass independent dispatch for axis-free problems. Single-pass remains appropriate for axis-prescribed problems (e.g., the 6 mandate-specific tracks of the v3 work each had a predetermined axis).

## Alternatives considered

- **Status quo: single-pass independent dispatch, off-list test after the fact.** Rejected: the off-list test happens after the expensive full dispatch. When the convergence is prompt-anchored, the full dispatch's output is unusable and must be re-run from cleaned sources. The two-pass design catches the convergence before the expensive work.
- **Sequential dispatch with cumulative prohibition.** Track 7 dispatches first; once it picks axis X, track 8 dispatches with "X prohibited"; track 9 dispatches with "X and Y prohibited." Rejected: order-effect bias (track 7 has more axis freedom than track 9 by construction); 3× the wall-clock time of parallel dispatch.
- **Pre-specified axes.** Lead agent picks 3 candidate axes upfront and assigns one per track. Rejected: loses the "let the corpus tell us which axis" framing entirely; lead-agent's axis-choices could themselves be biased.
- **Multi-agent negotiation framework.** Some agent frameworks support direct subagent-to-subagent communication. Rejected for this project: the Agent tool used here does not support it; adding a new framework introduces dependency risk for one pattern.

## Consequences

What becomes easier: the lead agent can detect prompt-anchored convergence before paying the full dispatch cost. The convergence-vs-divergence signal is preserved (pass 1 still produces independent proposals).

What becomes harder: two-pass adds wall-clock latency (~5-10 minutes for the pass-1 proposal phase) and one more lead-agent decision point (reviewing the proposals and deciding whether to enforce divergence). The discipline must be applied consistently — applying it sometimes but not others creates inconsistent expectations about parallel-subagent output reliability.

Trade-off knowingly accepted: every axis-free parallel dispatch now pays a ~10-minute pass-1 cost. The cost is paid every time. The single-pass alternative was cheaper per dispatch but each contamination event cost hours of re-runs.

## References

- [`../2026-05-24-128.md`](../2026-05-24-128.md) — the source retrospective.
- [`./SKILL-SPEC-51fe4d298e-parallel-subagent-axis-coordination.md`](./SKILL-SPEC-51fe4d298e-parallel-subagent-axis-coordination.md) — the skill spec that operationalizes this design.
- [`./AGENTS-MD-34dcf2c29f-off-list-test-for-convergent-parallel-subagents.md`](./AGENTS-MD-34dcf2c29f-off-list-test-for-convergent-parallel-subagents.md) — the AGENTS.md rule for the off-list test (which becomes a fallback when two-pass is skipped).
- PR #128 — Phase-2 work where the single-pass failure was diagnosed and the two-pass design was proposed.
