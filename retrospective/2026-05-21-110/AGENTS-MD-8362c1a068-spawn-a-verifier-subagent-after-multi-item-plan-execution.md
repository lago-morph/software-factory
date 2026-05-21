# agent instruction

**Spawn a verifier subagent after multi-item plan execution.** After completing any plan document with five or more numbered items (cleanup plans, refactor checklists, multi-step migrations), dispatch a fresh-context verifier subagent BEFORE opening the PR. Brief it to verify every numbered item against the actual repo state and to report findings in three buckets — `PASS`, `FACTUAL ERROR` (must fix), `MAJOR FINDING` (must fix) — ending with `VERDICT: CLEAN` or `VERDICT: NEEDS FIXES`. Loop on fixes until the verdict is CLEAN.

*Grounded in: PR #110 cleanup-plan execution where the verifier confirmed 50+ specific items in a single pass.*

# justification

The cleanup-plan-revised.md execution touched 13 files across 5 file types (PLAN.md, research-plan.md, README, two skill resource docs, the catalog JSON, MIGRATION-EXCEPTIONS.md, etc.) with 52 numbered items plus L.1–L.6 plus N1–N6. Self-auditing that against the plan document is bias-prone: the implementer already has a story about what they did, and confirmation bias makes them stop checking when the story sounds right. A fresh-context subagent reads the plan and the repo state without the implementer's narrative, so it catches the items where "I'm pretty sure I did that" was wrong.

The structured PASS / FACTUAL ERROR / MAJOR FINDING / VERDICT contract is what makes the result actionable: the implementer doesn't have to interpret prose findings, and the VERDICT line is a clean terminating condition for the fix-loop. The marginal cost is one subagent dispatch (~3–8 minutes) and the upside is catching the bug that would have produced review churn or a follow-up PR. The asymmetry is heavily in favor of always running it.
