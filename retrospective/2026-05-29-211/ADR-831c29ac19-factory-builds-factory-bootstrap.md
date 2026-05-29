# ADR: Factory builds factory bootstrap pattern after Layer 2

- **ID**: ADR-831c29ac19
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

v4's implementation plan has 4 phases. Phase 0 = minimum Gas City install. Phase 1 = verbatim OSS adoption (LangFuse, CXDB, formula↔DOT translator, CXDB bridge pack). Phase 2 = Layer 2 (scenarios + judge via Inspect AI). Phase 3+ = layers 3-6 (observability + "why" discipline, self-healing loop, digital twins, self-optimization).

The question: who builds Phase 3+? The naive answer is "the team builds it the way they built Phases 0-2". The user asked: "What do you think of a plan where we get layers 0-1 up, and as much partial stuff as we can scavenge from elsewhere, and let the factory build the rest itself, for itself?"

The factory-builds-factory pattern has empirical precedent: StrongDM reportedly used their platform to build their platform's extensions. Once the principle-bound runtime is up with scenarios + judge (Phase 2), it can be turned on its own development work. The work is well-suited:
- Components are scoped, bounded, evaluatable.
- Scenarios constrain what "done" means.
- Gene transfusion from existing OSS exemplars reduces invention risk (see [`ADR-related skill spec`](./SKILL-SPEC-31da471000-gene-transfusion-discipline.md)).
- Human design-review at each component piece adds a checkpoint.

Critical constraint: Layer 2 must come before factory-builds-factory begins. Without scenarios + judge, the factory has no way to evaluate its own work — humans become the evaluation bottleneck (the L3 trap that v4 is supposed to avoid).

The bootstrap validation moment is in Phase 2: the first non-trivial component the factory builds for itself (candidate: the raw-API-bodies → CXDB bridge pack). If that succeeds with reasonable human design review, the bootstrap pattern is validated. If it fails, the pattern needs reconsideration before Phase 3 begins.

## Decision

After Phases 0-2 deliver the minimum principle-bound runtime with scenarios and judge, use the factory itself to build Layers 3-6 (the remaining components) with human design review at each piece and gene-transfusion from established OSS exemplars; this is the StrongDM pattern (their platform was built first, methodology emerged from running it).

## Alternatives considered

- **Team builds all 6 phases the traditional way.** Rejected because front-loading all engineering investment loses the bootstrap leverage and treats the factory as something other than what it claims to be. If the factory can't build factory components, it probably can't build user software either.
- **Factory builds factory from Phase 1 (skip waiting for Layer 2).** Rejected because without scenarios + judge, the factory's own work has no evaluation signal beyond human review. Evaluation becomes the bottleneck and the bootstrap loop never converges.
- **Pick a subset of Phase 3+ for factory-build, do rest by hand.** Considered. The recommended ordering is factory-build for everything in Phase 3+, with human design review at each piece. This delivers leverage while preserving safety. Falling back to hand-build for a specific component is always an option if a factory-built attempt fails repeatedly.
- **Use a different agent for factory-build (not Claude Code under Max).** Rejected because v4's Phase 0-1 substrate is built around Claude Code; switching agents at Phase 3 introduces substrate-level changes. Sticking with Claude Code preserves the principle bindings.

## Consequences

What becomes easier:
- Phases 3-6 ship without proportional team engineering hours. The leverage is real.
- Components are bounded, scoped, evaluatable — well-suited to current-generation agent work.
- Gene transfusion from OSS exemplars (LocalStack for twins, Tracker for diagnosis, DSPy for variant identification) reduces invention risk.
- Each Phase 3+ piece is a separate factory-build with separate human design review, separate deployment — bounded blast radius.

What becomes harder:
- Phase 2 must include the bootstrap validation moment explicitly. First non-trivial factory-built component is the critical test.
- Human design review at each piece is real engineering attention, not zero-cost. Per-piece review budget needs to be planned.
- If the bootstrap pattern fails (factory can't reliably build factory components), v4 falls back to team-builds-everything, losing the leverage. This is a real risk.
- Drift in self-improvement loops is a real concern. Mitigation: external grounding (CXDB, Temporal stay as upstream OSS, factory builds the glue not the foundations).
- Layer 6 (self-optimization) is the highest-risk factory-build because the integration is research-frontier. Heaviest human review required.

Trade-off accepted: bootstrap validation risk in Phase 2 + per-piece human review burden in Phase 3+ in exchange for substantial leverage on the remaining engineering.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-4f2353b39d-v4-principle-bound-runtime.md`](./ADR-4f2353b39d-v4-principle-bound-runtime.md) — runtime framing that enables the bootstrap.
- [`./SKILL-SPEC-31da471000-gene-transfusion-discipline.md`](./SKILL-SPEC-31da471000-gene-transfusion-discipline.md) — the technique that makes factory-builds-factory tractable.
- `architectures/v4/README.md` Part 6 (Phases 3+) — implementation phases.
- `architectures/v4/README.md` Part 7 (self-bootstrap mechanic) — discipline patterns.
- `architectures/v4/AI-CONTEXT.md` §11.1 — decision logged.
- PRs the decision was made in: #209.
