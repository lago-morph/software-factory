# ADR: Decision-consequence pre-commitment as a rubric, not a pre-bound outcome enum

- **ID**: ADR-0305f34813
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-01
- **Source retrospective**: ../2026-06-01-233.md
- **PRs covered**: #231

## Context

The auto-001 brief had to pre-commit the consequence of a not-yet-run empirical spike (does `gc` prevent or merely detect an out-of-partition access). The Round-1 draft pre-bound a fixed enumeration of outcome→consequence rows (PREVENT / DETECT-ONLY / SILENT / MIXED → specific actions). Round-2 adversaries (methodology-purist + falsification) showed this was self-defeating in two ways: (1) it **decided findings the spike exists to produce** — pre-binding "SILENT ⇒ worse" and "MIXED ⇒ block" is answer-before-evidence, the exact anti-pattern the project's buildability-first thesis warns against; and (2) the 4-cell enum is **invented altitude** — real enforcement is a spectrum (path-glob, symlink-race, partial-namespace) and plausible results map to no cell, while the case "spike cannot be run" had no bound consequence at all. The fix was to bind the *decision criterion* (a rubric the operator applies to whatever the findings are) rather than a pre-enumerated branch table, and to fail closed on inconclusive/unrunnable.

## Decision

When pre-committing the consequence of a not-yet-gathered empirical result, bind the decision criterion as a rubric the operator applies to findings rather than a fixed enumeration of outcome-to-consequence rows, and fail closed on an inconclusive or unrunnable result.

## Alternatives considered

- **Pre-bound outcome enum** (the Round-1 form). Rejected: pre-decides the spike's findings (answer-before-evidence), invents a discrete taxonomy over a spectrum, and leaves between-cell and not-run results unbound.
- **Defer the consequence entirely until the spike runs.** Rejected: the operator explicitly wanted the consequence pre-committed so it is not re-litigated under schedule pressure; a rubric satisfies that without pre-deciding findings.
- **Bind only the happy path** (PREVENT ⇒ proceed). Rejected: leaves the dangerous and the inconclusive cases unbound — the falsification reviewer showed "couldn't run it" would then be read as "not-yet-bad" and waved through.

## Consequences

- **Easier:** the decision survives a spectrum of real results and an unrunnable spike (fail-closed) without re-litigation; it respects buildability-first (gather evidence, then apply the criterion).
- **Harder / cost:** a rubric is less mechanically checkable than a lookup table — it requires the operator to apply judgment to findings. Mitigated by also giving *illustrative* (non-exhaustive) example rows.
- **Trade-off accepted:** slightly more interpretive load at decision time in exchange for not baking in a wrong taxonomy or a pre-decided finding.

## References

- [`../2026-06-01-233.md`](../2026-06-01-233.md) — source retrospective (Phase 3).
- [`../../architectures/v4/_meta/decisions/auto-001-detect-only-binding-gate.md`](../../architectures/v4/_meta/decisions/auto-001-detect-only-binding-gate.md) — the brief this generalizes from.
- PR the decision was made in: #231.
