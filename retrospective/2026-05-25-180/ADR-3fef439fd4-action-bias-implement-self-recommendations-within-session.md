# ADR: Action-bias — implement self-recommendations within session

- **ID**: ADR-3fef439fd4
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-180.md
- **PRs covered**: #169, #171

## Context

The 2026-05-25 Phase-5-entry morning summary (PR #169) surfaced 4 morning-review items as "decisions the lead agent did NOT auto-decide; they are surfaced for user review." Three of the four items had:
- Clear lead-agent recommendation.
- Reversible execution path.
- No genuine ambiguity in the recommendation.

The user explicitly rebuked the pattern in PR #169 line-80: "I agree with this, do it. **You are supposed to recommend an action and run with it.** You recommended this action, you should have implemented it immediately. Do it now." And in line-105, on the Wave 5.3 deferral: "I am very confused why you did not continue to phase 5b." Both rebukes reflect the same failure: the agent triaged decisions to the user that the agent had already determined were the right call and that were reversible.

The failure pattern compounds across N parallel agents: each agent's "here's my recommendation, awaiting your call" reply becomes a triage item for the user, who then has to round-trip just to authorize work the agent already determined was correct. The user-as-traffic-cop model fails at multi-agent scale.

## Decision

**When the lead agent recommends an action AND the action has no genuine ambiguity AND the action is reversible AND the agent has session budget, the agent MUST implement the action within the same session.** Queuing self-recommendations for user adjudication is the failure pattern. Reserve user-adjudication for genuinely ambiguous or irreversible decisions.

## Alternatives considered

- **Always queue recommendations for user adjudication (status quo).** Rejected by the user's explicit rebuke. The autonomous-run skill's "prefer reversible action" working-mode rule already advocates for action-bias; this ADR sharpens "reversible action" into a concrete protocol.
- **Always implement (no user-adjudication gate at all).** Rejected because some decisions are genuinely ambiguous or have irreversible consequences (e.g., a destructive git operation, a public release announcement). The triage stays for those.
- **Per-decision policy declared at brief-write time.** Rejected because the brief-author doesn't know at write-time whether the user will be running multiple parallel agents at adjudication-time. A blanket action-bias default with documented exceptions is simpler.

## Consequences

**Easier:** Morning-review batches shrink — items the agent confidently recommends + reversibility get implemented, not queued. User triage is reserved for genuine adjudication. Multi-agent workflows where the user is context-switching benefit most.

**Harder:** The lead agent must distinguish "genuinely ambiguous" from "I'm uncertain because I'm being cautious". The reversibility test gives a concrete out: any reversible action with a clear rewind path is fair game; irreversible actions stay queued.

**Trade-off accepted:** Occasionally implementing an action the user would have wanted to discuss, in exchange for not making the user authorize work the agent already decided was right. The mitigation is reversibility — every implementation produces a stacked PR the user can revert.

**Explicitly NOT promising:** the rule doesn't override AGENTS-MD-d72e1a4f3c (adversarial-review-MUST-be-real-subagents) or any other binding gate. Architectural decisions still require adversarial review; this ADR is about post-recommendation execution, not about whether the recommendation is sound.

## References

- [`../2026-05-25-180.md`](../2026-05-25-180.md) — source retrospective.
- [`./AGENTS-MD-d63a08e7c3-action-bias-for-self-recommended-reversible-actions.md`](./AGENTS-MD-d63a08e7c3-action-bias-for-self-recommended-reversible-actions.md) — per-rule agents-file addition.
- [`./ADR-0dbcfe62e9-self-imposed-deferrals-are-checkpoints-not-stops.md`](./ADR-0dbcfe62e9-self-imposed-deferrals-are-checkpoints-not-stops.md) — companion ADR; deferrals are a specific case of this rule applied to phase-boundary scope.
- PR #169 line 80 + line 105 — user rebuke commit-of-record.
- PR #171 — the action-bias execution of the Phase-4-rule adoption.
