# agent instruction

**Flag unverified external-format examples as illustrative.** When documenting the syntax or behavior of an external substrate that has not been run/verified, present every example as explicitly illustrative ("shape, not verified syntax") and never assert a format detail, a borrowed example's field, or an unbuilt safety property as present fact; cite the source spec's own hedge.

*Grounded in: the methodology companion asserting a same-family Phase-0 judge as a "different model family" and inventing $slot/loop formula keys.*

# justification

The methodology companion presented an illustrative Gas City formula whose exact TOML syntax is, per the source spec, unverified (the conformance check has never run). A dedicated fact-check subagent caught three over-claims: a code comment stated the judge was a "different model family" as flat fact when the spec relaxes cross-family to advisory at that phase (an unbuilt safety property asserted as present), and the `$slot` parameter style and `[loop]` keys were borrowed/invented but not flagged as such. Each is the kind of error that propagates silently — a future reader takes the illustration for verified fact and builds on sand. The marginal cost of the rule is a one-line "illustrative shape, unverified" banner plus a citation to the spec's own hedge; the cost of omitting it is a fabricated-as-real detail that no reader can distinguish from a true one until something breaks against the real substrate.
