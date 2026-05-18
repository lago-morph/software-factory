# agent instruction

**Author canonical templates before referencing them in convention prose.** "When defining a convention that produces structured artifacts (skill specs, ADRs, agents-file fragments, report layouts), write the canonical template file in `resources/template-*.md` first, then have the convention prose link to it (e.g., 'copy from `resources/template-X.md`'). Freehand authoring from the prose drifts across consumers and across retros."

*Grounded in: PR #95 third round that added `resources/template-{retrospective-report,skill-spec,adr-draft,agents-md-rule}.md` and rewrote Steps 4, 5, 5.5, 6 to reference them.*

# justification

PR #95 ended up with two rounds of "freehand authoring drifted" — the consolidated `AGENTS-suggestions.md` format and then the first iteration of per-rule files. The third round added four canonical templates in `resources/`, then went back and reworked Steps 4, 5, 5.5, and 6 of the SKILL.md and the corresponding SPEC.md sections to instruct authors to copy from the templates. The drift cost would have compounded across every future retrospective: each author would slightly re-interpret the freehand format, and downstream tooling (the CI/CD `AGENTS.md` assembler, link checkers, retro-coverage audits) would fail on subtle inconsistencies.

The marginal cost of writing the template first is ~5 minutes per artifact type. The marginal benefit is that every consumer copies from the same source. This is the same single-source-of-truth pattern documented in the `single-source-of-truth-data` skill, applied to documentation conventions instead of data files. Adopt the rule and the template directory becomes the contract; skip it and the convention rots through retro-by-retro drift.
