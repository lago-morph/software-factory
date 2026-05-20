# agent instruction

**Pair synthesis reports with companion deep-dive followups.** When a session produces a dense analysis of a new corpus source (especially via parallel subagent dispatch), commit both a synthesis report at the top level (`research/NN-<slug>.md`) AND companion deep-dive references in `research/followup/MM-<slug>.md`. The synthesis carries the actionable mapping and cross-source ties; the followup carries the verbatim subagent output as the durable reference. Both must be registered in `research/INDEX.md` in the same commit.

*Grounded in: PR #101 — report 38 + followup/13 + followup/14 (Gas City / Gas Town substrate analysis).*

# justification

PR #101 dispatched two parallel subagents that produced ~10.2k + ~9.3k words of citation-rich architecture references for Gas City and Gas Town. The synthesis report (research/38, ~7.9k words) mapped both onto the Dark Factory and Compound Engineering primitive sets — that is the actionable artifact a reviewer of the parent project's architecture comparison can use. The two deep-dives are the durable reference future AI sessions will load when they need to know which `internal/` package implements the bead store or how `gt seance` routes predecessor-session queries.

Committing only the synthesis would have orphaned ~20k words of careful subagent output that the synthesis itself depends on; committing only the deep-dives would have left no usable mapping into the parent project's failure-mode catalogue. The corpus already enforces this pattern unevenly — report 03 (Every compound engineering) → followup/05 + followup/11; report 07 (Dark Factory) → followup/04 — but the pattern is implicit, so future sessions sometimes ship only one half. Making the pairing an explicit rule turns "the pattern most corpus contributions accidentally followed" into "the pattern every dense-source contribution explicitly follows," and the INDEX.md co-registration requirement makes the pair findable from a single grep.

The marginal cost is one extra file per source plus two extra INDEX rows. The cost of skipping it is the next session has to either re-do the deep dive (token waste) or ship a synthesis whose claims they cannot verify (provenance erosion).
