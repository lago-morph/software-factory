# agent instruction

**Boot images tokenless to verify without spending subscription.** To validate a container's full boot/wiring without spending API/subscription tokens, start it with no auth token so agent processes fail auth harmlessly while servers and schemas still initialize, then assert on the wiring rather than on agent output.

*Grounded in: verified the city boot + bead store with no CLAUDE_CODE_OAUTH_TOKEN.*

# justification

Verifying a Gas City image end-to-end means booting the whole stack — rendering city.toml, provisioning rigs, bridging the bead store, starting `gc`, and launching agents. But running real agents spends the user's Claude Max subscription tokens on every verification pass, and this session needed roughly six rebuild-and-boot cycles to converge. By leaving the agents tokenless (no `CLAUDE_CODE_OAUTH_TOKEN`), the agent processes fail authentication harmlessly and immediately, while every layer that matters for wiring verification — the managed Dolt server starting, the socat bridge binding the host/port, the bead-store schema initializing, the provider catalog resolving — still executes fully. This caught real bugs (the dolt `--user`/`--password` removal, the missing `[providers.claude]` catalog entry) that surface during boot, before any token would ever be spent. The marginal cost is zero — simply omitting an env var — and the payoff is unlimited verification passes at no token cost, with assertions placed on the wiring (process up, port open, schema present) instead of on agent replies that would require spend to produce.
