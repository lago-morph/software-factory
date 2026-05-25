# ADR: Unattended-session decisions — brief + adversarial review + rewind point

- **ID**: ADR-f702da3352
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-134.md
- **PRs covered**: #134

## Context

The project's existing convention (in [`AGENTS.md`](../../AGENTS.md) §"Interactive operation") is that in real-time conversation with the user, the agent doesn't start substantive work the user didn't ask for. The carve-out clause already exists: *"Doesn't apply to unattended sessions where the user delegated execution"*. But the project had no defined protocol for what an unattended session should *do* when it hits a question that would normally require user input — the absence of guidance left two bad failure modes: (a) the agent stops and idles, wasting overnight time; (b) the agent makes an undocumented unilateral choice that the user can't easily rewind.

At the end of PR #134, the user designed a third option and described it as the protocol for an upcoming overnight run: when the unattended agent would normally ask the user a question, it instead writes a **decision brief** documenting the question, the alternatives considered, and the chosen option with reasoning; dispatches **2-3 adversarial-reviewer subagents** to attack the brief from independent angles; incorporates the strongest objections (revising the brief or changing the decision); commits the brief on its own **stacked branch** (so the user can rewind back to the decision point in the morning if they disagree); and proceeds as if the user had authorized the chosen option. The user explicitly said "I'd rather you get a lot of work done overnight than do nothing."

## Decision

**For unattended sessions, when the agent would normally ask the user a question, it instead writes a decision brief, dispatches 2-3 adversarial-reviewer subagents to attack the brief, incorporates the strongest objections, commits the brief on its own stacked branch off the prior feature branch, and proceeds as if the user authorized the chosen option.** Every decision is reversible by reverting to the stacked branch's parent. The brief format covers: the question, the alternatives (≥3 when plausible), the chosen option, the reasoning, the adversarial-review summary (which objections were incorporated, which were rejected and why), and an explicit "if-user-overrides" rewind point. Decision briefs live in the relevant project directory (e.g., `architectures/v3/decisions/auto-NNN-<slug>.md` for v3 work) and are listed in the morning-summary doc at the repo root.

## Alternatives considered

- **Agent stops and idles when it hits a question.** Rejected because the whole point of overnight delegation is to get work done. Idling wastes the entire window.
- **Agent makes unilateral undocumented choices.** Rejected because the user has no audit trail in the morning; rewinding requires reconstruction of what the agent was thinking. The decision-brief artifact is the audit trail.
- **Agent dispatches reviewers but doesn't commit a brief.** Rejected because the reviewers' findings need to be durable; if the brief lives only in agent memory, the user can't see what was considered, only what was decided.
- **Single reviewer per decision instead of 2-3 adversarial.** Rejected because a single reviewer often shares the deciding agent's framing (the trap the playback-and-confirm rule addresses); independence of attack angle is what produces useful objections. The user specified "adversarial reviewers" plural.
- **Non-stacked branching (all decisions land on one long branch).** Rejected because the rewind unit then becomes "everything since the agent started" instead of "this one decision". Stacked branches make decisions individually reversible.

## Consequences

**Easier.** Overnight runs produce continuous progress instead of idling at the first ambiguity. The morning review surface is uniform — a list of decision briefs, each with rewind points, paired with stacked PRs that can be merged à la carte. The adversarial-review step catches a non-trivial fraction of misreads before they propagate (the playback-and-confirm trap, but with subagents as the playback audience).

**Harder.** Each ambiguity-point now costs at least one brief + 2-3 subagent dispatches + the brief revision. Overnight throughput is lower than pure forward motion. Stacked-PR discipline must be airtight — a misaligned base branch cascades through the rest of the stack. The agent must judge which questions are "ambiguous enough to need a brief" vs. "obvious"; over-triggering produces brief sprawl, under-triggering produces undocumented choices.

**Accepted trade-off.** The protocol favors reversibility and audit-trail over raw throughput. The user explicitly stated this preference: "I'd rather you get a lot of work done overnight than do nothing" — but combined with "rewind back to where the decision was against my intent" implies the rewind path must be cheap. Stacked branches + decision briefs make rewind cheap; that's the design point.

## References

- [`../2026-05-25-134.md`](../2026-05-25-134.md) — source retrospective.
- [`../../.claude/skills/stacked-pr-on-feature-branch/SKILL.md`](../../.claude/skills/stacked-pr-on-feature-branch/SKILL.md) — existing stacked-PR convention this builds on.
- [`../../.claude/skills/subagent-prompting/SKILL.md`](../../.claude/skills/subagent-prompting/SKILL.md) — existing subagent-briefing reference.
- [`../../.claude/skills/parallel-subagent-fanout/SKILL.md`](../../.claude/skills/parallel-subagent-fanout/SKILL.md) — adversarial-reviewer dispatch composes with this.
- [`../../AGENTS.md`](../../AGENTS.md) — interactive vs. unattended carve-out.
- [`./SKILL-SPEC-d12265e4f6-decision-brief-with-adversarial-review.md`](./SKILL-SPEC-d12265e4f6-decision-brief-with-adversarial-review.md) — the skill that operationalises this ADR.
- PRs the decision was made in: #134.