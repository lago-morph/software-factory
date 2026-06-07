# agent instruction

**git-init a scope that a tool resolves context from via its git root.** If a tool (e.g. `bd`) resolves a working scope by walking up to a git repository root, ensure that scope directory is actually a git repo; a non-git scope fails the tool's context/preflight check even when the underlying data layer is healthy.

*Grounded in: `/workspace/city` not being a git repo broke `bd context` and produced native_store_unavailable.*

# justification

gc's `bd_context_agreement` preflight kept emitting `native_store_unavailable` and falling back — on Linux as well as Windows, so it was not a platform or version issue. Live-booting the real stack and running the failing preflight showed the cause: `bd context` resolves a scope via its git repo root, and `/workspace/city` was not a git repo, so the preflight failed even though the data plane was perfectly healthy. This is a deceptive failure: the data layer works, the error message points at the store, and the real cause is a missing `.git`. The cost of not having this rule is a degraded-mode system (fallback path, warnings, the 3s-subprocess tax) that looks like a store problem and sends you debugging the wrong layer. The marginal cost is a one-line `git init` in the entrypoint for any directory a context-resolving tool will look at. When a tool finds its scope by walking to a git root, the absence of that root is a silent preflight failure waiting to happen.
