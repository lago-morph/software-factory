# ADR 0021: Discipline — holdout

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2 parallel fanout)

## Context

Holdout-partition appears as a `accepted` or `accepted-and-expanded` D-4 default across all 10 tracks' substrate-requirements summaries; the [disciplines index](../../architectures/v3/disciplines/index.md) names holdout as one of 21 canonical disciplines, and the per-discipline write-up at [`disciplines/holdout.md`](../../architectures/v3/disciplines/holdout.md) frames the contract as *unseen-by-builder*, not *out-of-tree* (the D-2 brownfield challenge inverts scenario-location without weakening the holdout requirement).

The forcing failure mode is [F28 (holdout leakage / acceptance criteria seen by builders)](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders), rated `critical` for greenfield (the judge is the *only* ground-truth signal — leakage short-circuits the entire lights-out loop) and `high` for brownfield (production behavior provides partial compensation). Absent substrate enforcement, holdout collapses into voluntary agent discipline and is [F53-fragile](../../architectures/v3/failure-modes-v3.md).

Holdout sits *between* substrate primitive [P-08 (scenario storage + runner-API contract)](../../architectures/v3/primitives/cluster-C3.md#p-08--scenario-storage-out-of-tree-holdout-partitioned) and the methodology layer. [ADR 0015](./0015-p-08-scenario-storage-with-runner-contract.md) authored P-08 as the substrate mechanism: typed-object store, ABAC policy on a `partition: train | holdout` field, and a `read(partition=holdout, judge-role=...) → ScenarioResult` runner-API. This ADR authors the **methodology contract** that every scenario-touching methodology layer must honor against that mechanism.

## Decision

**The holdout discipline binds every methodology that authors or consumes scenarios to three obligations against [P-08's runner-API contract](./0015-p-08-scenario-storage-with-runner-contract.md):**

1. **Write-time tagging.** Every scenario emitted into [P-08](../../architectures/v3/primitives/cluster-C3.md#p-08--scenario-storage-out-of-tree-holdout-partitioned) carries a `partition: train | holdout` field set at write-time by the authoring methodology. The field is immutable post-write (P-08's ABAC policy denies rewrites); methodologies that need to migrate a scenario between partitions must re-author it.
2. **Judge-role-only holdout consumption.** Builder-role contexts call [P-08's](./0015-p-08-scenario-storage-with-runner-contract.md) runner-API only with `partition=train`. Holdout-partitioned scenarios are consumed exclusively through the `judge-role` token via the runner subprocess; the parent strips the judge token before forking any builder process (per ADR 0015's runner contract).
3. **Verdict-envelope return.** The judge subprocess returns only a verdict envelope (`pass | fail | inconclusive` + structured failure-class tags) to the methodology layer. Scenario content, acceptance criteria, and per-test diagnostics MUST NOT flow back into builder-visible context. Methodologies that want richer feedback author it from the verdict envelope, never from the underlying scenario.

The discipline operationalizes [D-4 (corpus default)](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) at the methodology layer; substrate enforcement is delegated to [ADR 0015 P-08](./0015-p-08-scenario-storage-with-runner-contract.md). Architecture-spec authors (Phase 6) declare per-candidate provenance variations (operator-authored vs codebase-derived vs telemetry-as-scenario); the discipline's *shape* is uniform across candidates. Phase-8 lean-evals MUST include a holdout-leakage pressure-test against each candidate's verdict-envelope boundary.

## Alternatives considered

**B. Methodology-only honor-system (no substrate binding).** A reasonable starting position when scenarios are operator-authored documents the team agrees to gate informally. *Why rejected:* exactly the [F53 voluntary-discipline-fragile](../../architectures/v3/failure-modes-v3.md) pattern — a single hurried agent (or a refactor that "just inlines" a holdout snippet into a builder prompt for debugging) silently degrades F28 mitigation. Every track's discipline write-up explicitly names substrate enforcement as the point ([U-A](../../architectures/v3/tracks/unified-A.md): *"the substrate's policy mediator refuses to close a `kind: judge` interval if acceptance-criteria handles leaked"*; [GF-C](../../architectures/v3/tracks/greenfield-cold-start-first.md): *"enforced at substrate, not methodology discipline (per F53)"*). Binding the methodology layer to [ADR 0015 P-08](./0015-p-08-scenario-storage-with-runner-contract.md)'s runner-API converts the discipline from honor-system to mechanically-enforced.

**C. Per-environment partition (e.g., filesystem subdirs, separate repos, OS permissions).** *Why rejected:* per-environment partitioning defeats portability — the partition discipline must hold identically across local dev, CI, and production substrate deployments. ADR 0015 already rejected the filesystem-subdir variant at the substrate layer for the same reason (coarse, platform-specific, per-environment chore). A methodology contract that hooks per-environment mechanisms inherits that brittleness; binding to [ADR 0015's](./0015-p-08-scenario-storage-with-runner-contract.md) ABAC + role-token contract gives the methodology a single uniform interface.

## Consequences

**Easier:** F28 mitigation is uniform across all 10 candidates; methodologies consume one runner-API regardless of upstream scenario provenance. The verdict-envelope contract gives Phase-8 lean-evals a defined leakage-pressure-test surface (probe whether scenario content reconstructs from the envelope). Brownfield D-2 (scenarios-in-tree) is accommodated without weakening the discipline — *unseen-by-builder* is the operative property, and ABAC on the role token enforces it whether the bytes live out-of-tree or alongside the codebase.

**Harder:** Methodologies that previously inspected scenario content for richer feedback loops must re-author against the verdict envelope only. Candidates whose builder agents currently expect to see acceptance criteria during construction (a known anti-pattern that this discipline criminalizes) need explicit refactor work at architecture-spec time.

**Explicitly NOT promising:** the partition-selection protocol. *Which* scenarios go to `holdout` vs `train` is per-candidate provenance — codebase-derived selection in [BF-L](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md), operator-authored in [GF-M](../../architectures/v3/tracks/greenfield-methodology-first.md), telemetry-sampled in [BF-S](../../architectures/v3/tracks/brownfield-substrate-first.md). The discipline mandates the tagging *contract*; the selection *protocol* lives in the per-candidate architecture spec.

## References

- [Holdout discipline write-up](../../architectures/v3/disciplines/holdout.md)
- [Disciplines index](../../architectures/v3/disciplines/index.md)
- [ADR 0015 — P-08 scenario storage with runner contract](./0015-p-08-scenario-storage-with-runner-contract.md) — the substrate mechanism this discipline binds against
- [P-08 buildability sketch](../../architectures/v3/primitives/cluster-C3.md#p-08--scenario-storage-out-of-tree-holdout-partitioned)
- [F28 holdout leakage failure mode](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders)
- [F53 voluntary-discipline-fragile](../../architectures/v3/failure-modes-v3.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — this ADR is part of the Wave-5.2 parallel fanout.
