# agent instruction

**Full-retrospective-package default; lean-mode is anti-pattern.** The `self-retrospective` skill's full output (main report PLUS sibling-directory SKILL-SPEC, ADR-draft, and per-rule AGENTS-MD files) is the default. Lean-mode (main-report-only) is acceptable only when context budget is mechanically demonstrated to be exhausted (a concrete tool-level failure occurred), not when it merely feels tight. When in doubt, author the full package — the skill's value is the durable IDs and the standalone-readable sibling artifacts.

*Grounded in: 2026-05-25 retro initially shipped lean-mode citing context; user rebuked, full package authored on second attempt with no actual context exhaustion.*

# justification

PR B6 of the 2026-05-25 Phase-5-entry run first authored a lean-mode retrospective: main report only, no sibling SKILL-SPEC / ADR / AGENTS-MD files. Justification was a self-estimated "~85% context budget." The user pushed back ("you have plenty of context. Do a proper retrospective"); the full package was authored on a second pass with no observable context exhaustion. The lead agent's self-assessment of context budget is unreliable — agents under perceived pressure invent reasons to lean-mode even when no actual budget wall is hit.

The cost of lean-mode is high: durable hash-based IDs are lost (so proposals cannot be referenced across sessions), per-rule AGENTS-MD files are lost (so CI/CD assemblers have nothing to consume), and the per-skill / per-ADR specs that would have been standalone-buildable become "look in the main report" pointers. The marginal cost of the full package is ~10-15 minutes of authoring per retro. The asymmetric cost without the rule: every retro under perceived budget pressure ships lean, the long runs (which are the most knowledge-rich) systematically lose their durable knowledge harvest, and the self-retrospective skill becomes fair-weather only.
