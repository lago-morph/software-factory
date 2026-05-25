# agent instruction

**Save-then-dispatch for parallel subagent waves of ten or more.** When dispatching N≥10 subagents in parallel for results that each return ~1000-1500 words, batch in waves of 6-12 and write completed outputs to disk before dispatching the next wave. Accumulating 20+ subagent outputs in context is heavy and pushes the working window. The save-then-dispatch pattern keeps the conversation tractable.

*Grounded in: 24-subagent dispatch was run in two waves with disk-writes + commit between waves.*

# justification

The Phase-3.2/3.3 dispatch was 24 subagents. If dispatched as one wave with results accumulating in context, the working window would have been pushed close to its limit before any synthesis work could happen. The wave-then-save pattern (12 subagents, save outputs to disk, commit, then 12 more) kept the conversation tractable. Each wave's outputs landed asynchronously over ~3 hours; saving as they completed prevented the "all 24 outputs in context at once" overload. Cost: ~10 minutes of file-writing per wave. Benefit: the dispatch was feasible at all — without the pattern, the orchestrating session would have run out of working memory mid-dispatch.
