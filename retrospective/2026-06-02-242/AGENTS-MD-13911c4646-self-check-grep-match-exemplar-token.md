# agent instruction

**Self-check grep tokens must match the exemplar's actual spelling.** "When a subagent self-verifies a deliverable with a grep (per the tool-verification self-check rule), the grep pattern MUST match the exemplar's literal token, not a plausible guess — publish the exact token in the dispatch brief so every subagent greps the same string. Before shipping a self-check rubric, grep the exemplar once to confirm the token actually appears."

*Grounded in: four Sweep-2 builders hit a `R/W-by` vs `R/W by` mismatch, each reporting the grep returned 0 and adding a caveat that the column was present anyway.*

# justification

The self-check rubric told builders to `grep -c "R/W-by"`, but the format exemplar's ownership column is spelled `R/W by` (a space, no hyphen). Four builders dutifully ran the grep, got `0`, and each had to hand-explain in its receipt that the column existed despite the rubric's own pattern missing it — pure noise that erodes the self-check's credibility and, worse, could mask a genuine absence behind "the pattern is just wrong again." A tool-verified self-check is only as trustworthy as the token it greps for; confirming that token against the exemplar once, up front, costs one grep and removes a recurring false signal from every downstream receipt.
