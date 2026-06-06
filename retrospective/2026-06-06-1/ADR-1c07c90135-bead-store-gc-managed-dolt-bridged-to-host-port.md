# ADR: Bead store for the Gas City prototype is a gc-managed Dolt server bridged to a host/port

- **ID**: ADR-1c07c90135
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-06
- **Source retrospective**: ../2026-06-06-1.md
- **PRs covered**: #1

## Context

The prototype must run the bundled gastown pack, which makes roughly 368 `gc bd` calls. `gc bd` is gated to bd-contract providers, so the gc-native `file` provider — the user's first directive — cannot run the proven gastown fleet. The user then clarified they wanted a local **server** reachable by the whole compose group via host/port, backed by a non-synced local data file ("socket" turned out to mean a TCP host/port). A dedicated external Dolt service was attempted but hit a gc external-endpoint bootstrap circularity: `use-external` needs scope metadata that only scope-init creates, and there is no `gc init` external flag. Separately, gc's managed Dolt binds loopback on a hashed port and rejects host `0.0.0.0`, and pinning `[dolt].port` to force a stable port breaks gc 1.1.1's managed lifecycle. These constraints, surfaced during investigation and in-sandbox verification, made the bead-store transport a binding architectural decision rather than a config tweak.

## Decision

Run the prototype's bead store as a gc-managed Dolt SQL server and republish it to a compose-reachable host/port with a socat bridge, rather than using the gc-native file provider or a dedicated external Dolt service. The user selected this option via AskUserQuestion over the dedicated-service alternative. gc owns the Dolt lifecycle and scope/metadata init; a socat bridge republishes the loopback-bound managed port to `0.0.0.0:3307` for the compose group; cross-container root uses `DOLT_ROOT_HOST=%`.

## Alternatives considered

- **gc-native file provider** — rejected: it disables `gc bd`, and the gastown pack's ~368 `gc bd` calls cannot run against it.
- **Dedicated external Dolt / dolt-sql-server service** — rejected: gc's external-endpoint bootstrap is circular (`use-external` needs scope metadata that only scope-init creates, and there is no `gc init` external flag), so the external service cannot be bootstrapped cleanly.
- **Embedded bd** — rejected: it is not a shared server reachable by the whole compose group over host/port, which the user explicitly required.

## Consequences

The bead store's lifecycle is tied to the city container (gc manages Dolt), which is robust because gc owns scope and metadata initialization — sidestepping the external-bootstrap circularity entirely. The socat bridge is a small extra moving part to operate and monitor. Because the port is republished rather than pinned, gc's managed lifecycle stays intact across restarts. The store remains a bd-contract provider, so the gastown fleet runs unmodified.

## References

- [`../2026-06-06-1.md`](../2026-06-06-1.md) — the source retrospective.
- [`./SKILL-SPEC-f62885124d-dockerize-gas-city.md`](./SKILL-SPEC-f62885124d-dockerize-gas-city.md) — the dockerize-gas-city skill spec.
- PRs the decision was made in: #1 (lago-morph/software-factory-prototype).
