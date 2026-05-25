# agent instruction

**Verbatim text-pull when citing binding rule tables.** When a subagent or per-candidate summary cites a binding rule with a per-row application table (e.g., the Phase-3.5.5 RG-primitive rule's "Application to current candidates" table), the citation MUST be a verbatim quoted text-pull of the applicable row, not a paraphrase. Paraphrase drift across parallel subagents handling the same rule is silent and only surfaces at lead-agent aggregation.

*Grounded in: Wave 4.1 dispatch — auto-004 Round 2 added required text-pulls for §2 of substrate-requirements summaries after the aggregation-cost auditor flagged drift risk across BF-L / U-B / D7-U-1 parallel handling of the Phase-3.5.5 rule.*

# justification

A binding rule with a per-row application table is the closest thing the synthesis pipeline has to a contract surface. When three parallel subagents (BF-L, U-B, D7-U-1) each handle their applicable row, paraphrase drift is silent — each subagent renders "the rule says about my case" in their own words, and the words disagree in subtle ways (e.g., one says "may opt-in to bounded sub-track", another says "must commit to bounded sub-track", a third drops the per-portion-application caveat). The drift only surfaces when the lead agent aggregates the three summaries at Wave 4.2, at which point reconciliation requires re-reading the rule and patching three files. The verbatim text-pull rule eliminates the drift entirely: each subagent quotes their row, the quote either matches or doesn't, and the lead-agent aggregation is a yes/no consistency check rather than a meaning-reconciliation pass. The marginal cost of pulling a verbatim row is one tool call; the cost of unpatched drift is two passes through the per-candidate summaries.
