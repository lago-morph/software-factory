# agent instruction

**Follow the literal interpretation when the user clarifies a naming pattern.** "When the user clarifies a filename, identifier, or convention using literal text (quoted tokens, specific spelling, exact ordering), implement the literal interpretation. Don't 'translate' to what they probably meant. If the literal reading looks inconsistent with surrounding conventions, surface the ambiguity via `AskUserQuestion` before guessing — but once they answer, use their answer verbatim."

*Grounded in: PR #95 where the user's literal "AGENT-hash-name" and later "AGENTS-MD-" prefixes were each applied verbatim.*

# justification

Twice in PR #95 the user's literal naming instruction looked inconsistent with the existing convention. First: they wrote `AGENT-hash-name` (singular AGENT, hash-then-name order) while the existing skill specs and ADRs used `<name>-TYPE-<hash>.md` (name-first). I asked via `AskUserQuestion` and learned they wanted ALL THREE types switched to `TYPE-<hash>-<name>.md` — the literal hash-then-name order applied uniformly. Second: they wrote "I changed my mind about the name of the agents files. Instead on AGENT- I want to start with AGENTS-MD-." I applied AGENTS-MD- verbatim, including in the ID (`AGENTS-MD-<hash>`).

If I had translated "AGENT" to AGENTS for consistency on the first round (instead of asking), I would have produced an inconsistent half-convention. If I had questioned "but you said AGENT-, why AGENTS-MD- now?" on the second round, I would have looked obtuse. The pattern is: surface ambiguity once via `AskUserQuestion` if there's room for interpretation, then take the answer literally — even (especially) when it overrides what I think they probably meant.

Cost: one extra `AskUserQuestion` round-trip on genuinely ambiguous naming clarifications. Benefit: avoid two failure modes — silent translation that does the wrong thing, and re-litigating an answered question.
