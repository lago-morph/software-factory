# agent instruction

**Ask before producing when the user requests information.** When the user's request uses informational verbs ("tell me", "give me", "I want to understand", "help me decide", "what would you recommend"), produce information first — proposals, summaries, options with trade-offs — and wait for the user to respond before implementing. Implementation verbs ("build", "create", "make", "produce", "go") authorize action. The asymmetry is sharp: jumping to implementation when the user wanted information forces them to interrupt, undo work, and re-frame; producing information when the user wanted implementation costs only a re-prompt.

*Grounded in: build-guide session 2026-05-28, when the agent started writing PHASE-7-SUMMARY.md after the user's "more information so I can make a decision" request — the file had to be deleted and the branch dropped.*

# justification

The agent in this session repeatedly jumped from "the user asked a question" to "the user asked for an artifact." Three times in one session the user had to interrupt and clarify that they were asking for information, not action: once when the agent began writing a Phase-7 summary after a diagnostic was requested; once when the user clarified that listing authors-by-name as the answer to "what should I compare against?" was unhelpful; and implicitly throughout the build-guide negotiation, where the user kept having to constrain the agent's eagerness to start producing.

The cost of each instance was real. The PHASE-7-SUMMARY.md case required the agent to delete an in-progress file, drop the branch, and explicitly acknowledge the misread. The cumulative cost across the session was significant agent-attention and user-attention churn — and the implicit signal to the user that the agent could not be trusted to listen to the actual question.

The marginal cost of adopting this rule is small. It costs one additional sentence at the start of a response: "Before I produce anything, here's what I would produce — does this match what you want?" If the user wanted action, they say "yes go." If they wanted information, they got information. Either way the agent has avoided producing the wrong artifact.

The asymmetry — small cost to ask, large cost to misfire — is exactly the kind of decision an AGENTS.md rule should encode. The information-verb / implementation-verb heuristic is mechanical enough to apply quickly without freezing on every interaction.
