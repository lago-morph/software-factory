# agent instruction

**Action-bias for self-recommended reversible actions.** When the lead agent recommends an action in a morning-review item, decision brief, or PR description AND the action has no genuine ambiguity AND the action is reversible AND the agent has session budget, the agent MUST implement the action within the same session. Queuing self-recommendations for user adjudication is the failure pattern — the user has to triage them and respond just to authorize work the agent already determined was the right call. Reserve user-adjudication for genuinely ambiguous or irreversible decisions.

*Grounded in: PR #169 line-80 rebuke ("you are supposed to recommend an action and run with it"); PR #169 line-105 rebuke on the Wave 5.3 deferral ("I am very confused why you did not continue to phase 5b").*

# justification

The 2026-05-25 Phase-5-entry morning summary surfaced 4 morning-review items as decisions the agent did NOT auto-decide. Three of the four had clear lead-agent recommendations + reversible execution paths + no genuine ambiguity. The user rebuked both the Phase-4-rule adoption deferral ("you should have implemented it immediately") and the Wave 5.3 deferral ("I am very confused why you did not continue"). Both wasted a user round-trip to authorize what the agent already determined was correct.

The marginal cost of the rule: occasionally executing an action the user would have wanted to discuss. The mitigation: reversibility — every implementation produces a stacked PR the user can revert with one click. The asymmetric cost without the rule: every morning-review batch produces N user-triage tasks for work the agent recommended and the user just confirms. The user-as-traffic-cop model fails at multi-agent scale (when the user is concurrently running several agents, each agent's "awaiting your call" reply is a triage tax that compounds).

The autonomous-run skill's "prefer reversible action" working-mode rule already advocates for action-bias in principle; this rule sharpens the principle into a concrete protocol: reversibility + no-ambiguity + session-budget = execute, don't queue.
