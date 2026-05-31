# agent instruction

**Spot-check subagent-authored definitions against the corpus source of truth.** Before shipping a subagent-authored human-facing artifact, verify each load-bearing definition in it against the spec or corpus it describes; subagents confidently invent plausible-but-wrong meanings, and a fluent wrong definition is harder to catch than a clumsy one.

*Grounded in: a refresh subagent in this session describing the "digital twins" as "two copies of the factory that check each other's work," when the corpus (C44) defines twins as behavioral fakes of external services.*

# justification

A subagent refreshing the plain-language build-order guide rewrote the definition of "the twins" as two factory copies cross-checking each other — a coherent, confident, completely fabricated meaning. The actual corpus (the C44 "Digital Twin (per service)" spec, and the user-facing decisions doc) defines twins as LocalStack/VCR-style behavioral fakes of external services that the factory rehearses against before touching production. The fabrication survived into a committed, user-facing guide and was only caught on a deliberate end-to-end read against ground truth. A wrong definition in an outsider-facing explainer is high-blast-radius: the entire point of the guide is to be trusted by a reader who can't check it themselves. The marginal cost of the rule is one grep of the relevant spec per load-bearing term (here, `grep -i twin spec/C44-*.md`); the cost of skipping it was a fabricated definition shipped to the reader most dependent on it being right.
