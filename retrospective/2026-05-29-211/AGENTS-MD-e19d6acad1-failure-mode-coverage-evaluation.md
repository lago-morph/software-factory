# agent instruction

**Failure-mode coverage matrix for architecture evaluation.** "When evaluating an architectural plan that operates in a domain with a defined catalog of failure modes, produce an explicit coverage matrix mapping every catalogued failure mode against the plan's mechanisms with a four-class status (Addressed, Partial, Gap, Caution). Catalogued failures that go unmapped are silent risks; the matrix makes them visible. Especially flag Caution modes — places where the plan's design could worsen a failure if not actively guarded."

*Grounded in: v4 F-mode coverage analysis (PR #210) mapped all 61 F-modes and surfaced 4 Cautions (F52 Tempting-Wrong-Hybrid, F35 Federation drift, F47 Goodhart, F25 Design starvation) that would have been hidden without the matrix.*

# justification

The v4 F-mode coverage matrix surfaced 4 Cautions and 11 Gaps that would otherwise have hidden in the plan's optimism. F52 specifically — v4's emphasis on self-healing + self-optimization is exactly the "more controller patches" Schillace warns against; the matrix forced this admission. Without the matrix, v4 would have shipped with the optimism intact and discovered the cautions during implementation, at which point reverse-engineering the design discipline is more expensive than baking it in. The marginal cost of producing the matrix is one focused session against the failure-mode catalog; the cost of not producing it is shipping a plan that quietly amplifies known failure modes.
