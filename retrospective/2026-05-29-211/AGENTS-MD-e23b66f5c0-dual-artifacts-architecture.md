# agent instruction

**Dual artifacts for major architecture proposals.** "For architectural proposals load-bearing for multiple downstream sessions, produce two paired documents: a human-facing approach document (narrative, diagrams, conversational, per human-scoped-deliverables conventions) AND a dense AI-readable context document (structured sections, navigable, decision history with rationale, all alternatives considered, license caveats, config skeletons). Place both in the same directory. Single-artifact docs serve neither audience well."

*Grounded in: v4 architecture proposal shipped as README.md (human) + AI-CONTEXT.md (AI) in PR #209.*

# justification

A human reader and an AI agent picking up cold need different things. The human wants narrative, diagrams, decisions framed conversationally. The AI agent wants navigable structure, every decision with rationale, every alternative considered, every license caveat, specific config skeletons. A single document trying to serve both either becomes too dense for humans or too narrative for AI pickup. v4's two-doc structure scales: each can grow without polluting the other. The marginal cost is writing one more file at architecture-proposal time, which is small relative to the proposal's total cost. The asymmetry plays out across every future session that picks up the architecture — and for v4 specifically, that's many sessions.
