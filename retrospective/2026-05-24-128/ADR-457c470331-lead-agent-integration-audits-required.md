# ADR: Lead-agent integration audits required

- **ID**: ADR-457c470331
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-24
- **Source retrospective**: ../2026-05-24-128.md
- **PRs covered**: #127, #128

## Context

Several phases of the v3 architecture synthesis include a "lead-agent integration" step: a synthesis pass where the lead agent combines outputs from multiple subagents into a single primary artifact. The most consequential example was Phase-1's bias-guard integration, where three bias-guard reports (anchor-detector, missing-failure-modes, miscategorization) produced findings that the lead agent absorbed into the failure-mode catalog, the contradictions register, and the corpus inventory. Other examples: Phase-3 merge of parallel-track outputs into mandate-specific syntheses; Phase-6 ADR drafting from architecture specs.

The Phase-1 integration produced a measurable downstream failure (see ADR-6616438770 on bias-guard integration discipline). The root cause was not the substance of any specific integration — the findings were valuable, the integrations were correct in scope. The root cause was that lead-agent integrations are *single-author*: the lead agent reads N findings, writes N integrations, and commits the batch without an independent review of how the wording landed. Under that workflow, illustrative-example language that smuggles in architectural commitments is invisible to the author and invisible to the user (who reviews PRs at the diff-summary level, not at the wording-of-each-F-mode-mechanism level).

The pattern generalizes beyond bias-guard integration. Any lead-agent step that authors primary-artifact content from multiple inputs has the same structural risk: the author's framing leaks into the artifact, the artifact then seeds downstream subagents, and the downstream convergence looks like signal but is amplification.

## Decision

Every lead-agent integration step must include a dedicated audit pass via a small subagent before commit. "Integration step" means any of:

- Combining bias-guard findings into a primary artifact (catalog entries, register entries, inventory tags).
- Merging multiple parallel-subagent outputs into a single synthesis.
- Writing illustrative examples into rules, decisions, or discipline documents.
- Drafting an ADR from a session's discussions and code changes.
- Promoting a CANDIDATE to a numbered F-mode or equivalent.

The audit pass is a sonnet-class subagent (opus is overkill) with a narrow brief: scan the proposed integration for real-artifact references that should have been fictitious placeholders, for architectural-commitment language that should have been neutral phenomenon-description, and for downstream-citation patterns that would lend the integration's framing the weight of a primary source. The audit returns findings only; the lead agent applies fixes; a second audit pass runs if findings were extensive.

## Alternatives considered

- **No audit; trust the lead agent's wording.** Rejected: this is the current state and it produced the F57 contamination. The lead agent under load (writing entries for 10+ findings in one pass) does not reliably notice the failure modes the audit catches.
- **User reviews each integration at commit time.** Rejected: the user already reviews PRs, but at the diff-summary level. Gating each integration on synchronous user review halts work for minutes per integration; for 10+ integrations per pass, the cumulative delay is unworkable. The audit subagent is the asynchronous equivalent.
- **Run all integrations as subagent dispatches (no lead-agent authorship).** Rejected: lead-agent authorship is sometimes the right call (when the integration requires cross-finding judgment the subagent cannot perform from a single brief). The decision is not to eliminate lead-agent authorship but to add an audit pass after it.
- **Add a manual checklist to lead-agent integrations.** Rejected: checklists work for mechanical checks (filename conventions, link validity) but fail for judgment checks (is this example fictitious enough? is this wording neutral?). A subagent applies the judgment without the original author's blind spots.

## Consequences

What becomes easier: lead-agent integrations are no longer single points of failure. The audit pass catches the specific class of wording errors the F57 case demonstrated.

What becomes harder: every integration pass now adds one subagent dispatch. The cost is small per integration (~10-30 seconds on sonnet) but it's a friction point that can be forgotten under pressure. The audit subagent's own briefs must be kept current (what to scan for evolves as new failure modes are discovered).

Trade-off knowingly accepted: integration steps are slower by one subagent dispatch each. The contamination cost is paid only when prevention fails, but each contamination event is materially expensive (full re-runs). The expected-value calculation favors the discipline for any project with multiple integration phases.

## References

- [`../2026-05-24-128.md`](../2026-05-24-128.md) — the source retrospective.
- [`./ADR-6616438770-bias-guard-integration-discipline.md`](./ADR-6616438770-bias-guard-integration-discipline.md) — the related ADR on bias-guard integration discipline (this ADR is the general-form version of the same discipline).
- [`./SKILL-SPEC-a296db1e83-bias-guard-finding-integration.md`](./SKILL-SPEC-a296db1e83-bias-guard-finding-integration.md) — the skill spec that operationalizes the integration step + audit pattern for the bias-guard case.
- PRs the decision was made in: #127 (where the contamination was integrated), #128 (where the contamination was identified, the cleanup discipline was developed, and the audit pattern was used in production for D5/D6/D7 sanitization).
