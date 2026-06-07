# ADR: Runtime state lives in a named Docker volume, not a host bind mount

- **ID**: ADR-a4932dad26
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-07
- **Source retrospective**: ../2026-06-07-7.md
- **PRs covered**: #2, #3, #4, #5, #6, #7

## Context

The operator running the dockerized Gas City prototype on a Windows laptop (Docker Desktop) reported that the bead store was "extremely slow." The shipped `docker-compose.yml` stored the prototype's runtime state — the Dolt bead-store database and the rigs — on a host bind mount (`./workspace`). On Docker Desktop's translated host filesystem (drvfs/9p on the WSL2 VM), Dolt's many small reads/writes and its file locking crawl: the workload is exactly the pathological case for a translated bind mount. The slowness was not visible during development because verification had used a different storage configuration (a named volume) — see ADR on verifying the shipped config and the related skill spec.

## Decision

Store the prototype's runtime state (the Dolt bead-store database and the rigs) in a named Docker volume rather than a host bind mount, because Docker Desktop's host-mount filesystem is unusably slow for Dolt's many small reads/writes and file locking.

## Alternatives considered

- **Host bind mount (`./workspace`) for easy host-side browsing** — rejected on performance: the translated filesystem on Docker Desktop made Dolt unusably slow; the convenience of browsing files from the host does not justify a prototype that is too slow to use.
- **tmpfs / in-memory volume** — rejected on durability: runtime state (beads, commits, rig history) must survive container restarts; tmpfs loses everything on stop.

## Consequences

- The prototype is fast and correct on Docker Desktop (Windows/macOS) as well as native Linux.
- The host can no longer browse the state files directly through the filesystem; to inspect or extract state, use `docker compose exec` or `docker cp` into the named volume.
- A full reset is `docker compose down -v` (the `-v` removes the named volume); operators must know that `down` without `-v` preserves state and `down -v` wipes it.
- Two companion hardening changes shipped alongside this in PR #2 (later partially revised): pinning `DOLT_VERSION`, and an initial `GC_BEADS_FORCE_FALLBACK=1` that was subsequently dropped in PR #3 because it forced every snapshot read through a `bd` subprocess and blew gc's 3s budget.

## References

- [`../2026-06-07-7.md`](../2026-06-07-7.md) — the source retrospective.
- [`./SKILL-SPEC-02811cf740-verify-the-shipped-config-not-a-proxy.md`](./SKILL-SPEC-02811cf740-verify-the-shipped-config-not-a-proxy.md) — why the proxy verification hid this.
- PRs the decision was made in: #2, #3.
