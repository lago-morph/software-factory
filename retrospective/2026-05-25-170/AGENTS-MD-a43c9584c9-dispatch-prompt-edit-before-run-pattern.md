# agent instruction

**Dispatch-prompt edit-before-run pattern.** When the user surfaces a quality concern about a dispatch prompt for an upcoming autonomous run, commit the modification to the prompt file in its own PR BEFORE kicking off the run — do not fold the modification into the run's first work-PR. The edit is then mechanically auditable (the run's scope envelope can cite the prompt at a stable commit) and the run benefits from the improvement.

*Grounded in: 2026-05-25 PR #158 added the Phase-A verification step to `next-agent-prompt-phase-5.md` before the run started; the verification caught the registry-TL;DR concern in PR A5.*

# justification

The 2026-05-25 session opened with the user asking for a verification subagent step to be added to the end of Phase A in the dispatch prompt. The lead agent committed the modification in PR #158 (a tiny standalone PR), the user merged it, and only then did the autonomous run kick off with "Do both A and B." The pre-run merge meant the scope envelope in PR A0 could cite the dispatch prompt at a stable commit, and the verification step that PR #158 added caught a real quality issue in PR A5 (the candidate-registry TL;DR's conclusion-restating line).

The counterfactual: if the lead agent had folded the modification into the first work-PR (PR A0 or PR A1), the dispatch prompt's improvement would be entangled with first-phase work — harder to audit, harder to revert without disturbing the run, harder to cite as "the prompt the run executed." More importantly, if the user had asked for the modification but the lead agent had ignored it and proceeded straight to the run, the verification step would not have existed, and the registry-TL;DR concern would have shipped to main.

Marginal cost of the rule: one extra small PR per dispatch-prompt modification request (~5 minutes). Asymmetric cost without: a quality improvement requested at run-start gets ignored, deferred, or muddled into other work; the run misses the improvement entirely.
