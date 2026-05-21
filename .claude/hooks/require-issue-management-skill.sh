#!/usr/bin/env bash
# require-issue-management-skill.sh
#
# PreToolUse gate for the `issue-management` skill. Blocks any call to
# an issue-touching GitHub MCP tool unless the skill has been loaded
# in this session (signalled by the existence of /tmp/.claude-skill-loaded-issue-management).
#
# Installed by: .claude/skills/issue-management/scripts/install.py
# Wired up via: .claude/settings.json -> hooks.PreToolUse
#
# Why this exists:
#   The issue-management skill defines mandatory conventions for every
#   touch of a GitHub issue (STARTED label/assignee + comment, PR-OPENED
#   comment, CREATE-ISSUE auto-label, etc.). Those conventions are
#   silently skipped if the agent forgets to load the skill — the failure
#   mode that bit us once already. This hook makes the load
#   deterministic: no marker, no issue tool calls.
#
# Allow path:
#   - The marker file exists. Exit 0; tool call proceeds.
#
# Block path:
#   - No marker. Exit 2 with an instructive stderr; Claude Code surfaces
#     the stderr to the agent so it can correct course (load the skill,
#     then retry).
#
# Bypass:
#   - To bypass intentionally (e.g. a one-off read in a context where
#     loading the skill is genuinely not warranted), `touch` the marker
#     manually. The hook does not police what produced the marker — only
#     that it exists.

set -euo pipefail

MARKER="/tmp/.claude-skill-loaded-issue-management"

if [[ -f "$MARKER" ]]; then
    exit 0
fi

# Read & discard the tool-use JSON on stdin (Claude Code passes it; we
# don't need it for the allow/block decision but reading it keeps the
# pipe clean).
cat >/dev/null 2>&1 || true

cat >&2 <<'EOF'
[issue-management gate] BLOCKED.

You are about to call a GitHub MCP tool that touches an issue
(mcp__github__issue_*, add_issue_comment, list_issues, search_issues,
or sub_issue_write), but the `issue-management` skill has not been
loaded in this session.

To unblock:
  1. Invoke the issue-management skill (Skill tool with
     skill=issue-management). The skill's pre-flight runs
     install.py --check, which creates the marker file at
     /tmp/.claude-skill-loaded-issue-management.
  2. Retry the tool call.

The issue-management skill defines the conventions that MUST fire on
every issue touch (STARTED comment + claim labels, PR-OPENED comment,
CREATE-ISSUE auto-label with `help wanted`, etc.). Skipping them
breaks the per-issue audit trail this repo relies on.

If you have a genuine reason to bypass this gate one time
(e.g. recovery scenario), run:
  touch /tmp/.claude-skill-loaded-issue-management
and retry. The skill load is not policed by the hook — only the marker.
EOF

exit 2
