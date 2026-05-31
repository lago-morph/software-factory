# agent instruction

**Decision-robustness claims require re-reading the artifacts.** "Before telling the user a set of decisions is 'robust under a refined bar/criterion', re-read the artifacts each decision touches. Pattern-matching from your earlier scoring is not sufficient — the artifact's specific text can flip the decision when the bar is interpreted concretely. Over-claiming robustness then walking it back during apply erodes trust more than calibrated uncertainty does."

*Grounded in: PR #218, where I told the operator "no decisions change under the refined bar" based on the SURVIVOR-PASS table, then had to publicly walk back 4 of those decisions when I opened the C08/C09 specs to actually apply.*

# justification

When the operator refined the bar mid-session from "no satisfaction without it" to "adds capability tied to a specific principle, partial satisfaction by upstream stack counts," I checked my prior scoring against the refined bar by pattern-matching on the ledger summary and reported: "no decisions change under the refined bar." That statement was wrong. The pattern-match worked for 21 of the 25 keeps, but C08-01/02 and C09-01 (the "spec is a standalone bundle referenced by the prompt template" cluster) had a subtle property pattern-matching missed: applying them would reverse faithful's deliberate `[AMBIGUITY: OQ-1]` resolution. Under the original bar, "would this delta add capability the canonical lacks?" — yes, structurally. Under the refined bar, "would it add capability for a specific 12-principle?" — no, it just *re-organizes* the same P1 capability differently. The bar interpretation flipped at the artifact level, not at the table-row level.

I caught this only during the apply phase when I opened C08 to actually edit it. At that point the operator had already been told "no decisions change" — so I had to issue a public correction ("the C08/C09 cluster reclassifies on close read"). That correction was costlier than calibrated uncertainty would have been. Saying "I think the decisions hold but I'll verify each by re-reading during apply" loses nothing; saying "no decisions change" claims a precision the pattern-matching couldn't deliver.

The fix is a categorical bar on what claims can be made before re-reading. Before re-reading: "the ledger summary shows the bar-shift doesn't obviously flip any verdict; I'll verify during apply." After re-reading: "verified, all decisions hold" or "reclassified N, here they are." The intermediate form ("decisions are robust") implies a precision that pattern-matching from a summary cannot honestly deliver.

The cost of the discipline is one bullet of language hedging at the moment robustness is claimed. The cost of skipping the discipline is the trust hit when the apply phase forces a public correction. Asymmetric in the discipline's favor.
