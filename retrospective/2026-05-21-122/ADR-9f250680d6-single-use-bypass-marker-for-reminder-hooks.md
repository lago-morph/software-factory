# ADR: Single-use bypass marker pattern for reminder-style PreToolUse hooks

- **ID**: ADR-9f250680d6
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-122.md
- **PRs covered**: #122

## Context

This session was tasked with fixing issue #104 (internal doc reference hygiene). Within the first few minutes the agent invoked `AskUserQuestion` (the harness's chat picker) to scope the work — and forgot to mirror the question on the issue thread as a `[QUESTIONS]` comment, which the `issue-management` skill explicitly requires. The user caught it. The agent diagnosed the cause (the skill's QUESTIONS behavior described the trigger abstractly as "needs clarification" and never named the `AskUserQuestion` tool), then proceeded to repeat the exact same mistake one round later, *while authoring the diagnosis*. This twice-in-five-minutes failure was diagnostic data: prose-level recall of conventions is not sufficient when the convention has a carve-out the agent has to evaluate every time. The convention this session adds — "Any `AskUserQuestion` about an in-flight issue is a `[QUESTIONS]` event; post the comment first" — needs mechanical enforcement, not just documentation.

The naïve enforcement options each have a known failure mode. Fire-once-per-session (touch a "warned" marker on first hit, then exit 0) is exactly what the in-session retry data showed is insufficient — the agent forgets between calls. Always-block is unworkable because there are legitimate non-issue questions the harness should let through. Counter-based or time-window fallbacks introduce tuning parameters that nobody will calibrate.

## Decision

Reminder-style PreToolUse hooks (hooks that exist to surface a rule with legitimate carve-outs) fire on every matching tool call when the relevant skill is loaded, exit 2 with the rule reminder, and require a single-use bypass marker file at `/tmp/.<gate-name>-suppress` to allow the next call through. The hook deletes the bypass marker after honouring it, so each subsequent call re-fires unless the bypass is re-touched. The convention name for the marker is `/tmp/.claude-skill-<skill-name>-<verb>-suppress`.

## Alternatives considered

- **Fire once per session (warn marker).** First call exit-2's with the reminder; subsequent calls within the session pass through. Rejected by direct evidence in this very session: the agent retried the failure pattern even after being explicitly warned. The model's working set is not a session-stable container for "I was warned about this 10 minutes ago."
- **Always block / no bypass.** Every matching tool call exit-2's with the reminder, no way to acknowledge-and-proceed. Rejected because there are legitimate non-issue calls (tooling preferences, environment confirmations) that should not require the agent to post on an issue thread first. Always-block produces ceremony for non-applicable cases.
- **Time-window bypass** (e.g., a marker file with a TTL that expires after N seconds or N minutes). Rejected: introduces a tuning parameter (`N`) without a principled value, and the marker's persistence across calls becomes a debugging variable.
- **Counter-based bypass** (e.g., bypass for the next 3 calls). Same problem: arbitrary parameter, weak link to the actual rule's applicability.
- **Environment variable toggle** (e.g., `CLAUDE_ASKUSER_BYPASS=1`). Rejected because environment variables persist for the rest of the session by default; one toggle silences the rule for the rest of the work. The marker-file approach is single-shot by construction (the hook unlinks it).
- **Skill-loaded as the entire signal** (i.e., no separate marker — every AskUserQuestion call exit-2's when the skill is loaded). Rejected: the agent can't proceed at all without an escape valve; the bypass is the escape valve. Tying the bypass to a single-shot artifact gives the agent a clean acknowledgement signal.

## Consequences

What becomes easier:

- Rule recall is mechanical, not aspirational. Every matching call surfaces the rule fresh, so the failure mode "I was told once and forgot under load" doesn't recur.
- The bypass action is a recognised acknowledgement signal. When the agent touches the marker, it has actively decided whether the rule applies — both branches (apply / not-apply) require the same one-line action, so the agent is forced to think about it.
- The pattern generalises. Any future skill with a "rule with carve-outs" enforcement need can adopt the same shape: `/tmp/.claude-skill-<name>-<verb>-suppress`, single-use, hook-deletes-on-honour. The shape becomes a project convention.

What becomes harder:

- Per-call friction on AskUserQuestion (one filesystem touch + a re-call) is real. For an agent that calls AskUserQuestion ten times in a session, that's ten extra round-trips. This is the explicit trade-off: friction is the feature.
- The bypass-marker location is now part of the public contract for the hook. Renaming it later is a breaking change for any in-flight session that has touched the old name.

What we accept:

- The hook is per-session because `/tmp` is per-session in the sandbox. If the session restarts, the bypass marker is gone (along with the skill-loaded marker). That's correct — a restart should re-plant the reminder.
- The hook's exit-2 stderr text must be terse. Long messages train the agent to skim, defeating the friction.

## References

- [`../2026-05-21-122.md`](../2026-05-21-122.md) — the source retrospective.
- [`./AGENTS-MD-18e5faf82e-askuserquestion-mirrors-questions-comment.md`](./AGENTS-MD-18e5faf82e-askuserquestion-mirrors-questions-comment.md) — the project-level rule this pattern enforces.
- The hook implementation: `.claude/skills/issue-management/resources/hooks/remind-questions-on-askuserquestion.sh` (template) and `.claude/hooks/remind-questions-on-askuserquestion.sh` (installed).
- The installer that manages multiple hooks via a list of `HookSpec` entries: `.claude/skills/issue-management/scripts/install.py`.
- PR #122 — the change that ships this pattern in the `issue-management` skill.

<!--
PROMOTION NOTE:
When this draft is adopted into docs/adr/ via the `adr` skill, preserve
the `**ID**: ADR-9f250680d6` line verbatim. The NNNN number in the
docs/adr/ filename is a separate human-friendly sequence; the hash is
the durable identifier and must not drift.
-->
