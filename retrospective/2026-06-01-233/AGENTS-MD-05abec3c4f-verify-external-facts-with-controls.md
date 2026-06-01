# agent instruction

**Verify load-bearing external facts with your own tool calls and controls.** When a fact the run depends on is asserted by a subagent or a web search — whether a repo/binary/tool exists, or how an API behaves — confirm it yourself with at least two independent signals and a control case before acting on it. Treat a subagent's research narrative as a lead, not a fact; a blanket transport error (e.g. a proxy returning 403 for every path, including known-good controls) tells you nothing about the underlying truth.

*Grounded in: a subagent reported Gas City as "v1.2.0 / brew install" (confabulated specifics) while the repo's existence was real; direct GitHub-API/HTML/search probes with control repos distinguished a proxy-403 artifact from real existence.*

# justification

The run's single highest-leverage unknown (does `gc` exist — gap G11) was nearly answered wrong by a subagent that returned a confident narrative with a fabricated version number and install command. The general claim (the repo exists) happened to be true, but the specifics were invented — confidence and confabulation co-occur. The cost of verifying was three `curl` calls plus a control repo: the control (`torvalds/linux` returning the *same* 403 on the API `/repos/` path) is what converted an ambiguous signal into a definite "this 403 is a proxy artifact, not a 404," after which the HTML host and search endpoints gave an unambiguous CONFIRMED. Building a whole sweep on an unverified premise, or concluding "doesn't exist" from a transport artifact, are both far more expensive than the seconds the control-based check costs.
