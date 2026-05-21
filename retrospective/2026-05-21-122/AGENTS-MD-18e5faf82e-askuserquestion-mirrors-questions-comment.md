# agent instruction

**AskUserQuestion about an in-flight issue must be mirrored as a `[QUESTIONS]` comment FIRST.** Before calling `AskUserQuestion` (or any equivalent chat picker) with a question about a GitHub issue you are currently working on — including scope, planning, option-picker, and direction-confirmation questions — post a `[QUESTIONS]` comment on the issue thread per the `issue-management` skill's QUESTIONS behavior, apply the `question` label, then touch `/tmp/.claude-skill-issue-management-ask-suppress` and call the chat tool. There is no carve-out for "this is just scoping" or "this is just lightweight."

*Grounded in: PR #122 / issue #104 — twice-repeated AskUserQuestion-without-QUESTIONS-comment failure inside a single session.*

# justification

This rule is the project-level statement of the discipline the `issue-management` skill's new PreToolUse reminder hook enforces. The session that produced PR #122 saw the agent (a) invoke `AskUserQuestion` to scope issue #104 without posting on the issue thread, get caught by the user, (b) author a diagnosis of why it had failed, then (c) repeat the exact same mistake one tool-call later, *while writing the diagnosis*. That double-failure inside ~5 minutes is the strongest possible signal that prose-level recall of the convention is not sufficient.

The cost of breaking the rule is high: a scoping question answered in chat leaves the issue thread without the durable record of why the agent took the path it took. A future agent picking up the same issue cold has no audit trail for the scope decision — they see the original issue body, the agent's STARTED comment, and then implementation commits with no recorded rationale. The cost of following the rule is one filesystem touch (`touch /tmp/.claude-skill-issue-management-ask-suppress`) plus the comment-post itself (which the issue-management skill templates make trivial). Asymmetric: high cost of skipping, near-zero cost of complying. The PreToolUse hook makes compliance mechanical — but a project-level rule in `AGENTS.md` is what tells the human reviewer (and any non-Claude agent) that the convention is binding, not optional skill flavor.
