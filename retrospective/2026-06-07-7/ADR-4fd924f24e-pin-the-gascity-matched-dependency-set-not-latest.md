# ADR: Pin the gascity-matched dependency set, not latest

- **ID**: ADR-4fd924f24e
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-07
- **Source retrospective**: ../2026-06-07-7.md
- **PRs covered**: #2, #3, #4, #5, #6, #7

## Context

The prototype's `Dockerfile` built `gc` from `main` rather than from a pinned release. As a result the shipped image stamped `gc 1.1.1` even though the intended, gascity-matched version was `v1.2.1`. Floating on `main` means the image is not reproducible and is exposed to version skew between `gc` and its companion binaries (`bd`, `dolt`). That class of breakage is not hypothetical: `dolt latest` had at one point removed the `sql-server --user` flag the stack relied on. gascity publishes a `deps.env` per release that declares the matched set of versions known to work together; building against that manifest is what keeps the image coherent.

## Decision

Pin gc, bd, and dolt to the matched versions declared in the chosen gascity release's deps.env (gc v1.2.1 / bd 1.0.4 / dolt 2.1.0) rather than building from main or `releases/latest`, so the image is reproducible and avoids version-skew breakage.

## Alternatives considered

- **Build from `main` / `releases/latest`** — rejected: not reproducible, and exposes the image to upstream breaking changes landing between builds (the `dolt sql-server --user` removal is a concrete example).
- **Vendor the binaries into the repo** — rejected as overkill for a prototype: it bloats the repo and creates its own update/maintenance burden; pinning to a published release tag achieves reproducibility without vendoring.

## Consequences

- The image is reproducible: a rebuild yields the same matched gc/bd/dolt set.
- Version skew between gc and its companion binaries is eliminated, because the set comes from one upstream-blessed manifest.
- Upgrading requires a deliberate bump of the pinned release tag (and re-running the verification), rather than silently drifting — this is the intended trade-off: explicit, verified upgrades over invisible drift.
- The verification step must read the versions stamped inside the built image, not assume the intended versions (the float to 1.1.1 was invisible without that check).

## References

- [`../2026-06-07-7.md`](../2026-06-07-7.md) — the source retrospective.
- [`./SKILL-SPEC-02811cf740-verify-the-shipped-config-not-a-proxy.md`](./SKILL-SPEC-02811cf740-verify-the-shipped-config-not-a-proxy.md) — verify the stamped versions in the shipped image.
- PRs the decision was made in: #4.
