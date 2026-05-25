# agent instruction

**Exemplar before parallel uniform-schema fanout.** Before dispatching ≥3 parallel subagents producing a uniform-schema deliverable, the lead agent MUST author one exemplar of the deliverable and ship it with the dispatch brief as input. Subagents read the exemplar as the format model. Choose an exemplar candidate that is least-contested (no RG flags, no contested-primitive references, no shared-skeleton obligations) so the exemplar demonstrates the schema cleanly.

*Grounded in: Wave 4.1 — the GF-M substrate-requirements summary was authored as the exemplar; the 9 Wave-4.1 subagents consumed it as the format model; aggregation at Wave 4.2 was tractable because all 10 summaries shared the format.*

# justification

A uniform-schema fanout's "simpler aggregation" claim relies on the N output files actually conforming to the schema. Without an exemplar, subagents drift: section orderings shuffle; required text-pulls become paraphrases; fixed sub-section headers become free-form prose; word counts vary 2× across the fanout. The lead agent then pays the drift cost at aggregation — re-reading each output to extract the conformant fragment, or re-shaping outputs that didn't conform. An exemplar authored before dispatch shifts that cost from N × aggregation-pass to 1 × authoring-pass. In Wave 4.1, the GF-M exemplar took ~10 minutes to write and made the 9-subagent fanout's outputs aggregator-ready; Wave 4.2 rendered 8 same-vs-distinct verdicts in one lead-agent pass because all 10 §3 sections used the same fixed sub-section headers. The marginal cost is one exemplar per fanout; the saved cost is per-output aggregation overhead × N.
