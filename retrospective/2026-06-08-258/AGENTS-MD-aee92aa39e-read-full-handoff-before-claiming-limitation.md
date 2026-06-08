# agent instruction

**Read the full handoff/environment doc before claiming an environment limitation.** Before reporting that a capability is unavailable (no Docker, no token, no network, "can't verify here"), read the repo's complete handoff / environment / getting-started doc end to end — not just its head — and probe directly (e.g. `which dockerd`, `docker info`). State a limitation only after both the doc and a live probe confirm it.

*Grounded in: claiming "no Docker host / no token" when the daemon merely needed `sudo dockerd` and a token plus a full build recipe were documented in HANDOFF.md §3, which had only been skimmed.*

# justification

This session twice asserted an environment limitation that was false: first "no Docker host," then "no subscription token," and on the strength of those it shipped two PRs' worth of changes labeled "unverified." Both claims were wrong — Docker was present (the daemon simply was not started) and a real token plus a complete CA-injection build recipe were sitting in `docs/HANDOFF.md` §3. The cost was concrete: false "unverified" notes propagated into two merged-bound PRs and required a follow-up correction pass once the operator pushed back ("how did the prototype do all that testing if it didn't have access to docker?"). The marginal cost of the rule is one full read of a doc the agent was already partially reading, plus a one-line probe (`docker info`). That asymmetry — minutes of reading versus shipping unverified work and eroding trust — makes the rule strongly net-positive, and it generalizes beyond Docker to any "I can't do X here" claim.
