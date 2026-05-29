# agent instruction

**Async subagents for long-running research.** "For research questions expected to take more than a few minutes (multi-source web research, deep repo inspection, multi-project surveys), dispatch the subagent as async background work (run_in_background=true) so main work can continue. Continue the conversation with the user on related topics until the notification arrives. Do not block on long subagent calls when the user is engaged."

*Grounded in: layer 2-6 coverage survey for v4 (dispatched async during the gene-transfusion conversation, completed while we discussed the broader picture; results integrated into v4 design without losing momentum).*

# justification

When the user is engaged in a substantive conversation, blocking on a 5-minute subagent kills momentum. The async dispatch pattern let the layer 2-6 coverage survey run in parallel with the gene-transfusion discussion; results integrated into v4 design when they arrived. The marginal cost of async is one `run_in_background=true` parameter; the gain is no conversational dead air on long research. Note the discipline that pairs with async: continue with related work, not unrelated work, so the research findings can be folded back coherently when they return. Async without discipline = parallel threads of conversation that don't reconnect.
