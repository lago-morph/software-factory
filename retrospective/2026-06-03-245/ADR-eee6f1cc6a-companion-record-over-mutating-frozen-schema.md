# ADR: Companion record over mutating a downstream-frozen schema

- **ID**: ADR-eee6f1cc6a
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-03
- **Source retrospective**: ../2026-06-03-245.md
- **PRs covered**: #245

## Context

The spec-scenarios-system triangle work (ADR-0069 / D-42) required the judge component (C32) to emit a new per-build output — a diagnosis carrying root-cause attribution, repair recommendation, and the tri-alignment verdict. But C32 already owned a record, `ScoreRecord`, that had been **frozen by D-39** in a prior Sweep-2 run with three named downstream consumers (C33 aggregates it, C34 audits it, C46 reads it for the judge-FP rate). The implementation plan (HANDOFF §0★.2.1) explicitly offered two ways to add the diagnosis: (a) add it as additive optional fields on `ScoreRecord` with a bead-type version bump, or (b) emit a separate companion record keyed to the `ScoreRecord`. The choice mattered because a self-building factory's contracts are consumed by independently-authored components, and a freeze is the thing that lets those consumers be built in parallel without re-checking each other on every change.

## Decision

When a frozen cross-component schema needs new fields and downstream consumers depend on that freeze, extend it by adding a companion record keyed to the frozen record rather than mutating the frozen record in place. (Realized this session as D-43: the `DiagnosisRecord` is a companion to the untouched D-39 `ScoreRecord`, keyed by `score_record_refs` + `factory_build_ref`.)

## Alternatives considered

- **Additive optional fields on the frozen record + a bead-type version bump.** Rejected for this case: even additive-optional changes force every consumer (C33/C34/C46) to re-validate that the bump didn't disturb their reads, re-touch the frozen artifact, and reason about two versions of one type; and the diagnosis has a *different cardinality* from the score (one diagnosis per build vs one score per scenario-trajectory), so folding it into the per-scenario record would have been a semantic mismatch as well as a freeze violation. Additive fields remain the right call when the new data shares the existing record's cardinality and no hard freeze is in force.
- **Mutating the frozen record in place (rename/restructure).** Rejected outright — it breaks the D-39 freeze and every consumer built against it; the freeze exists precisely to make that impossible without a new binding decision.
- **A free-standing record with no key back to the score.** Rejected: the diagnosis must be auditable against the exact H↔I evidence it was computed over, so it carries explicit references (`score_record_refs`) back to the scores rather than floating independently.

## Consequences

Easier: the D-39 freeze is preserved verbatim, so C33/C34/C46 keep consuming `ScoreRecord` with zero changes (the seam adversary confirmed zero drift on it); the new record can have its own cardinality, owner, and freeze (`DiagnosisRecord` is one-per-build, owned and frozen by C32); and the two concerns stay separable for future evolution. Harder / accepted trade-off: there are now two records to register, persist, and audit instead of one (the C22 registration + a C20 `diagnosis_bead_ref` slot became tracked follow-ups), and consumers that want both score and diagnosis must join them by key rather than reading one row. The standing rule this encodes: a freeze is a load-bearing contract, and the default way to grow a frozen schema is a keyed companion, not a mutation.

## References

- [`../2026-06-03-245.md`](../2026-06-03-245.md) — the source retrospective.
- [`./SKILL-SPEC-288fe4b337-contract-first-cross-component-fanout.md`](./SKILL-SPEC-288fe4b337-contract-first-cross-component-fanout.md) — the orchestration recipe that ships this kind of contract decision.
- `architectures/v4/_meta/review-log.md` — D-39 (the `ScoreRecord` freeze) and D-43 (the companion `DiagnosisRecord` decision this ADR generalizes).
- `docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md` — the invariant whose implementation surfaced the choice.
- PRs the decision was made in: #245.
