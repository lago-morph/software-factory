# agent instruction

**Lead-verify a subagent's contradiction verdict before applying it.** When a subagent reports that a finding CONTRADICTS the corpus, grep the actual spec/doc text the contradiction names before annotating anything — a fact being true of the substrate does not contradict a document that never made the opposing claim. Reclassify to NEW-INFO when no opposing claim exists.

*Grounded in: a harvest subagent flagged 3 CONTRADICTS-CLAIM facts; grepping the actual specs showed 0 true contradictions (the specs had deferred the field names to later verification or never referenced them).*

# justification

A subagent harvesting facts from an external prototype flagged three substrate facts as contradicting the v4 corpus. Applying those verdicts would have written three "v4 is wrong" annotations into canonical specs and triggered needless rework — when in fact the corpus had correctly *deferred* the relevant field names to later verification (one case) or never referenced the thing at all (two cases). Grepping the actual spec text took three commands and turned "3 contradictions" into "0 true contradictions; all NEW-INFO," which became a positive headline (the corpus's deferral discipline held up) rather than a false alarm. Subagents systematically over-flag contradictions because they reason forward from the new fact rather than backward from what the document actually claims; the lead is the only one positioned to check the claim side.
