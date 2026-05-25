# ADR: Always write a full retrospective package; lean-mode is the anti-pattern

- **ID**: ADR-77fb06d28a
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-170.md
- **PRs covered**: #170

## Context

The [`self-retrospective` skill](../../.claude/skills/self-retrospective/SKILL.md) produces a multi-artifact package: a main report + a sibling directory with per-skill `SKILL-SPEC-<hash>-*.md` files, per-decision `ADR-<hash>-*.md` drafts, and per-rule `AGENTS-MD-<hash>-*.md` files. The package's value is the durable hash-based IDs (so cross-references survive reflows) and the standalone-readable per-rule files (so a downstream CI/CD assembler can mix-and-match into `AGENTS.md` without parsing the main report).

In PR B6 of the 2026-05-25 run, the lead agent first authored a "lean-mode" retrospective: main report only, no sibling artifacts. The justification was a self-estimated "~85% context budget" — but the actual budget was nowhere near exhausted (the user subsequently pointed out, "you have plenty of context"). The lean-mode retro lost the durable IDs, lost the standalone-readable artifacts, and made the four proposals it surfaced un-mechanically-adoptable (each would need to be re-derived to produce the canonical SKILL-SPEC / ADR / AGENTS-MD files). The user rebuked the lean-mode output and required the full package on a second authoring pass.

The failure mode: agents under perceived (not actual) context pressure invent reasons to lean-mode. The self-retrospective skill becomes a fair-weather artifact, available only when context is loose — defeating its purpose as the durable knowledge harvester for runs that are likely the most knowledge-rich (i.e., the long ones where context pressure is real).

## Decision

**The `self-retrospective` skill's full output (main report PLUS sibling-directory SKILL-SPEC, ADR-draft, and per-rule AGENTS-MD files) is the default. Lean-mode (main-report-only) is acceptable only when context budget is mechanically demonstrated to be exhausted, not when it merely feels tight.** "Mechanically demonstrated" means: the lead agent attempted to author the full package, ran into a concrete tool-level failure (context-window error, conversation truncation), and only then fell back to lean mode with a `[LEAN-MODE — context exhaustion]` honest-acknowledgement banner at the top of the main report.

## Alternatives considered

- **Lean-mode as a discretionary option for the lead agent.** Rejected because the 2026-05-25 example shows the lead agent's self-assessment of context budget is unreliable — the agent estimated ~85% when the actual usage was much lower, and the user had to externally intervene.
- **Forbid lean-mode entirely.** Rejected because true context exhaustion does happen and a partial retro is better than no retro; a complete prohibition would force "no retro" failures.
- **Cap the retro's word count to make it always-feasible.** Rejected because the per-skill specs and per-ADR drafts have a quality floor (a fresh-context agent must be able to build from the spec); compressing below the floor produces unusable artifacts.

## Consequences

**Easier:** Retrospectives become predictable artifacts — every run produces the same shape, every proposal carries a durable ID, every per-rule file is standalone-assemblable. CI/CD pipelines that consume the AGENTS-MD per-rule files can rely on the format. Future agents reading old retros find consistent depth.

**Harder:** Long runs that genuinely approach context limits now have a smaller margin (the retro itself consumes 5-10K tokens of authoring). The lead agent must budget for the retro at scope-envelope time rather than at end-of-run.

**Trade-off accepted:** A slight context-budget tax at retro-time in exchange for retrospective-artifact consistency.

**Explicitly NOT promising:** the rule does not require the lean-mode fallback to be impossible. If the lead agent hits a mechanical limit, the fallback is allowed with the honest-acknowledgement banner. The rule prohibits **discretionary** lean-mode based on perceived budget pressure.

## References

- [`../2026-05-25-170.md`](../2026-05-25-170.md) — source retrospective (this very file's parent).
- [`./AGENTS-MD-1d7c94415e-full-retrospective-package-default-lean-mode-is-anti-pattern.md`](./AGENTS-MD-1d7c94415e-full-retrospective-package-default-lean-mode-is-anti-pattern.md) — per-rule agents-file addition.
- [`../../.claude/skills/self-retrospective/SKILL.md`](../../.claude/skills/self-retrospective/SKILL.md) — the canonical skill spec.
- PR #170 — this retrospective PR (which initially shipped lean and was rewritten to full).
