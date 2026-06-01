# agent instruction

**Run a cross-component seam adversary after a parallel uniform-schema fan-out.** Per-deliverable review is not enough when parallel subagents author interdependent components: even subagents that verbatim-cite the same binding decision drift on the wire types at their shared boundary. After the fan-out, dispatch one adversary whose sole job is pairwise seam consistency (field names, wire types, who-guarantees-what) before integrating.

*Grounded in: parallel Sweep-2 builders for C23 and C41 both cited the same D-5 boundary yet produced EventId{stream,seq} vs bare uint64 at the chain seam — a HIGH build-breaker only the seam adversary caught.*

# justification

The existing verbatim-text-pull rule prevents *paraphrase* drift when parallel subagents cite a shared decision — but it does not prevent *type* drift. In this run the C23 and C41 builders both quoted the same D-5 boundary verbatim and still disagreed on the wire type at the exact seam they quoted: C23 emitted a `{stream, seq}` struct, C41 consumed a bare integer. Per-component adversary review reads one spec at a time and is structurally blind to a mismatch that exists only *between* two specs — every per-component check passed, and the drift reached the working tree. One additional adversary, reading just the interface sections of the whole cluster and checking pairwise consistency, caught a HIGH build-breaker (plus three lesser drifts) at authoring time, when a field-rename fixes it — versus implementation time, when it breaks the build contract. The marginal cost is one dispatch per cluster.
