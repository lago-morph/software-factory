# agent instruction

**Self-check rubric requires tool-verification for measurable items.** Self-check rubrics that include measurable items (word count, file existence, link relativity) MUST require the subagent to run an actual tool call (`wc -w`, `ls`, `grep`) verifying the item, not just self-attest. Bare self-attestation drifts.

*Grounded in: Wave 4.1 — the BF-L subagent returned 1676 words against an 800-1500 budget while claiming self-check passed.*

# justification

Self-check rubrics that ask the subagent to confirm measurable properties (word count within X-Y, all sections present, all links relative) are nearly useless when the verification is by self-attestation. The Wave 4.1 BF-L subagent returned 1676 words against an 800-1500 budget and self-attested "Word count between 800 and 1500: ✓". The subagent had not actually counted; it had pattern-matched on the rubric item and emitted a checkmark. Without tool verification, the rubric becomes ritual. With tool verification (`wc -w <file>` returning a number that the subagent then compares to the budget), the rubric is a contract. The cost of adding `wc -w` to a rubric is one bullet; the cost of overshoot going undetected is downstream readers facing 100% larger files than expected and aggregator passes being more expensive than budgeted.
