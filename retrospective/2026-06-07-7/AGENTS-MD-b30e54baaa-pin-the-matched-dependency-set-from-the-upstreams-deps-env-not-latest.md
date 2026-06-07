# agent instruction

**Pin the matched dependency set from the upstream's deps.env, not latest.** When building an image around an upstream tool that publishes a pinned dependency manifest (e.g. gascity's `deps.env`), pin your image to that matched set — the tool plus its companion binaries — at a release tag, not `main`/`latest`, to stay reproducible and avoid version skew.

*Grounded in: floating on gascity `main` stamped gc 1.1.1, and `dolt latest` had once removed a flag the image relied on.*

# justification

The Dockerfile built `gc` from `main`, so the shipped image stamped `gc 1.1.1` when the intended, gascity-matched version was `v1.2.1`. Floating pins make the image non-reproducible and expose it to version skew between gc and its companions — and that skew is not theoretical: `dolt latest` had previously removed the `sql-server --user` flag the stack depended on. gascity publishes a `deps.env` per release naming the matched gc/bd/dolt set known to work together. The cost of not pinning to it is an image that builds differently every time and can break overnight when any upstream component cuts a release; the failure surfaces far from its cause and is hard to bisect. The marginal cost is reading one upstream manifest and pinning to a release tag. Reproducibility and a coherent matched set are worth one deliberate version bump per upgrade over invisible drift.
