# agent instruction

**Defer spec wiring that would reframe an operator-adopted decision.** When a freshly-decided brief implies a change to a decision the operator has already adopted, do not silently propagate the change into specs — record the decision, flag the reframing as an explicit operator morning-review item, and defer the spec wiring until the operator re-adopts. A downstream brief acting alone does not relitigate an adopted decision.

*Grounded in: auto-001's rubric reframes operator-adopted D-20 as conditional-on-prevention; the C43/C34/C42/C56/C57 wiring was deferred pending operator re-adoption rather than applied.*

# justification

The auto-001 decision brief concluded that the "fence" (adopted by the operator as D-20, *unconditionally*, as a Phase-2 precondition) should be reframed as *conditional on the substrate actually preventing*. That is a sound engineering conclusion — but D-20 was an operator-adopted decision, and the project rule is that adopted decisions are not relitigated. Silently writing the conditional framing into C43/C34/C42/C56/C57 would have erased the operator's explicit sign-off and buried a security risk-tolerance change inside a spec diff where it is easy to miss. Instead the decision was recorded in the brief, the reframing was surfaced as an explicit morning-review item ("re-adopt D-20 as conditional?"), and the spec wiring was deferred until the operator answers. The cost of deferring is one summary bullet and one HANDOFF line; the cost of silently applying it is the loss of the operator's editorial authority over a safety decision.
