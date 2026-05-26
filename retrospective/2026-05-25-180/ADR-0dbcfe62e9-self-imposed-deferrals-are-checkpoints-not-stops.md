# ADR: Self-imposed deferrals are checkpoints, not stops

- **ID**: ADR-0dbcfe62e9
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-25
- **Source retrospective**: ../2026-05-25-180.md
- **PRs covered**: #165, #173, #174, #175, #176, #177

## Context

Decision briefs sometimes establish deferrals to manage perceived constraint risk — e.g., the 2026-05-25 `auto-005` Round 2 decision deferred Wave 5.3 to a successor run, citing the cost-hawk reviewer's estimate of ~20 PRs against the 30-PR cap with 10 PRs of margin. The deferral was treated as binding by the lead agent and was honored mechanically.

At the time the deferral would have fired (after Phase-5a closed with the morning summary + retrospective), the actual PR count was 13. The cited constraint (PR-cap pressure) was not actually binding. Continuing in-session was feasible and the user explicitly surfaced this as: "I am very confused why you did not continue to phase 5b. Please tell me your logic." The lead agent's logic trace conceded the over-conservatism, lifted the deferral, and delivered Wave 5.3 in the same run (PRs #173-177, ~17 total PRs against the 30 cap, 13 PRs of margin).

The failure pattern: a decision-brief deferral was honored as a stop-signal rather than re-validated against actual constraints at the deferral checkpoint.

## Decision

**Decision-brief deferrals are checkpoints to re-validate against actual constraints, not unconditional stops. When the constraint cited in the deferral is not binding at the time the deferral would fire, lift the deferral and continue.** The re-validation is a mechanical 5-second check (e.g., `gh pr list | wc -l` against the cap). If the original constraint is still binding, honor the deferral. If not, continue and document the lift in the morning summary's "what I deliberately did NOT do — exceptions" section.

## Alternatives considered

- **Treat deferrals as unconditional stops.** Rejected because the failure pattern is exactly this rule — the lead agent honored the deferral mechanically and the user had to round-trip to surface the over-conservatism. The autonomous-run skill's "prefer reversible action" working-mode rule conflicts with treating deferrals as unconditional.
- **Re-write decision briefs to express deferrals as conditional (instead of relying on a post-hoc rule).** Rejected because decision briefs reflect the constraints visible AT brief-writing time; the constraint at deferral-fire time is what matters and is by definition not knowable at brief-write time.
- **Always continue past deferrals unless the user explicitly confirms.** Rejected because that defeats the value of decision briefs entirely — a brief whose deferrals can be ignored at will is just a recommendation, not a decision.

## Consequences

**Easier:** Autonomous runs don't get artificially throttled by stale constraint estimates. The "do both A and B" delegation actually delivers both when feasible. Wave-5.3-style situations (deferral cited budget pressure that didn't materialize) lift cleanly.

**Harder:** The lead agent must remember to run the re-validation check at every deferral fire-point, not just at brief-write time. The morning summary's "what I deliberately did NOT do" section gains an "exceptions where the deferral was lifted" sub-section for honesty.

**Trade-off accepted:** A slight discipline tax at every deferral checkpoint in exchange for not artificially throttling autonomous runs when actual constraints don't bind.

**Explicitly NOT promising:** the rule doesn't override hard constraints. If the deferral cited "no Wave 5.3 because Phase 6 spec must be authored first" (a structural constraint), the re-validation would still confirm that's binding. The rule only lifts deferrals whose cited constraints aren't actually binding at fire-time.

## References

- [`../2026-05-25-180.md`](../2026-05-25-180.md) — source retrospective.
- [`./AGENTS-MD-cb08b5a7f3-self-imposed-deferrals-re-validate-before-honoring.md`](./AGENTS-MD-cb08b5a7f3-self-imposed-deferrals-re-validate-before-honoring.md) — per-rule agents-file addition.
- PR #169 thread, line 105 ("I am very confused why you did not continue to phase 5b") — the user-surfaced symptom.
- PRs #173–177 — the Wave 5.3 delivery that lifted the deferral.
