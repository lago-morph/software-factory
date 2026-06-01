# ADR: Seam-consistency adversary pass after parallel uniform-schema fan-out

- **ID**: ADR-6697a87c16
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-01
- **Source retrospective**: ../2026-06-01-233.md
- **PRs covered**: #232

## Context

In this run, five interdependent components (C19/C20/C21/C23/C41) were deepened to implementation depth by parallel subagent builders, each briefed with a vetted exemplar and instructed to cite its binding cross-component decisions **verbatim** (per the existing `AGENTS-MD-bf4431be57` text-pull rule). That discipline prevented *paraphrase* drift — but did not prevent *type* drift at the shared boundary. The C23 builder produced `EventId = {stream, seq}` while the C41 builder consumed a bare `uint64` at the very D-5 chain seam both had quoted verbatim. Each builder filled an under-specified field type locally, and per-component review (which reads one spec at a time) cannot see a mismatch that only exists *between* two specs. A dedicated cross-component seam adversary — reading only the §3/§4 interface sections of all five specs and checking pairwise consistency — caught it as a HIGH build-breaker, alongside three lower-severity drifts (field-name, payload ownership, wire-type placeholder). This is the panel's "integration tax" risk (R4) realized at the cluster level.

## Decision

After any parallel fan-out where subagents author a uniform-schema deliverable with shared cross-component contracts, run a dedicated cross-component seam-consistency adversary before integrating, in addition to per-deliverable review.

## Alternatives considered

- **Rely on per-component adversary review only** (status quo before this run). Rejected: a per-component reviewer sees one spec; a between-spec type mismatch is structurally invisible to it. The drift here reached the working tree precisely because every per-component check passed.
- **Rely on verbatim binding-decision citation alone.** Rejected: the builders *did* cite D-5 verbatim and still drifted on the un-specified field type — verbatim citation fixes paraphrase drift, not type-resolution drift.
- **A full integrator that rewrites all seams.** Rejected as heavier than needed; the cheaper, higher-signal move is one adversary that *finds* the drift, after which the lead resolves each conflict through the decision ledger (D-26…D-29) and a single targeted integrator pass.

## Consequences

- **Easier:** cross-component contract mismatches are caught at authoring time (cheap) rather than at implementation time (expensive); the seam adversary's findings feed straight into the cross-component decision ledger.
- **Harder / cost:** one extra adversary dispatch per cluster, plus a fix-integration pass when drift is found. Acceptable: in this run it converted a HIGH build-breaker into four ledger decisions resolved in one wave.
- **Trade-off accepted:** the seam adversary needs the cluster's interface sections in one context, which bounds cluster size to what one reviewer can hold (~5–8 specs).

## References

- [`../2026-06-01-233.md`](../2026-06-01-233.md) — the source retrospective (Phase 4).
- [`./SKILL-SPEC-fe12e3af25-empirical-external-fact-verification.md`](./SKILL-SPEC-fe12e3af25-empirical-external-fact-verification.md) — sibling verification-discipline spec.
- Cross-component ledger decisions D-26…D-29 in `architectures/v4/_meta/review-log.md`.
- PR the decision was exercised in: #232.
