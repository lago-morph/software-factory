# agent instruction

**Deferred-work binding-artifact triple.** When an autonomous run defers in-scope work to a successor run, the deferral MUST appear as a binding constraint in all THREE of: (a) the session handoff doc (`SESSION-HANDOFF-*-close.md`), (b) the morning summary's "what I deliberately did NOT do" section, and (c) the next-run dispatch prompt (or its absence flagged as a follow-up). Divergence among the three is a process bug — pick one source of truth and propagate to the others before run-close.

*Grounded in: 2026-05-25 Wave 5.3 deferral — all three Round-2 adversarial reviewers raised the "binding artifact" concern from different angles (pre-mortem, governance, naive newcomer).*

# justification

In auto-005 Round 1 of the 2026-05-25 run, the cost-hawk reviewer correctly argued Phase 5 needed to split across two runs (PR-cap pressure). The Round-1 brief simply said "Wave 5.3 deferred to a subsequent run" — informal. Three Round-2 reviewers independently surfaced the same failure mode: an informal deferral dissolves at run boundary. The pre-mortemer asked "what if the next run never happens?"; the regulator/governance reviewer asked "what artifact is the binding commitment?"; the naive-newcomer asked "where does the next run's dispatch prompt live?". All three converged on the binding-artifact-triple amendment.

Without the rule, deferred work disappears across run boundaries with high probability — different agent, different scope, different priorities. The 2026-05-25 morning summary explicitly flagged the next-run dispatch prompt as not-yet-authored, but the rule applied: the handoff doc carries the Wave-5.3 scope + Phase-6 gate, the morning summary names the deferral in "what I deliberately did NOT do," and the missing dispatch prompt is a follow-up flag (a defensible partial state).

Marginal cost of the rule: triple-write of ~5 sentences. Asymmetric cost without: deferred work silently disappears; downstream phases break when they assume the deferred work landed; runs after the deferral repeat work or skip work without realizing.
