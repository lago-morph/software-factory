# agent instruction

**Record risk-tolerance cross-component calls as provisional rulings plus morning-review.** When a cross-component decision turns on operator risk-tolerance (e.g. a security or sequencing trade-off) rather than something derivable from the corpus or prior decisions, record it as a PROVISIONAL ledger ruling carrying the recommended resolution AND surface it as an explicit morning-review item for operator confirmation -- neither silently settling it nor freezing the run.

*Grounded in: the v4 run's D-18 provisional C43 isolation pull-forward.*

# justification

Most cross-component conflicts are resolvable from the spec corpus, the standing bar, or earlier decisions, and an autonomous run should just rule them and move on. But a few are genuinely the operator's call because they trade off risk the agent has no mandate to price — here, whether the factory may scale unattended and self-modify (phases P2/P3b) before its lethal-trifecta blast-radius bound (C43) lands, accepting an exposure window. Freezing the run to ask would violate the unattended mandate; silently choosing would usurp a risk decision. The provisional-ruling pattern does both right: it records the well-reasoned recommended split (D-18) so downstream work isn't blocked, while flagging it as the #1 morning-review item with an isolated, revertible commit so the operator can confirm or override in one read. The cost is one ledger entry plus one summary bullet; the asymmetry is that an un-surfaced security trade-off is the kind of thing that should never be discovered after the fact.
