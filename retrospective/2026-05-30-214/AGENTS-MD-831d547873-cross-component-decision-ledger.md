# agent instruction

**Drive cross-component rulings through a decision ledger.** "When parallel subagents surface conflicting cross-component decisions, record each resolution as a numbered adopted decision in a shared ledger file, then pass the decision id into later subagent briefs so the ruling propagates without re-litigation."

*Grounded in: decisions D-1..D-5 reconciling four-way namespace and ownership conflicts across foundational specs.*

# justification

Independent builder subagents produced four different identity namespaces and two different "who owns the bead schema" answers across foundational specs — exactly the drift you get when many agents work in parallel without a shared source of truth. Capturing each resolution as a numbered, adopted decision (D-1…D-5) in a `review-log.md`, then feeding the decision id into subsequent briefs, made later subagents self-align: components built *after* a ruling reproduced it unprompted (e.g. a builder independently adopted the D-2 namespace and the D-4 dependency direction). A single integrator pass then applied each ruling across the already-built specs. The marginal cost is a few lines per decision in one file; the payoff is that a 57-component, two-track corpus stays internally consistent despite being authored by dozens of agents that never see each other's context.
