#!/usr/bin/env bash
# remind-questions-on-askuserquestion.sh
#
# PreToolUse reminder for the `issue-management` skill. Fires on every
# AskUserQuestion call within a session where the issue-management skill
# has been loaded, exiting 2 with a short stderr reminder that any
# AskUserQuestion about an in-flight issue is a `[QUESTIONS]` event and
# the issue-thread comment + `question` label must be posted FIRST.
#
# Installed by: .claude/skills/issue-management/scripts/install.py
# Wired up via: .claude/settings.json -> hooks.PreToolUse
#
# Why this exists:
#   The issue-management skill's QUESTIONS behavior fires on "agent has
#   clarifying questions for the user about an in-flight issue". In
#   practice the agent reaches for AskUserQuestion (ergonomic chat
#   picker) and forgets to mirror the question on the issue thread.
#   The mistake costs the issue its durable record of why the agent
#   chose the path it chose. Prose-level rules in SKILL.md are not
#   sufficient — this session demonstrated the same mistake twice in a
#   row even while diagnosing it. The hook supplies mechanical friction
#   so the rule has to be considered every time.
#
# Allow path:
#   - The issue-management skill marker does NOT exist (i.e. the skill
#     is not loaded in this session). Exit 0.
#
# Block path:
#   - The skill marker DOES exist (we are in a session that loaded
#     issue-management). Exit 2 with a short stderr reminder. The
#     agent's response is to:
#       (a) decide whether the AskUserQuestion is about an in-flight
#           issue,
#       (b) if yes — post a `[QUESTIONS]` comment + apply `question`
#           label per the skill, then re-call AskUserQuestion,
#       (c) if no — re-call AskUserQuestion immediately.
#
# Bypass:
#   - One-off bypass: `touch /tmp/.claude-skill-issue-management-ask-suppress`
#     before the AskUserQuestion call. The hook deletes the suppress
#     marker after honouring it so it cannot accidentally silence
#     subsequent calls.

set -euo pipefail

SKILL_MARKER="/tmp/.claude-skill-loaded-issue-management"
SUPPRESS_MARKER="/tmp/.claude-skill-issue-management-ask-suppress"

# If the skill is not loaded in this session, the hook has nothing to
# do — we're not in issue-management territory.
if [[ ! -f "$SKILL_MARKER" ]]; then
    exit 0
fi

# Honour a one-off suppress. The agent uses this when it has already
# evaluated the call and confirmed the question is not about an issue
# (or has posted the QUESTIONS comment already).
if [[ -f "$SUPPRESS_MARKER" ]]; then
    rm -f "$SUPPRESS_MARKER"
    exit 0
fi

# Read & discard the tool-use JSON on stdin.
cat >/dev/null 2>&1 || true

cat >&2 <<'EOF'
[issue-management] AskUserQuestion reminder.

The `issue-management` skill is loaded in this session, which means you
may be working an in-flight GitHub issue. The skill's QUESTIONS
behavior triggers on ANY clarifying question for the user about an
in-flight issue — including scope, planning, and option-picker
questions. There is no carve-out for "this is just scoping" or "this is
just lightweight."

Before calling AskUserQuestion, evaluate:

  Is this question about an issue I'm currently working
  (STARTED but not yet PR-OPENED / closed)?

If YES:
  1. Post a `[QUESTIONS]` comment on the issue thread using
     templates/comment-questions.md (one batched, numbered list).
  2. Apply the `question` label
     (`issue_write update labels=[...existing, "question"]`).
  3. Touch the bypass marker so this hook lets the next AskUserQuestion
     through:
       touch /tmp/.claude-skill-issue-management-ask-suppress
  4. Re-call AskUserQuestion.
  5. After the user answers, post an `[ANSWERS]` comment and remove the
     `question` label.

If NO:
  1. Touch the bypass marker:
       touch /tmp/.claude-skill-issue-management-ask-suppress
  2. Re-call AskUserQuestion.

The bypass marker is single-use — it is deleted by this hook the first
time it is honoured, so it cannot accidentally silence later calls.
EOF

exit 2
