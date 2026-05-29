# ADR: Pivot from methodology-pick to principle-bound runtime

- **ID**: ADR-4f2353b39d
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209, #210, #211

## Context

The v3 work produced ten candidate methodologies (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1), each with a specific bet about what the load-bearing piece of an AI factory is. The natural question that emerged was "which one do we build?" The v4 answer is: that's the wrong question to ask first.

The corpus's central finding (documented in `architectures/v3/build-guide/03-substrate.md` and reinforced by the OSS substrate convergence across Kilroy, Fabro, Mammoth, Smasher, Tracker, OpenHands, Overstory, Gas City) is that *methodology is the variable; substrate is convergent*. Multiple independent teams building dark-factory implementations converge on the same three-layer architecture. The methodology that runs on top is where the variation lives.

The user articulated the pivot directly: "What if instead of figuring out the right methodology, we instead create tooling and the most basic environment that supports the 11 principles other than sharing pipeline files? We get all that in place around Claude code. The simplest factory is just prompt response. What do we get if we add those 11 supporting structures? Then start layering on top of that." This was the pivot moment.

## Decision

Build a principle-bound runtime that supports the 12 working principles (the El Kaim 11 plus self-optimization as the 12th); treat methodologies as configurations (pipeline files + custom nodes) that run on top of the runtime rather than as architectural decisions to commit to in advance.

## Alternatives considered

- **Pick one of the v3 ten candidates and build for it (the v3-implicit framing).** Rejected because (a) the choice would lock in substrate-shaped commitments that are hard to reverse, (b) the bet on any specific candidate is speculative without empirical evidence, (c) wrong-methodology means rebuilding substrate (high cost) whereas wrong-pipeline-file means rewriting a config file (low cost).
- **Pick a small set of v3 candidates (e.g., GF-M + BF-M) and build for both.** Rejected because the runtime work has to be done either way; building for "all candidates that could run on the runtime" is strictly cheaper and gives optionality. This is in effect what the principle-bound runtime achieves.
- **Defer the decision and wait for more evidence.** Rejected because the runtime is the gating step — until it exists, no methodology can be tested, so deferring delays evidence-gathering indefinitely.

## Consequences

What becomes easier:
- Testing v3 methodologies becomes "write a pack" instead of "build a new factory".
- New methodology ideas after v3 can be tested on the same runtime without re-architecting.
- The runtime's principle-grounding gives every methodology a baseline level of discipline.
- Pivoting away from a methodology that doesn't work is cheap (delete the pack).

What becomes harder:
- The runtime has to support a wider range of methodology shapes than any single candidate would have required. Some shapes may not fit cleanly.
- The runtime work is the front-loaded engineering investment; nothing is testable until it ships.
- The user has to defer methodology curiosity until the runtime is up.

Trade-off accepted: front-load engineering investment in substrate to gain methodology optionality afterward.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-0aa07c7b72-gas-city-runtime-baseline.md`](./ADR-0aa07c7b72-gas-city-runtime-baseline.md) — choice of substrate baseline.
- [`./ADR-2e1946a2e9-self-optimization-12th-principle.md`](./ADR-2e1946a2e9-self-optimization-12th-principle.md) — 12th principle decision.
- [`./ADR-831c29ac19-factory-builds-factory-bootstrap.md`](./ADR-831c29ac19-factory-builds-factory-bootstrap.md) — bootstrap pattern that follows from this pivot.
- `architectures/v4/README.md` (PR #209) — full human-facing approach.
- `architectures/v4/AI-CONTEXT.md` (PR #209) — dense session capture.
- `architectures/v4/F-MODE-COVERAGE.md` (PR #210) — how the pivot maps against catalogued failure modes.
- PRs the decision was made in: #209.
