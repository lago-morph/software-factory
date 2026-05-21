# agent instruction

**Backfill missed conventions on mid-session catch.** If the agent discovers it touched a tool surface governed by a process skill without first loading the skill — typically because a gate fired, the user pointed it out, or a downstream check tripped — load the skill immediately and post a retroactively-flagged comment / commit / artifact capturing the events that already happened. Mark the backfill explicitly (e.g. "Posted retroactively — work was already underway and PR #N has just been opened"). Silent skipping erodes the per-issue / per-PR audit trail the conventions exist to maintain.

*Grounded in: PR #116, where the missed `issue-management` load was caught mid-session and the STARTED + PR-OPENED comments were posted on issue #105 with an explicit "Posted retroactively" preamble, restoring the audit trail rather than pretending the slip didn't happen.*

# justification

When the user pointed out that `issue-management` had been skipped on issue #105, the right move was not to silently move on. The skill defines a STARTED claim, an assignee write, and a `good first issue` label that *should have happened* the moment I first read the issue. Backfilling means posting those things now, with a one-line marker that they're retroactive. The thread then reads as: issue opened → agent claimed it (retro) → PR opened (retro) → PR merged → issue auto-closed. The marker preserves the convention's audit-trail property — a later reader can scan for `[STARTED]` and find one — without rewriting history dishonestly.

The marginal cost of the rule is the few seconds it takes to compose a "Posted retroactively" preamble and a paragraph naming what already happened. The cost of skipping it is two-fold: the audit trail is broken (the conventions exist precisely to be scannable), and the failure becomes invisible to the post-mortem. Misses that get silently elided don't accumulate as feedback; the retrospective two weeks later can't see the slip happened at all. Backfilling makes the miss visible, which is what surfaces it as a candidate for mechanical enforcement (which then became PR #117's PreToolUse gate).
