# agent instruction

**No invented limitations.** "When evaluating an OSS dependency or architectural option against a defined principle set, do not introduce limitations or 'gaps' that aren't grounded in the agreed principle set. Stay scoped to what the agreed evaluation criteria actually require; do not drag in nice-to-have capabilities (counterfactual branching, runtime sliders) and frame them as deficiencies."

*Grounded in: claiming BLAKE3-CAS counterfactual branching was a 'Gas City gap' when it isn't in the 12 principles; the user called this out as scope creep.*

# justification

Inventing limitations introduces decision noise — the user has to spend cognitive cycles separating real constraints from invented ones. In the BLAKE3-CAS case, I dragged a CXDB-vs-Gas-City difference into the evaluation when the 12 principles never required it; the user correctly identified this as scope creep with the line "Is that one of the 12 principles? If not why mention it?" The marginal cost of staying scoped is essentially zero (one check: "is this in the agreed criteria?"); the cost of invented limitations is conversation overhead and risk of bad decisions made on false constraints. The same failure mode showed up with the "context fidelity slider" suggestion that the user noted prompt manipulation already handles.
