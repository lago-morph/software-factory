# ADR: LangFuse over Phoenix for Layer 3 observability

- **ID**: ADR-3c01baa97e
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-29
- **Source retrospective**: ../2026-05-29-211.md
- **PRs covered**: #209

## Context

v4's Layer 3 implements principle 8 ("why am I doing this?") and the observability foundation for principle 11 (self-healing loop). The OSS landscape for LLM observability includes:

- **LangFuse** — Apache 2.0, self-hostable, full LLM observability stack (traces, sessions, scoring, prompt management). Strong on session/conversation threading.
- **Phoenix (Arize)** — **Elastic License**, designed around OpenInference standard. Built-in evaluation features.
- **Helicone** — Apache 2.0, lighter-weight LLM observability.
- **OpenLLMetry** — Apache 2.0, instrumentation conventions on top of OpenTelemetry.
- **Generic OpenTelemetry Collector** — Apache 2.0, language-agnostic event collection.

The license hygiene step in v4 README's Part 5 caught Phoenix's Elastic License as a concern. The Elastic License restricts hosted-service operation: organizations cannot offer Phoenix as a managed service. For v4, this is a real constraint because part of v4's value proposition is the factory could itself be operated as a service (or its outputs hosted as services downstream). LangFuse, in contrast, is Apache 2.0 — clean for any operational shape including hosted services.

The functional surface of LangFuse covers what v4 needs at Phase 1: trace browsing UI, session/conversation management, prompt-version tracking. Self-hostable means no external service dependency.

## Decision

Use LangFuse (Apache 2.0) self-hosted as the Layer 3 trace browsing and session management component rather than Phoenix (Arize, Elastic License) because the Elastic License is restrictive on hosted services and would prevent operating the factory as a service downstream.

## Alternatives considered

- **Phoenix (Arize) as default.** Rejected because Elastic License is restrictive on hosted services. Phoenix's built-in evaluation features are valuable but not load-bearing — Layer 2 (Inspect AI) handles evaluation; Layer 3 only needs storage + browsing.
- **Helicone as default.** Considered as Apache 2.0 alternative. Phoenix and Helicone are roughly comparable on raw capability; LangFuse wins on session/conversation threading specifically, which matters for v4's bead model.
- **OpenLLMetry + Generic OTel Collector + Jaeger/Tempo.** Considered as a more generic stack. Rejected because the LLM-specific conventions in LangFuse (prompt versions, sessions, scores) deliver immediate value without us inventing them on top of generic tracing.
- **Skip dedicated LLM observability for Phase 1; use Gas City event bus + ad-hoc tooling.** Rejected because the trace browsing UI is materially useful during Phase 1 development, and the absence of session/conversation threading would make debugging harder.

## Consequences

What becomes easier:
- LangFuse self-hosted via Docker Compose or Kubernetes — straightforward install.
- Apache 2.0 license is clean for any operational shape including hosted services.
- Session/conversation threading maps to Claude Code's `session.id` correlation attribute.
- OpenTelemetry Collector can route Claude Code OTLP output to LangFuse directly.

What becomes harder:
- LangFuse storage is Postgres-backed, not content-addressed. v4 needs CXDB *in addition* for principle 10's content-addressed substrate (see [`ADR-d566506f19`](./ADR-d566506f19-cxdb-bridge-path.md)). The two systems are complementary: LangFuse for trace browsing UI, CXDB for durable content-addressed trajectory storage.
- LangFuse + CXDB means more moving parts in the Phase 1 stack. Acceptable because both serve distinct purposes.
- If LangFuse pivots toward a restrictive license in future versions, we'd need to migrate. The OSS forks-available rule applies (Apache 2.0 forking is permitted) but migration is non-trivial.

Trade-off accepted: somewhat more moving parts (LangFuse + CXDB) in exchange for clean license posture allowing hosted-service operation.

## References

- [`../2026-05-29-211.md`](../2026-05-29-211.md) — source retrospective.
- [`./ADR-d566506f19-cxdb-bridge-path.md`](./ADR-d566506f19-cxdb-bridge-path.md) — CXDB as complement (content-addressed substrate).
- `architectures/v4/README.md` Part 5 (license hygiene table) — where Phoenix's Elastic License is flagged.
- `architectures/v4/AI-CONTEXT.md` §10.2 (license-clean alternatives chosen) — explicit pick rationale.
- `github.com/langfuse/langfuse` — LangFuse repo.
- PRs the decision was made in: #209.
