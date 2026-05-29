# ADR: Inspect AI as Layer 2 default for scenarios and judge

- **ID**: ADR-f215047ebe
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

v4's Layer 2 implements principles 5 (scenarios as held-out test set) and 6 (satisfaction not test-pass). The OSS landscape for LLM evaluation has matured rapidly: multiple competing frameworks exist with overlapping capabilities (scenario authoring format, runner, judge harness, metric aggregation).

Surveyed candidates:
- **Inspect AI** (UK AISI, MIT) — Python Task DSL, agent-trajectory-aware, multiple scorers, model-agnostic. Designed for safety evaluations originally; the trajectory model maps cleanly onto agent work.
- **promptfoo** (MIT) — YAML-based, prompt-centric, excellent A/B testing built in. Weaker on agent-trajectory evaluation; more focused on single-prompt-multiple-input comparisons.
- **OpenAI Evals** (MIT) — original-of-the-genre, JSONL format widely understood. Smaller community; less actively developed than Inspect AI.
- **DeepEval** (Apache 2.0) — "Pytest for LLMs", excellent developer ergonomics. Smaller community; pack integration would be more bespoke.
- **Ragas** (Apache 2.0) — RAG-specific evaluation. Subset of v4 needs.

Inspect AI was chosen because (a) it's the most mature general-purpose framework, (b) the agent-trajectory model maps cleanly onto Gas City's bead structure (scenario = bead of type "scenario", judge output = bead of type "judgment"), (c) MIT licensed for OSS release viability, (d) UK AISI maintainership signals long-term support.

## Decision

Use Inspect AI (MIT, UK AISI) as the default Layer 2 framework providing scenario authoring, scenario runner, LLM-as-judge harness, and satisfaction aggregation; wrap as a Gas City pack with Inspect AI invoked as a tool node from formulas.

## Alternatives considered

- **promptfoo as default.** Rejected because prompt-centric model doesn't fit agent-trajectory evaluation as cleanly. Remains a viable secondary choice for prompt-variant testing in Layer 6.
- **OpenAI Evals as default.** Rejected because lower activity level and less mature than Inspect AI.
- **DeepEval as default.** Rejected because the Pytest-style developer ergonomics are valuable but the smaller community means more bespoke integration work.
- **Build a custom Layer 2 from scratch.** Rejected because Inspect AI delivers ~80% of what's needed out of the box; custom work would duplicate well-tested code.
- **Defer Layer 2 framework choice; use ad-hoc judge harness for Phase 2 bootstrap.** Rejected because the bootstrap validation needs to evaluate the factory's own work, which requires a real evaluation framework. Inspect AI is small enough to install + wrap during Phase 2.

## Consequences

What becomes easier:
- Phase 2 of v4 is "install Inspect AI + write a Gas City pack that wraps it as a tool node." Bounded scope.
- Scenario authoring uses Inspect AI's Python Task DSL — well-documented, examples available.
- Multi-judge ensemble is native to Inspect AI's scorer composition model.
- Score reduction (satisfaction metric aggregation) is built in.

What becomes harder:
- Inspect AI is Python; v4's other layers are mostly Go (Gas City, CXDB Go client). Cross-language integration means the Inspect AI tool node is a Python subprocess called from Gas City. Manageable but introduces a Python dependency in the Phase 2 stack.
- Inspect AI's session-id model and Gas City's session model may need adapter logic. Likely a small Go wrapper that maps between the two.
- If Inspect AI's roadmap diverges from our needs, switching to promptfoo or building custom is non-trivial but bounded (pack reauthoring rather than substrate rewrite).

Trade-off accepted: Python dependency in Phase 2 stack in exchange for skipping a custom-built Layer 2 evaluation framework.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-0aa07c7b72-gas-city-runtime-baseline.md`](./ADR-0aa07c7b72-gas-city-runtime-baseline.md) — Gas City baseline (the wrapping target).
- `architectures/v4/README.md` Part 4 — Principle 5 and Principle 6 components, with Inspect AI as the OSS choice.
- `architectures/v4/README.md` Part 6 Phase 2 — Phase 2 build steps.
- `architectures/v4/AI-CONTEXT.md` §7 (Layer 2 row) — full per-capability landscape that informed the pick.
- `github.com/UKGovernmentBEIS/inspect_ai` — Inspect AI repo.
- PRs the decision was made in: #209.
