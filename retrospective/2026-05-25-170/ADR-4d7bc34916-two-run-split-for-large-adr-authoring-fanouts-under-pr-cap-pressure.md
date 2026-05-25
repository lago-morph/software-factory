# ADR: Two-run split for large ADR-authoring fanouts under PR-cap pressure

- **ID**: ADR-4d7bc34916
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-170.md
- **PRs covered**: #165, #168

## Context

The autonomous-run skill caps each run at 30 PRs. The 2026-05-25 Phase-5-entry run's auto-005 Round-1 cost-hawk reviewer demonstrated that the originally-proposed single-run Phase 5 (Waves 5.1 + 5.2 + 5.3, ~54-62 ADRs total) would consume 15-20 PRs by itself, leaving zero margin against the cap when factoring in Phase A's 6 PRs, the decision-brief PR, the handoff, and the morning summary. Re-dispatch on any failed subagent would push past 30. The Round-2 amendment split the work across two runs at the wave boundary: this run delivers Wave 5.1 + 5.2 (27 ADRs in ~10 PRs); a successor run delivers Wave 5.3 (29 ADRs).

The split required a binding mechanism so the successor run actually executes Wave 5.3 rather than drifting (all three Round-2 reviewers raised this concern). See [ADR-???? deferred-work binding-artifact pattern](./ADR-77fb06d28a-always-write-a-full-retrospective-package-lean-mode-is-the-anti-pattern.md) for an unrelated but co-discovered pattern; the relevant binding-artifact handoff was authored in PR B4 (#168).

## Decision

**When a planned ADR-authoring phase would consume more than ~10 PRs in a single autonomous run, split it across two runs at a phase boundary that preserves cross-reference stability** — common ADRs (framework + discipline) in the first run; candidate-specific and per-variant ADRs in the second run. The split is authorized by the parent decision brief's Round-2 amendments, and the binding mechanism is the session handoff doc + morning summary + (optionally) next-run dispatch prompt, per the deferred-wave-binding-handoff skill.

## Alternatives considered

- **Single-run dispatch of all ADRs.** Rejected because PR-cap pressure forces re-dispatch fragility — any subagent failure in Wave 5.3 (the 29-ADR wave) would push past the 30-PR cap mid-run, requiring an emergency wrap-up. The cost-hawk's math: 7 PRs in flight + 10 Phase-5 PRs + 3 Phase-B-close PRs = 20 PRs used with only 10 margin; insufficient for even modest re-dispatch.
- **Split at a different boundary** (e.g., commodity-tier in run A; designed-system + per-candidate in run B). Rejected because designed-system framework ADRs (P-19, P-28, P-29, P-30) need to be settled before per-variant ADRs reference them; deferring framework ADRs to run B would force run B's per-variant subagents to wait on intra-run dispatch ordering, eroding parallelism.
- **Stretch the PR-cap to 40 or 50 for "large" runs.** Rejected because the cap is grounded in reviewer-throughput limits (a human reviewing 30 stacked PRs is already heavy; 50 is impractical) and aggregation-budget limits (the lead agent's context budget at 50 PRs of subagent returns).

## Consequences

**Easier:** Each of the two runs stays well under the PR cap (this run: 12 PRs; next run: ~10-15 PRs estimated for Wave 5.3 + handoff). Re-dispatch budget is preserved in each run. Wave 5.3 benefits from settled Wave-5.1+5.2 ADR IDs for cross-references (no race condition on ID assignment). Phase 6 (architecture spec authorship) benefits from being able to inform Wave 5.3 if the user adopts the Phase-6-may-run-concurrently variant.

**Harder:** Wave 5.3 incurs a session-startup cost (new run needs to read the handoff + auto-005 Round 2 + the 27 Wave-5.1+5.2 ADRs as input). The deferral requires triple-write across handoff + summary + next-prompt to be binding. Phase-6 dispatch is gated until Wave 5.3 closes (or an adversarially-reviewed waiver lands), adding 1 extra session boundary in the worst case.

**Trade-off accepted:** Two-session overhead for Phase 5 in exchange for re-dispatch safety + cross-reference cleanliness.

**Explicitly NOT promising:** the rule does not name a hard PR-count threshold. ~10 PRs is the rule-of-thumb for "needs a split"; the lead agent's scope analysis (and Round-1 adversarial review) is the actual decision authority. A run that's planned at 14 PRs with high confidence and zero re-dispatch risk may stay single-run.

## References

- [`../2026-05-25-170.md`](../2026-05-25-170.md) — source retrospective.
- [`./SKILL-SPEC-b62e17f619-deferred-wave-binding-handoff.md`](./SKILL-SPEC-b62e17f619-deferred-wave-binding-handoff.md) — the binding mechanism for the deferred wave.
- [`./SKILL-SPEC-2412f18523-wave-split-with-checkpoint.md`](./SKILL-SPEC-2412f18523-wave-split-with-checkpoint.md) — intra-run wave-split discipline (related but distinct from cross-run split).
- [`../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md`](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) § Decision (Round 2) — the parent decision brief.
- [`../../architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5a-close.md`](../../architectures/v3/SESSION-HANDOFF-2026-05-25-phase-5a-close.md) — the binding artifact for Wave 5.3.
- [`../../.claude/skills/autonomous-run/SKILL.md`](../../.claude/skills/autonomous-run/SKILL.md) § Stacked-PR discipline — the 30-PR cap rule.
- PRs: #165 (auto-005 Round 2 codified the split), #168 (handoff carrying the binding artifact).
