# ADR: Use the synthesis-plus-companion-deep-dive pattern for dense corpus contributions

- **ID**: ADR-cf8bdf804a
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-20
- **Source retrospective**: ../2026-05-20-101.md
- **PRs covered**: #101

## Context

The research corpus already produces two distinct artifact types when it analyzes a new source: a **synthesis report** at the top level (`research/NN-<slug>.md`) that maps the source onto the failure-mode catalogue, the candidate architectures, and the corpus' cross-cutting themes; and **companion deep-dive followups** (`research/followup/MM-<slug>.md`) that carry the verbatim provenance-rich detail a future AI session would need to verify or extend a claim. The pattern is implicit — report 03 (Every compound engineering) → followup/05 + followup/11; report 07 (Dark Factory) → followup/04; report 28 (Schillace Sunday Letters) → embedded harness diagrams in followup/06.

PR #101 (Gas City + Gas Town substrate analysis) followed the same pattern deliberately: two parallel subagents produced ~10.2k + ~9.3k words of deep architecture references; the synthesis report (research/38, ~7.9k words) mapped both onto the StrongDM Dark Factory and Every.to Compound Engineering primitive sets. The pairing was natural because the deep-dives carry citation-rich provenance and the synthesis is the actionable mapping — neither alone would have served a downstream reader well.

The session also surfaced cases where the pattern is currently absent: report 12 (adjacent ecosystem) covers many sources at moderate depth without companion followups; reports 25 + 26 (RE/SE + LLM-prompt-underspec from Round 9) have no companion deep-dives. In each case the result is the same: claims that the future reader cannot verify without re-fetching the primary sources, and provenance that lives only in the report's "Sources reviewed" table.

The corpus has accumulated enough evidence — and PR #101 is concrete enough as a worked example — to codify the pattern as a binding rule rather than leave it as a recurring accident.

## Decision

When a session produces a dense analysis of a new corpus source via parallel subagent dispatch (or comparable depth), the unit of contribution is one synthesis report at the top-level `research/` plus one or more companion deep-dive followups at `research/followup/`, both registered in `research/INDEX.md` in the same commit.

The synthesis report is the actionable artifact: it carries the mapping onto the corpus' shared frames (failure modes, architectures, themes, cross-source ties), and is the natural entry point for a reader who is sizing up the source. The deep-dive is the durable reference: it carries the verbatim provenance, the citation chain, and the structural detail that the synthesis abstracts away. Both must be registered in `research/INDEX.md`'s numbered-reports table and follow-up-reports table respectively, in the same commit, so a single grep against INDEX surfaces the pair.

## Alternatives considered

- **Synthesis-only.** Cheaper to produce (skip the deep-dive entirely) and matches the corpus pattern for routine sources. Rejected for dense sources because the synthesis claims rest on provenance the future reader cannot verify without re-fetching the primary sources — exactly the failure mode the corpus' "Sources reviewed" discipline already tries to prevent. The synthesis becomes load-bearing for downstream architecture work; its claims must be auditable.
- **Deep-dive-only.** Captures the provenance richly but orphans the actionable mapping. The corpus' value comes from cross-source ties (failure-mode catalogue, candidate architectures, recurring themes); a deep-dive without a synthesis loses that integration. Future readers would have to do the synthesis work themselves on each lookup.
- **Inline-embedded** (deep-dive content folded into the synthesis as a giant appendix). Rejected because the synthesis word-count target (≤3,500 words for actionable readability) is incompatible with the deep-dive's typical 8–10k-word size. Folding produces a single artifact that is too long to read in either mode.
- **One synthesis + one combined deep-dive** (single followup file covering both subagent outputs). Workable for two related sources, but breaks down at three or more, and obscures the per-source provenance trail. The corpus pattern is one deep-dive per source.

## Consequences

What becomes easier:

- A future AI session loading just the synthesis can act on the mapping; loading just the deep-dive can verify any claim against the cited primary sources.
- The `research/INDEX.md` co-registration makes the pair findable from a single grep against either the source slug or the source URL.
- Subagent-produced deep-dives have a clear committal home — they are no longer "long output that the synthesis depends on but doesn't ship with."
- The pairing is explicit, so future sessions don't accidentally ship only one half.

What becomes harder:

- Every dense-source PR carries at least three new files (1 synthesis + 1+ deep-dives + INDEX update). The PR review surface is larger.
- The pairing rule needs a way to scale to more than two parallel subagents — when 4+ subagents produce 4+ deep-dives for related sub-sources, the synthesis has to integrate four threads. PR #101 had two; the pattern's behavior at higher fan-out is untested.

What trade-off is accepted:

- Extra authorship cost per dense contribution, in exchange for permanent verifiability and the load-bearing-mapping/durable-reference split. The cost compounds positively: the deep-dive of source N becomes the input to the synthesis of source N+1 when they share a theme.

## References

- [`../2026-05-20-101.md`](../2026-05-20-101.md) — the source retrospective.
- [`./SKILL-SPEC-5782bfb04d-substrate-fit-assessment.md`](./SKILL-SPEC-5782bfb04d-substrate-fit-assessment.md) — the skill spec for the substrate-fit-assessment shape, which is the natural consumer of synthesis + companion deep-dive pairs.
- [`./AGENTS-MD-6d2ec706a7-pair-synthesis-with-followup-deep-dives.md`](./AGENTS-MD-6d2ec706a7-pair-synthesis-with-followup-deep-dives.md) — the operational rule that translates this decision into per-agent guidance.
- Worked example: `research/38-gas-systems-substrate.md` + `research/followup/13-gas-city-deep-dive.md` + `research/followup/14-gas-town-deep-dive.md` (the PR #101 trio).
- Prior corpus instances of the pattern (implicit; this decision codifies):
  - `research/07-dark-factory.md` + `research/followup/04-gastown-beads.md`
  - `research/03-every-compound-engineering.md` + `research/followup/05-klaassen-siblings.md` + `research/followup/11-compound-knowledge.md`
  - `research/02-strongdm-attractor.md` + `research/followup/02-attractor-implementations.md`
- PRs the decision was made in: #101.
