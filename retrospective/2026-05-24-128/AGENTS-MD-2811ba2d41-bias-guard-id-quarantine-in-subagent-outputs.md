# agent instruction

**Bias-guard ID quarantine.** Subagent outputs cite the underlying corpus material referenced inside bias-guard findings (specific reports, sections, primary sources) — never the bias-guard finding ID itself (`MISSED-N`, `WEAK-N`, `CANDIDATE-N`). Bias-guard sharpenings and audits are critic framings, not corpus references. Citing a finding ID lends a critic's framing the weight of a primary source and turns the lead-agent's prior integration into a downstream anchor.

*Grounded in: five parallel subagents cited the same bias-guard sharpening ID in their outputs, treating an auditor's framing as a stable corpus claim.*

# justification

The Phase-2 anchor-detector audit identified one bias-guard sharpening (a critic's three-position framing for an existing failure mode) as the single most contamination-suspect finding in the run: five of the nine Phase-2 tracks cited the sharpening by its `WEAK-N` ID, treating it as a corpus reference. Bias-guard findings are by design partial, contested, and lead-agent-curated; treating them as primary sources collapses the distinction between "the corpus says X" and "an auditor proposed X." The fix is mechanical: when a downstream subagent wants to cite the substance of a bias-guard finding, it cites the underlying source (the report, the section, the original quote), not the finding's ID. Marginal cost: one extra grep when writing a subagent brief. Cost of not having the rule: an entire Phase-2 dispatch had to be re-run because the citation pattern was structural in the contamination.
