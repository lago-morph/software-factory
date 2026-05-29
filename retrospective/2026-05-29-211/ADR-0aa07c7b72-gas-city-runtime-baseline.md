# ADR: Adopt Gas City as v4 runtime baseline

- **ID**: ADR-0aa07c7b72
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

Once the v4 decision was made to build a principle-bound runtime (see [`ADR-4f2353b39d`](./ADR-4f2353b39d-v4-principle-bound-runtime.md)), the next question was which third-party substrate to build on. The OSS landscape for pipeline runners includes Kilroy (Shapiro, Go), Mammoth (2389 research, Go), Smasher (2389, Rust), Tracker (2389, Go), Fabro (Bryan Helmkamp / Qlty.sh, Rust), Gas City (Steve Yegge / Gas Town Hall, Go), plus OpenHands and Overstory which are agent runtimes more than pipeline runners. A research subagent surveyed each project's coverage of v4-relevant principles (documented in `architectures/v3/build-guide/03-substrate.md` and the layer-2-6 coverage research in PR #209's preparation).

Gas City's smallest viable install (~30 lines of TOML) handles principles 1, 2, 3-basic, 4, 9, and 10 natively. Specifically, Gas City's bead store + event bus + attribution model is the strongest match in the corpus for principle 9 (attribution), and beads handle principle 10 (memory layer) cleanly. The pack-based extension model (TOML configuration + tool node binaries + prompt templates) means custom extension doesn't require forking. Progressive activation (turn on `[formulas]` for principle 3, `[mail]` for inter-agent messaging, etc.) lets the build start tiny and grow.

Kilroy is the simplest reference but lacks Gas City's attribution depth and work-ledger sophistication. Mammoth's 21-rule DOT linter is valuable but its strength is the DOT runtime, not the broader principle support. Fabro's CSS model stylesheet is excellent for cost-aware routing but its operator surface is more elaborate than v4 needs at start.

## Decision

Use Gas City (Steve Yegge / Gas Town Hall) as the load-bearing third-party dependency for v4's runtime; the smallest viable Gas City install handles principles 1, 2, 3-basic, 4, 9, and 10 natively without any custom code, and the pack model handles all v4 extension needs.

## Alternatives considered

- **Kilroy as baseline.** Rejected because Kilroy lacks Gas City's beads-with-attribution model; we'd be building principle 9 + 10 substrate from scratch. Kilroy remains a strong transfusion source for the CXDB integration pattern (see [`ADR-d566506f19`](./ADR-d566506f19-cxdb-bridge-path.md)).
- **Mammoth as baseline.** Rejected because Mammoth (which wraps the Tracker library) is more DOT-runtime than full-principle substrate. Tracker's `Diagnose`/`Audit`/`Doctor` programmatic APIs are the strongest Layer 4 transfusion source — adopted as transfusion source, not as runtime baseline.
- **Build from scratch on top of Claude Code subagents alone.** Rejected because Claude Code's skill + subagent + hook + MCP combo covers a lot but doesn't have a proper work ledger, attribution model, or formula DAG runtime. Building those from scratch is what Gas City already provides.
- **Adopt Fabro as runtime.** Rejected because Fabro is Rust (vs. our Go preference for downstream pack-binary work) and its operator surface is more sophisticated than v4 needs at Phase 0. Fabro's CSS model stylesheet is a transfusion source for Layer 6 cost-aware routing, not a runtime baseline.
- **Overstory as multi-agent runtime.** Rejected because Overstory was archived 2026-05-28 (one day before this session). Warren is the successor, status unverified.

## Consequences

What becomes easier:
- Phase 0 of v4 is essentially configuration (one `pack.toml` + one `city.toml` + one prompt template).
- Principles 1, 2, 3-basic, 4, 9, 10 are delivered immediately without custom code.
- Attribution (principle 9) is the strongest native match in the corpus.
- Pack-based extension means all subsequent layers ship as pack additions, not substrate modifications.

What becomes harder:
- Vocabulary cost (cities, rigs, formulas, molecules, packs) — real cognitive load, paid once, recoverable.
- Migration tail risk: Gas City has two CI-enforced migrations in flight (worker boundary, session-first). Expect 1-2 breaking pack-schema or formula-format changes per quarter through 2026.
- `internal/` paths in Go block direct module import — only matters if v4 ever needs to use Gas City as a Go library, which the pack model avoids (see [`ADR-93078657de`](./ADR-93078657de-pack-based-extension-no-fork.md)).
- Lock-in to Gas City's specific design choices (Dolt for serious storage, OTP reconciler, TOML formulas). Migration away would be substantial.

Trade-off accepted: vocabulary cost + migration tail risk + design lock-in in exchange for skipping ~Layer-1 build entirely.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-4f2353b39d-v4-principle-bound-runtime.md`](./ADR-4f2353b39d-v4-principle-bound-runtime.md) — runtime framing.
- [`./ADR-93078657de-pack-based-extension-no-fork.md`](./ADR-93078657de-pack-based-extension-no-fork.md) — extension model.
- `architectures/v4/README.md` Part 4 (PR #209) — per-principle Gas City placement.
- `architectures/v4/AI-CONTEXT.md` §3 (PR #209) — Gas City coverage map.
- `research/followup/13-gas-city-deep-dive.md` — deep-dive that informed the choice.
- PRs the decision was made in: #209.
