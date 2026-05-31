# agent instruction

**Subagents persist to disk and return short receipts.** "Brief every authoring subagent to write its deliverable to a file and return only a <=15-line receipt (paths written, headline findings, open questions). The orchestrator must never read large source docs or full subagent output into its own context."

*Grounded in: sustaining ~15 build/review waves without exhausting the primary context window.*

# justification

This session decomposed a 1500+ line architecture into 57 components and ran scores of builder/adversary/integrator subagents. If the orchestrator had read the source docs or the full output of each subagent, its context would have been exhausted within the first two batches. Instead, every subagent wrote its spec/plan/review to a distinct path and returned a tight receipt; the orchestrator only ever held the compact component inventory plus a stream of short receipts. The cost of the rule is one extra sentence in each brief ("write to disk, return a <=15-line receipt"). The payoff is that the primary can orchestrate an arbitrarily large body of work whose total size dwarfs any single context window — the filesystem, not the context, becomes the working set.
