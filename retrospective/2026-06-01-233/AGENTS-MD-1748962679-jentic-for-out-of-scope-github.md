# agent instruction

**Use jentic for GitHub operations outside the session-scoped repo.** The GitHub MCP is hard-scoped to the session's repository; calls to any other repo are denied. To read PRs/issues/contents of a different repository, use the jentic execute tool against the github.com API (search the operation, load its schema, execute) or git clone for file content — do not assume the GitHub MCP can reach it.

*Grounded in: reading lago-morph/gascity-prototype PR descriptions required jentic pulls/list because the GitHub MCP rejected the out-of-scope repo.*

# justification

Mid-task, the operator asked for the PR descriptions of a *different* repository than the session's scoped one. The GitHub MCP returned a hard "Access denied: repository not configured for this session," and there was no `add_repo`/`list_repos` tool available in the session. Without knowing the fallback, an agent wastes a round-trip and risks reporting the capability as unavailable. The jentic API gateway can call the public `github.com` API (`pulls/list`, `pulls/get`, etc.) against any public repo via its search→load→execute flow, and plain `git clone` retrieves file content. Naming jentic explicitly as the out-of-scope GitHub path turns a dead end into a one-step move.
