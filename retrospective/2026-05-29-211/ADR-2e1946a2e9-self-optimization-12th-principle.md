# ADR: Add self-optimization as the 12th working principle

- **ID**: ADR-2e1946a2e9
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

El Kaim's "Dark Factory" synthesis enumerates 11 + 1 principles for AI software factories. The 12th principle in the original list is "pipeline files worth sharing" — a community-norms commitment about publishing pipeline files as OSS so the community of dark-factory builders can share infrastructure.

During the v4 planning session, the user asked: "Is self optimization one of the principles?" The honest answer (verified against the El Kaim 12 principles): no. The closest matches are principle 11 (self-healing loop, about fixing what broke) and principle 8 ("why am I doing this?", about converting manual overrides into validation rules). Neither covers what self-optimization means: the system measures its own meta-performance (cost-per-satisfaction, judge false-positive rate, etc.) and identifies, tests, and promotes variants that improve it.

The user observed that the absence of self-optimization is a real gap. The corpus reflects what teams have publicly demonstrated; StrongDM has reportedly achieved self-healing but not self-optimization at scale. So the 12 principles describe what's known to work, not what's aspirational.

For v4 specifically, principle 12 in El Kaim's form ("publish your pipeline files") is a release-time decision, not a runtime component. It doesn't shape the substrate. Self-optimization, by contrast, is a real architectural capability: it requires CXDB content-addressed trajectory storage, meta-metric tracking, variant testing harness, A/B routing, statistical comparison, promotion gates. Each of these slots into the runtime architecture.

Substituting self-optimization for "publish your pipeline files" in the v4 working set keeps the count at 12 while making the principle slot operative — something v4 designs for, not just declares.

## Decision

Substitute self-optimization (the system measures its own meta-performance and improves it via variant testing) for El Kaim's original 12th principle (publish your pipeline files, a community-norms commitment) in v4's working set, because self-optimization is the natural architectural extension after self-healing and the publish principle is a release-time decision rather than a runtime component.

## Alternatives considered

- **Keep "publish your pipeline files" as the 12th principle.** Rejected for v4 because it doesn't shape the runtime architecture; it's a release-time decision separately addressable. We can still commit to publishing as a release-time matter, just not as a runtime principle.
- **Add self-optimization as a 13th principle (don't substitute).** Considered. Rejected because the El Kaim 12 is the corpus's anchor; growing the count opens the door to "what's principle 14, 15, ..." debates. Substitution keeps the count stable while shifting the slot to a runtime-shaping principle.
- **Don't add self-optimization at all; defer to "future work".** Rejected because v4's bootstrap pattern (factory builds factory after Layer 2) requires meta-metrics for the factory to know whether its own work is improving. Without self-optimization in the principle set, the bootstrap loop has no quality compass.
- **Wait until the corpus formally adopts self-optimization before adding it.** Rejected because the corpus reflects past demonstrated work; v4 is forward-looking. The 12th-principle substitution is a v4-specific working choice, not a claim on the corpus.

## Consequences

What becomes easier:
- v4's Layer 6 has principle-level grounding (P12) rather than being "extra work beyond the 11 principles."
- Bootstrap loop has a quality compass: variants are tested against meta-metrics, winners are promoted.
- CXDB's counterfactual replay (O(1) trajectory branching) gets architectural justification — it's load-bearing for P12.

What becomes harder:
- v4 is one principle out of step with the corpus's canonical 12. Documentation needs to explain the substitution clearly to avoid confusion.
- Publishing pipeline files (original P12) becomes a release-time discipline rather than a runtime principle; needs separate attention.
- Self-optimization at scale isn't publicly demonstrated; v4's P12 implementation is research-frontier. Higher risk on the most ambitious layer.

Trade-off accepted: one-step-out-of-step with corpus canon + research-frontier P12 implementation in exchange for a 12-principle set that's all runtime-shaping.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-4f2353b39d-v4-principle-bound-runtime.md`](./ADR-4f2353b39d-v4-principle-bound-runtime.md) — runtime framing that motivates the substitution.
- `architectures/v4/README.md` Part 4 (Principle 12) — full decomposition of self-optimization into components.
- `architectures/v4/AI-CONTEXT.md` §1 — 12 working principles list noting the substitution.
- `architectures/v3/build-guide/02-paradigm.md` — original El Kaim 12 principles for reference.
- `reference-only/f675af7d98/dark-factory-article.txt` — El Kaim source.
- PRs the decision was made in: #209.
