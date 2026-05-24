# ADR: Bias-guard integration discipline (sanitized neutralization)

- **ID**: ADR-6616438770
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-24
- **Source retrospective**: ../2026-05-24-128.md
- **PRs covered**: #127, #128

## Context

During Phase-1 of the v3 architecture synthesis, three bias-guard subagents (anchor-detector, missing-failure-modes, miscategorization) produced finding-catalogs with IDs like `MISSED-N`, `WEAK-N`, `CANDIDATE-N`. The lead agent integrated several of these findings into the primary v3 artifacts — the failure-mode catalog, the contradictions register, the corpus inventory — to incorporate the audit's substance into the work the next phase would consume.

One specific integration produced a measurable downstream failure. A bias-guard `CANDIDATE-N` finding was promoted to a numbered F-mode entry in the failure-mode catalog. The promotion's "mechanism" field was written with wording that named one specific architectural pattern as the factory's mechanism for handling the failure — phrased as an illustrative description of how the failure manifested, but read by downstream subagents as a corpus claim. All 9 Phase-2 subagents read the F-mode catalog as part of their corpus inputs. Two of three unified-mandate tracks independently converged on the architectural pattern the F-mode wording had named. The Phase-2 axis-divergence auditor identified the F-mode wording as the smoking-gun contamination source. The entire Phase-2 dispatch had to be discarded and re-run from cleaned source files.

A second, softer instance: five of nine Phase-2 tracks cited a specific `WEAK-N` bias-guard sharpening by its ID, treating an auditor's framing as a stable corpus claim. The Phase-2 anchor-detector flagged this as the single most contamination-suspect framing in the run.

The integrations themselves were not wrong — the underlying findings were valuable, and the lead agent's job is exactly to integrate audit output into the running record. The failure was the *form* of the integration: architectural-commitment language in entry wording, real-artifact names in illustrative examples, bias-guard IDs presented in primary-artifact contexts where downstream agents would treat them as corpus references.

## Decision

Lead-agent integration of bias-guard findings into primary artifacts must:

1. **Neutralize architectural-commitment language.** Entry mechanism / claim / definition fields describe the phenomenon (what fails, what's contradicted, what's tagged) without naming a specific architectural pattern as the answer. Pass a neutralization self-check: if the lead agent removes the bias-guard finding's framing language from the integration and the integration still conveys the underlying phenomenon, the wording is neutral.
2. **Use only fictitious placeholders for illustrative examples.** If the rule body contains an example, the example never names a real file path, real ID, or real project-specific term. Use obviously fictitious placeholders (`widgets/example-catalog.md`, `pattern-Q`, `EXAMPLE-FINDING-7`).
3. **Quarantine bias-guard IDs from downstream citation.** Bias-guard finding IDs (`MISSED-N`, `WEAK-N`, `CANDIDATE-N`) live in the bias-guard report files only. Primary artifacts that absorb the substance of a finding cite the underlying corpus material (specific reports, sections, primary quotes), not the finding's ID.
4. **Run a sanitization-audit pass before commit.** A dedicated small subagent reads the proposed integration and flags any real-artifact references that slipped in.

## Alternatives considered

- **No discipline, trust the lead agent's wording.** Rejected: this is what produced the F57-class contamination. The lead agent under load (writing entries for 10+ findings in one pass) does not reliably notice when their illustrative example names a real architectural pattern.
- **Forbid integration entirely; bias-guard findings stay in bias-guard files.** Rejected: the substance of valuable findings would be siloed from primary artifacts. Downstream agents would have to read both the primary artifacts and the bias-guard reports to get the complete picture, and *that* would re-expose the bias-guard report contents to potential contamination.
- **Two-person review (lead agent + user) on every integration.** Rejected: the user already reviews PRs, but the integration happens commit-by-commit during work; gating every integration on synchronous user review halts work for minutes per finding. The sanitization-audit subagent is the asynchronous equivalent.
- **Sanitize in retrospect (clean up after contamination is found).** Rejected: this is what the v3 work had to do; it cost a full Phase-2 dispatch. Prevention is materially cheaper than cleanup.

## Consequences

What becomes easier: downstream subagents can trust primary artifacts as corpus references without re-validating each one against the bias-guard reports. The next session can pick up the v3 work without re-deriving why certain entries are worded a specific way.

What becomes harder: every lead-agent integration step now requires a sanitization-audit dispatch. The cost is small (~10 seconds per integration on a sonnet-class subagent) but it's an additional friction point that the lead agent could forget under pressure.

Trade-off knowingly accepted: every bias-guard finding integration is now slower by one subagent dispatch. The cost is paid every time; the contamination cost is paid only when prevention fails, but each contamination event is materially expensive (full re-runs). Over a long synthesis project the expected-value calculation strongly favors the discipline.

## References

- [`../2026-05-24-128.md`](../2026-05-24-128.md) — the source retrospective.
- [`./SKILL-SPEC-a296db1e83-bias-guard-finding-integration.md`](./SKILL-SPEC-a296db1e83-bias-guard-finding-integration.md) — the skill spec that operationalizes this decision.
- [`./AGENTS-MD-049b4dd1fc-sanitize-examples-in-rules-and-discipline-documents.md`](./AGENTS-MD-049b4dd1fc-sanitize-examples-in-rules-and-discipline-documents.md) — the AGENTS.md rule for the example-sanitization sub-discipline.
- [`./AGENTS-MD-2811ba2d41-bias-guard-id-quarantine-in-subagent-outputs.md`](./AGENTS-MD-2811ba2d41-bias-guard-id-quarantine-in-subagent-outputs.md) — the AGENTS.md rule for the ID-quarantine sub-discipline.
- PRs the decision was made in: #127 (where the contamination was integrated), #128 (where the contamination was identified, the cleanup discipline was developed, and the rule was committed).
