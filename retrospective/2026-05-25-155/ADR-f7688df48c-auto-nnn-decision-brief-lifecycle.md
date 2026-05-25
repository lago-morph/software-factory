# ADR: Auto-NNN decision-brief lifecycle for autonomous sessions

- **ID**: ADR-f7688df48c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-155.md
- **PRs covered**: #146, #147, #149, #150, #152, #154, #155

## Context

Autonomous (unattended) sessions on the v3 synthesis pipeline have produced four decision briefs to date: `auto-001` (Phase 3.5 dispatch shape, overnight 2026-05-25), `auto-002` (U-B P-31 path, overnight 2026-05-25), `auto-003` (BF-L per-RG-view choice, this session), and `auto-004` (Phase 4 dispatch shape, this session). All four converged on the same lifecycle independently: lead-agent writes Round 1 with the best-call decision + implementation framing; ≥2 real adversarial subagents review; Round 2 revises based on findings; Round 1 is preserved struck-through for traceability. The pattern is currently encoded informally — there is no ADR binding it.

The cost of *not* having this lifecycle is documented in the [AGENTS.md adversarial-review rule](../../../AGENTS.md#adversarial-review-must-be-real-subagents): inline-simulated reviewers inherit the lead agent's anchoring; they produce objections the lead agent has already mentally defused and counter-proposals the lead agent has already prepared rebuttals for. The auto-001 R1 → R2 transition (per-cluster → hybrid dispatch shape) and the auto-002 R1 → R2 transition (full sub-track → smoke-test variant) both materially shifted the decision based on findings the inline-simulated reviewers had missed.

## Decision

Autonomous-mode decision briefs follow the `auto-NNN` filename convention with Round 1 (lead-agent best call with implementation framing) + ≥2 real adversarial subagent reviewers + Round 2 (revised brief) in a single file with Round 1 preserved struck-through for traceability.

## Alternatives considered

- **Single-round brief (no adversarial review).** Cheaper. Rejected because the AGENTS.md rule already requires real-subagent review for any lead-agent-authored decision artifact; this ADR codifies the lifecycle the rule implies.
- **Two-file format (Round 1 + Round 2 as separate files).** Cleaner separation. Rejected because the single-file format makes the audit trail (Round 1 anchoring → reviewer findings → Round 2 revision) navigable in one read; the strikethrough convention is the audit trail discipline.
- **Multi-round (Round 1 → reviewers → Round 2 → reviewers → Round 3).** More thorough. Rejected as default because empirically Round 2 has been sufficient in 4/4 cases; multi-round would cost without clear benefit. Reserved as an option for high-stakes briefs where Round 2 surfaces a major new question.
- **Inline-simulated reviewers (the deprecated pattern).** Already forbidden by AGENTS.md. The deprecation is what this lifecycle replaces.

## Consequences

- Every autonomous-mode decision brief in this repo follows a known shape, making them mutually navigable and audit-trail-consistent.
- Round 1 is no longer the "final" form — the lead agent must accept that Round 1 may be substantially rewritten. The "preserved for traceability" discipline removes the temptation to delete-and-rewrite.
- Cost: ≥2 real subagent dispatches per brief. At ~60 seconds per reviewer for typical adversarial review, plus lead-agent time to synthesize findings into Round 2, ~5-10 minutes added per brief. The empirical value (auto-001 R2's shape change; auto-002 R2's smoke-test substitution; auto-003 R2's counter-proposal adoption) substantially exceeds this cost.
- Briefs that need to ship a Round 1 quickly (e.g., to authorize concurrent work) can do so; the Round-2 honest-acknowledgements section (separate proposed ADR / rule) covers the case where Round-1-authorized work fires pre-Round-2.

## References

- [`../2026-05-25-155.md`](../2026-05-25-155.md) — the source retrospective.
- [`./SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md`](./SKILL-SPEC-34dd1d0274-decision-brief-adversarial-review-lifecycle.md) — the skill spec for executing this lifecycle.
- [`./AGENTS-MD-8a7029647f-adversarial-review-verdict-tiers.md`](./AGENTS-MD-8a7029647f-adversarial-review-verdict-tiers.md) — required 3-tier verdict schema.
- [`./AGENTS-MD-bb7fe2c5aa-round-1-strikethrough-preservation.md`](./AGENTS-MD-bb7fe2c5aa-round-1-strikethrough-preservation.md) — the strikethrough preservation rule.
- [`./AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md`](./AGENTS-MD-ffe35aa500-honest-acknowledgements-pre-round-2-firing.md) — honest-acknowledgements rule for wave firing.
- Existing briefs: [`../../architectures/v3/decisions/auto-001-phase-3.5-dispatch-shape.md`](../../architectures/v3/decisions/auto-001-phase-3.5-dispatch-shape.md), [`auto-002-ub-path.md`](../../architectures/v3/decisions/auto-002-ub-path.md), [`auto-003-bfl-rg-view-choice.md`](../../architectures/v3/decisions/auto-003-bfl-rg-view-choice.md), [`auto-004-phase-4-dispatch-shape.md`](../../architectures/v3/decisions/auto-004-phase-4-dispatch-shape.md).
- PRs the decision was repeatedly applied in: #146, #147, #149, #150, #152, #154, #155.
