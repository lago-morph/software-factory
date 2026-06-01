# agent instruction

**Verify a subagent's structure-changing claim against its cited source.** "Before integrating a subagent finding that changes a deliverable's structure — adds or removes a node in a graph, flips a binding decision, swaps membership — open the primary source it cites and confirm it, rather than trusting the subagent's summary. Do this even when the subagent is one you dispatched and trust."

*Grounded in: an adversarial reviewer's claims that C31 was required and that decision D-20 splits C43 (deferring C44) — both materially changed the backbone and both were verified against spec/C53 and panel/VERDICT.md before acting.*

# justification

Two adversarial subagents returned claims that each changed the backbone's membership: that the scenario runner C31 was silently required, and that operator decision D-20 splits the isolation fence C43 so its twin half (C44) defers. Both were correct — but acting on a wrong structural claim would have shipped a wrong graph into a doc the next planning run treats as the spine. Opening the cited sources (`spec/C53-bootstrap-validation.md` AC-9 and `panel/VERDICT.md` line 14) cost two file reads and converted "a subagent said so" into "the source says so, quoted." Subagent summaries compress and occasionally over-claim; a structural change to a deliverable is exactly the place where that compression is most expensive to get wrong. The asymmetry is stark: one verification read per structure-changing claim, versus a corrupted dependency graph propagating into every downstream plan that cites it.
