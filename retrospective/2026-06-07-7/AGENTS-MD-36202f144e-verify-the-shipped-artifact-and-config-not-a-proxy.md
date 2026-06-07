# agent instruction

**Verify the shipped artifact and config, not a proxy.** Verify a packaged deliverable by running the exact shipped artifact and configuration — the real compose file, entrypoint, and volume/network settings — on a target-equivalent platform, not a hand-rolled approximation that is easier to run.

*Grounded in: verifying with `docker run` + a named volume while shipping `docker-compose` + a bind mount hid a Windows-only performance failure.*

# justification

The session's hardest-to-find bug was the Windows slowness: development verification used `docker run` with a named volume (fast), while the shipped `docker-compose.yml` used a host bind mount (`./workspace`) that crawled on Docker Desktop's translated filesystem. The proxy verification passed precisely because it had swapped out the one property — the volume type — where the bug lived. The cost of not having this rule is shipping a deliverable that fails on the operator's actual machine while every internal check is green, then burning a full debugging cycle (and the operator's goodwill) chasing a failure you can't reproduce because you never ran the shipped config. The marginal cost is trivial: boot the real compose file via the real invocation on the closest-available target platform instead of a convenience command. A verification that diverges from the shipped path can only ever certify the path nobody ships.
