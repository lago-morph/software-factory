# ADR: City scope is a git repo and statically-declared rigs carry per-rig pack imports

- **ID**: ADR-544b6c7cf4
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-07
- **Source retrospective**: ../2026-06-07-7.md
- **PRs covered**: #2, #3, #4, #5, #6, #7

## Context

Two distinct failures traced back to the same theme: gc subsystems resolve context in ways the static prototype config did not satisfy. First, gc's `bd_context_agreement` preflight emitted `native_store_unavailable` and fell back — reproduced on Linux, so not Windows- or version-specific. Live-booting the real stack showed `bd context` resolves a scope via its **git repo root**, and `/workspace/city` was not a git repo (`not a git repository`), so the preflight failed even though the data plane was healthy. Second, the gastown rig roles (witness/refinery/polecat) never expanded, so native dispatch did nothing: `[defaults.rig.imports.gastown]` is only a **template that `gc rig add` consumes** at registration, and the prototype declares rigs **statically** in config and never runs `gc rig add` — so the pack was never imported into any rig.

## Decision

git-init the city directory and give each statically-declared rig its own [rigs.imports.<pack>], because bd resolves a scope's context via its git root and gc's [defaults.rig.imports] is only consumed by `gc rig add` — without both, the bd_context preflight fails and the rig-scoped agents never expand.

## Alternatives considered

- **Run `gc rig add` at entrypoint instead of declaring rigs statically** — viable (it would consume `[defaults.rig.imports]` correctly), but it changes the entrypoint model from declarative static config to imperative registration; rejected for now to keep the prototype's config declarative and inspectable.
- **Leave force_fallback on instead of fixing the preflight** — rejected: forcing the `bd` subprocess path masks the real cause and reintroduces the 3s-timeout regression seen in PR #3.

## Consequences

- Native dispatch works end-to-end: `gc agent list` shows `rigN/gastown.{witness,refinery,polecat}`, the mayor routes, the polecat pool auto-scales 0→1, polecat commits on a branch, refinery merges into the rig, and the bead closes (verified live with a real commit `542f2ef` in rig1 main).
- The per-rig `[rigs.imports.gastown]` block is boilerplate that must be kept in sync across every `[[rigs]]` — a maintenance cost accepted in exchange for keeping rigs statically declared.
- The entrypoint now git-inits the city dir, so any tool that resolves scope via git root works.
- Behavioral note for operators: the mayor **triages** and will not blindly sling every open bead (gastown design); a `gc session nudge` or an explicit `gc sling rigN/gastown.polecat` routes a specific bead.

## References

- [`../2026-06-07-7.md`](../2026-06-07-7.md) — the source retrospective.
- PRs the decision was made in: #4, #6, #7.
