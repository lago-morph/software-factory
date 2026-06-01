# agent instruction

**Recompute counts after membership changes; never trust a carried-over total.** "When the membership of a counted set changes during editing — even a one-in-one-out swap that 'should' leave the total unchanged — recompute the count programmatically and grep every stated instance of it in the document before committing. Stated totals drift silently across edits."

*Grounded in: swapping C44 out for C31 kept the backbone at 25, but the draft asserted 26 in eight places until a scripted recount caught it.*

# justification

The backbone draft was written with a 25-component count, then an adversarial finding swapped C44 out and C31 in — a net-zero membership change that should have left the total at 25. But an earlier arithmetic slip had already seeded "26" into eight places (the headline, two ring labels, the cluster caption, the summary line). Because the swap "obviously" didn't change the count, the instinct was to leave the numbers alone — exactly the wrong move, since the numbers were already wrong. A three-line Python recount of the cluster union plus a grep for the stray "26" found and fixed all eight in one pass. The marginal cost is one script run per membership change; the cost of skipping it is a document that contradicts itself on its own central figure, which a careful reader will catch and an agent will have to explain. Counts in a long doc are the single most drift-prone fact; mechanize their verification rather than eyeballing.
