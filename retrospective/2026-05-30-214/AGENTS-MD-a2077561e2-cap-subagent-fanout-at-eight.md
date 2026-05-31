# agent instruction

**Cap subagent fan-out at roughly eight concurrent.** "When dispatching parallel subagents, launch in waves of no more than ~8; beyond that the platform rate-limits and silently drops the surplus. Pipeline the work: let in-flight agents drain to ~2, then dispatch the next chunk."

*Grounded in: a 24-agent launch where 16 were rate-limited to zero output.*

# justification

A single dispatch of 24 subagents in this session returned 8 successful background launches and 16 `API Error: Server is temporarily limiting requests` failures — each of those 16 burned a few tool-uses and produced zero output, and re-dispatching them was pure waste. The user had explicitly asked for "50+ concurrent," so discovering the real ceiling experimentally cost a whole wave. The marginal cost of the rule is trivial: dispatch in chunks of 6–8 and refill as agents finish, which also keeps the orchestrator's receipt-processing load steady. Encoding "~8, pipelined" up front turns a hard infrastructure limit from a surprise into a planning constant, and a wave that would have half-failed instead runs clean.
