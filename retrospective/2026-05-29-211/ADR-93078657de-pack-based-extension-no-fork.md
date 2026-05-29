# ADR: Extend Gas City via packs only; no fork required

- **ID**: ADR-93078657de
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209 (introduced wrong framing), #211 (corrected framing)

## Context

When v4 README.md and AI-CONTEXT.md first shipped in PR #209, both documents recommended forking Gas City and vendoring its `internal/` Go paths into a usable module path. The user caught this in subsequent conversation: "Why did you suggest forking gascity? I thought its whole thing was you could extend with packs."

The pushback was correct. Gas City's pack model (TOML configuration + tool node binaries + prompt templates + prompt template materialization) is designed exactly for the kind of extension v4 needs. Packs don't require importing Gas City's Go code — they're declarative configuration plus standalone tool-node binaries called as subprocesses. The `internal/` constraint only matters if you want to use Gas City as a Go library, which v4 doesn't.

I had conflated two distinct earlier-discussed goals in the session: (1) "extract the tmux runtime as a standalone library so OTHER pipeline runners (Kilroy, Mammoth, your own thin reconciler) can use it" — that goal would require forking + vendoring; (2) "extend Gas City for v4" — that goal is pack-shaped. Only (2) is part of v4. PR #211 corrected the framing in both v4 docs.

## Decision

Extend Gas City exclusively via its pack model (TOML config + tool node binaries + prompt templates); do not fork Gas City for v4 work because pack-based extension does not require Go library imports, so the `internal/` path constraints do not apply.

## Alternatives considered

- **Fork Gas City and vendor `internal/` paths into our own module path (the originally-recommended approach).** Rejected because pack-based extension covers all v4 needs and forking commits the team to maintaining a fork forever, including chasing Gas City's two in-flight CI-enforced migrations.
- **Use only the tmux runtime extracted from Gas City as a standalone library.** Rejected for v4 because Gas City's minimum install covers 6 of 12 principles natively (see [`ADR-0aa07c7b72`](./ADR-0aa07c7b72-gas-city-runtime-baseline.md)) — extracting only tmux would forfeit principles 1, 2, 3-basic, 4, 9, 10 native coverage. The extraction option remains valid for *other* pipeline runners that want Claude Code support, but that's a different goal than v4 extension.
- **Mixed: install Gas City + maintain a fork for emergency bug fixes.** Considered but rejected because it adds operational complexity (which version is canonical?) without delivering value during normal operation. Fork only if/when a substrate-level need arises.

## Consequences

What becomes easier:
- All v4 extension is pack-shaped: TOML files + prompt templates + tool node binaries called as subprocesses. No Go imports.
- Upstream Gas City updates flow in via normal release adoption; no rebase pain.
- Gas City's two in-flight migrations don't burden the v4 codebase.
- Phase 0 is "install `gc` from upstream" — single binary install.

What becomes harder:
- If a substrate-level Gas City limitation surfaces (a missing runtime Provider, a needed reconciler modification, an urgent bug fix), the path is contributing upstream or temporarily forking. Either way, not the operational default.
- v4 is constrained to extension shapes that the pack model allows. New runtime Providers (e.g., a new agent runtime beyond tmux/subprocess/exec) would require source-level work that v4 doesn't currently need.

Trade-off accepted: stay within pack model constraints in exchange for clean upstream relationship and no fork maintenance overhead.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective; the session that produced both the original wrong framing and the correction.
- [`./ADR-0aa07c7b72-gas-city-runtime-baseline.md`](./ADR-0aa07c7b72-gas-city-runtime-baseline.md) — Gas City adoption decision.
- `architectures/v4/README.md` Part 5 + Part 9 (corrected in PR #211) — license hygiene table and start-tomorrow steps.
- `architectures/v4/AI-CONTEXT.md` §11.1 + §11.3 (PR #211) — decision log entries: pack-based extension affirmed, fork rejected.
- PRs the decision was made in: #209 (initial wrong framing), #211 (correction).
