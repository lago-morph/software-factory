# ADR: Integrate CXDB via raw-API-bodies bridge, not OTLP

- **ID**: ADR-d566506f19
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

v4 uses CXDB (StrongDM's content-addressed DAG event store) as the trajectory substrate for principles 10, 11, and 12 (memory layer, self-healing loop, self-optimization). The question is how to get Claude Code's emitted events into CXDB.

A research subagent investigated CXDB's ingestion model. Key findings (documented in `architectures/v4/AI-CONTEXT.md` §5):
- CXDB exposes two ingestion protocols: msgpack on port 9009 (high-throughput) and HTTP/JSON on port 9010 (general).
- **CXDB has no native OTLP receiver.** StrongDM explicitly positions CXDB *against* OTel: "Built for distributed tracing. Spans model request trees, not conversations." The unit of storage in CXDB is a "turn," not a span — turns form a DAG with parent pointers, payloads are content-addressed via BLAKE3.

Claude Code emits three streams of data that could feed CXDB:
1. **OTLP traces** via `CLAUDE_CODE_ENABLE_TELEMETRY=1` env vars — span-shaped data
2. **Raw API bodies** via `OTEL_LOG_RAW_API_BODIES=file:<dir>` — conversation-shaped JSON files dumped to disk
3. **Session JSONL logs** — Claude Code's per-session log format, similar to (2) but per-session

Three bridge options, ranked by impedance:

| Path | Impedance | Why |
|---|---|---|
| Gas City event bus JSONL → CXDB | Lowest | Events already attributed and trajectory-shaped |
| Claude Code raw API bodies → CXDB | Low | Conversation-shaped already; parent-chain via `session.id` |
| Claude Code OTLP → CXDB | Highest | Span tree → turn DAG mapping is what CXDB was designed against |

## Decision

Bridge Claude Code into CXDB via the raw-API-bodies escape hatch (`OTEL_LOG_RAW_API_BODIES=file:<dir>`) and a small standalone tool-node binary that posts to CXDB HTTP API on port 9010; do not use the OTLP path because CXDB was explicitly designed against the OTel span-tree model.

## Alternatives considered

- **OTLP → CXDB via translator service.** Rejected because span-tree-to-turn-DAG translation requires inventing the parent-turn mapping logic, which is exactly the modeling problem CXDB chose to avoid. The translator would be the impedance mismatch made concrete.
- **Gas City event bus → CXDB.** This is the lowest-impedance option but addresses a different scope — Gas City events are already attributed and trajectory-shaped, so they map cleanly. We use this path *too*, as a complement to the raw API bodies path. Both bridges can feed the same CXDB instance; they capture different layers (Gas City events = orchestration; raw API bodies = the actual model interactions).
- **Skip CXDB entirely; use Gas City's event bus alone.** Considered for Phase 0 simplicity. Rejected for Phase 1 because principle 10 (memory layer) is materially stronger with content-addressed trajectory storage, and principle 11 (self-healing) anomaly clustering benefits from BLAKE3 dedup at scale.
- **Send Claude Code OTLP to LangFuse only, no CXDB.** LangFuse handles principles 9 + 10 partially via its event storage but isn't content-addressed. Use both: LangFuse for trace browsing UI, CXDB for the durable content-addressed trajectory substrate. They're complementary.

## Consequences

What becomes easier:
- The raw-API-bodies dump is conversation-shaped, matching CXDB's turn model directly. Bridge is a standalone tool-node binary, ~few hundred lines of Go. Pattern transfusion from Gas City's `internal/sessionlog` (which parses Claude Code JSONL similarly).
- CXDB's content-addressing gives us free dedup (long repeated payloads stored once) and tamper-evidence on payload references.
- O(1) trajectory branching becomes available for counterfactual replay (used at Layer 6 self-optimization).
- The bridge ships as a Gas City pack — standalone binary called as a tool node, no Go imports of CXDB or Gas City code required.

What becomes harder:
- Two ingestion paths feeding CXDB (raw API bodies + Gas City event bus) means careful schema design to distinguish "this turn came from a Claude Code session" vs "this event came from Gas City orchestration." Type registry handles this via bundle IDs (`claude_code_v1` vs `gas_city_v1`).
- Raw API bodies path means writing to disk first, then bridging. Disk I/O adds latency vs. direct in-memory ingestion. Acceptable for v4 because the raw bodies path is already the supported Claude Code escape hatch.

Trade-off accepted: two ingestion paths with type-registry discipline in exchange for clean impedance-matched bridges.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-0aa07c7b72-gas-city-runtime-baseline.md`](./ADR-0aa07c7b72-gas-city-runtime-baseline.md) — Gas City baseline.
- `architectures/v4/README.md` Part 6 Phase 1 (PR #209) — Phase 1 build steps include this bridge.
- `architectures/v4/AI-CONTEXT.md` §5 (PR #209) — CXDB details, three bridge paths.
- `reference-only/d93e59de67/factory.strongdm.ai__products__cxdb.html` — CXDB product page.
- PRs the decision was made in: #209.
