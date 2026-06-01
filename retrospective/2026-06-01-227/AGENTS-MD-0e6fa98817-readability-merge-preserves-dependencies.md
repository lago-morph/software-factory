# agent instruction

**A readability merge must preserve the dependency source-of-truth grouping.** Before collapsing two items into one unit to make a document read more cleanly, check the dependency source of truth: if the items have different upstream dependencies, merging them misrepresents the graph and contradicts any section that lists them separately. Keep them separate even if it costs one more box or row.

*Grounded in: folding the bead-type schema (C20, which depends on C19) into the spec-intake product to claim 'six products' contradicted the catalog and was reverted to seven.*

# justification

Mid-restructure, "seven products" felt like one too many for a clean backbone diagram, so the bead-type schema (C20) got folded into the spec-intake product to round the count down to six. It read better — and it was wrong. C20 depends on the bead store (C19), not on the spec artifact (C08/C09); the products catalog already (correctly) listed it as its own product with its own dependency. The merge created a genuine self-contradiction: the same component was modeled two incompatible ways in the same document, with two different upstream dependencies. The skeptical-architect reviewer caught it and it cost a full second-round fix to unwind — separating the node again, splitting the table row, re-deriving the count back to seven, and re-checking the ring math. The marginal cost of the rule is one dependency lookup before merging two items for presentation. The cost of ignoring it is a contradiction that a knowledgeable reader trips on immediately and that erodes trust in every other count in the document. Presentation convenience never outranks the dependency graph.
