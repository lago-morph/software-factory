# agent instruction

**Every adversarial-review round needs a regression-verifier persona.** In a multi-round adversarial review loop, dispatch one reviewer per round whose sole job is to confirm the previous round's fixes are complete and introduced no new defect, reporting an explicit COMPLETE/INCOMPLETE verdict per named fix. A fix can be internally self-consistent yet inconsistent with the rest of the artifact; only a verifier that re-checks the prior fixes by name catches a half-applied correction before it ships.

*Grounded in: the round-2 and round-3 regression verifiers confirming the fence/eval and C20 fixes COMPLETE.*

# justification

In this session the round-1 fix for the fence/eval ordering contradiction touched nine separate locations (two Mermaid diagrams, three prose passages, three tables, one scheduling note). A fix spread that wide is exactly where a half-application hides — update eight places, miss the ninth, and the artifact is now internally contradictory in a *new* way. The round-2 regression verifier was briefed to check all nine by name and returned "FIX-1 fence/eval: COMPLETE" with the specific edge annotations it confirmed; the round-3 verifier did the same for the seven-products restructure and the fence caveat. Both came back clean, which is the only reason the loop could terminate with confidence rather than hope. The marginal cost is one extra subagent per round, briefed with the named fixes. The cost of omitting it is shipping a correction that fixed the reported contradiction while quietly creating another — the precise failure the review loop exists to prevent. A general adversarial reviewer hunts for new problems; it does not reliably re-verify old ones unless told to, by name.
