# agent instruction

**Handoff plan discipline.** When writing a plan for a fresh-context next session, run these checks before committing: (1) does the plan name forbidden artifacts (contaminated files, deprecated approaches, things the next agent should not read) in its startup-reading sections? Move those references into the specific step that uses them, or relocate the artifacts via the permalink-with-guard pattern. (2) Does the plan contain tasks already done? Remove them — the next agent only needs pending work. (3) Does the plan stop-and-ask at every step? Prune to major decision points only. (4) Does the plan have an explicit pointer to where the next session continues when this plan completes? If no, add one — don't strand the master plan.

*Grounded in: the PHASE-2-RERUN-PLAN.md handoff went through five rounds of PR-comment-driven fixes before all four checks passed.*

# justification

The plan went through PR comments at lines 13, 34, 36, plus a research/PLAN.md banner critique, plus an AGENTS.md over-cautious critique, plus two bugs (chain break after Phase 2 + done-tasks clutter) caught only at the final pass. Each round trimmed verbosity, moved references, removed forbidden-fruit pointers, or fixed bugs that come from writing the plan without an explicit review pass. The marginal cost of running these four checks before pushing a handoff plan is small — maybe five minutes per plan. The cost of not running them is a multi-round PR-comment loop that burns user attention and produces frustrated feedback. The asymmetry is roughly 5 minutes vs. an hour of round-trips. The four checks aren't novel — each came directly from a specific PR comment in this session — but capturing them as a discipline prevents the next handoff from rediscovering them one at a time.
