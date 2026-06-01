# agent instruction

**Functional closure beyond the dependency edge-list.** "When computing a build order or minimal backbone from a dependency table, do not stop at the transitive closure of the edge column — walk the actual runtime story of the target capability and add the components that are functionally required to *run* it but that no edge names. Present the result as explicit rings (strict-closure / runnable / safe) so the gap between the graph and reality is visible, not hidden."

*Grounded in: the v4 self-build backbone, where the inventory's Depends-on closure omitted the scenario runner C31 and the entire run-flow (C05/C09/C18).*

# justification

The component inventory's "Depends on" column records what each component's *spec* references, not what it takes to *run* the capability. Computing the strict transitive closure of `{C53, C43}` produced a 19-component set that looked complete but could not actually execute a build: it had the spec format and the bootstrap gate but no dispatch (C05), no prompt binding (C09), and — caught only by an adversarial subagent — no scenario *runner* (C31) to execute the held-out scenario that feeds the judge. A reader who trusted the edge-closure would have planned a backbone that cannot reach its own milestone. The marginal cost of the rule is one pass of "narrate the runtime story and diff against the closure"; the cost of skipping it is a build plan that is silently short its load-bearing executor, discovered only when someone tries to run it. Presenting the result as rings (19 strict → 22 runnable → 25 safe) makes the otherwise-invisible gap between the dependency graph and operational reality an explicit, reviewable line item.
