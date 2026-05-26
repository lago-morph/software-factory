# ADR 0015: P-08 scenario storage with runner contract

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a exemplar)

## Context

Four candidates claim P-08 scenario storage as a load-bearing substrate primitive: [GF-S/S2](../../architectures/v3/tracks/greenfield-substrate-first.md), [GF-M (D-4 enforcement)](../../architectures/v3/tracks/greenfield-methodology-first.md), [BF-L (codebase-derived scenarios)](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md), and [BF-M (stage-7 acceptance)](../../architectures/v3/tracks/brownfield-methodology-first.md). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/cluster-C3.md#p-08--scenario-storage-out-of-tree-holdout-partitioned) verdicts the primitive `designed-system` — the storage half is commodity, the partition-discipline + role-keyed access boundary is the load-bearing design content. Per the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse), P-09 (held-out runner) absorbs into P-08 as a runner-API on the same substrate; this ADR covers the combined surface.

The forcing failure mode is [F28 (holdout leakage)](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders) rated `critical` for greenfield and `high` for brownfield. The substrate must keep partition assignments durable from write-time and must enforce read-access by role token rather than relying on agent-discipline (which would be [F53-fragile](../../architectures/v3/failure-modes-v3.md)).

## Decision

**Build P-08 as a typed-object store on a content-addressed blob backend (S3-compatible with object-versioning; Git LFS acceptable for smaller deployments), with an OPA-Rego attribute-based access-control (ABAC) policy layer enforcing the `partition: train | holdout` field against the requester's role token, and a `read(partition=holdout, judge-role=...) → ScenarioResult` runner-API contract published alongside.** Builder-role tokens are denied reads on `partition=holdout` entries; judge-role tokens read both but cannot rewrite the `partition` field. The policy itself is versioned alongside the store so partition-rule edits are auditable.

The runner-API is **part of P-08's contract** (not a separate P-09 primitive). The runner subprocess inherits the judge-role token via a scoped environment variable the parent strips before forking any builder process. Determinism is enforced by pinning the runner image hash + model snapshot + seed.

## Alternatives considered

**B. P-09 as a distinct primitive (storage + runner as separate ADRs).** Initially carried this way through Phase 3.5. *Why rejected:* the Phase-4.2 overlap analysis verdicted P-09 as the read-API contract on P-08's substrate, not a separable primitive — a P-09 deployment without P-08 is non-executable. Treating them as distinct invited methodology-layer drift on partition enforcement. See [overlap.md § P-08 ↔ P-09](../../architectures/v3/primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse).

**C. Filesystem partition (training/ and holdout/ subdirs) with OS-level permissions.** *Why rejected:* OS-level permissions are coarse and platform-specific; rebuilding the partition discipline across platforms (Linux/macOS/Windows for local dev; container/host boundary in CI) becomes a per-environment chore. ABAC at the substrate layer is platform-independent and audit-friendly. See [`P-08 Construction path`](../../architectures/v3/primitives/cluster-C3.md#construction-path).

## Consequences

**Easier:** F28 mitigation becomes substrate-enforced rather than agent-discipline-dependent (closes [F53 fragility](../../architectures/v3/failure-modes-v3.md)). All four claiming candidates' partition requirements are met by the same substrate. The runner-API contract is uniform across deployments — methodology layers consume `P-08.read(partition='holdout', judge-role=...)` without knowing the storage backend.

**Harder:** OPA-Rego deployment + policy authoring becomes a per-environment ops requirement. Role-token issuance and rotation need a separate identity discipline (not part of this ADR; resolved at architecture-spec time per Phase 6).

**Explicitly NOT promising:** the same-vs-distinct verdict on partition *semantics* across candidates. GF-M's D-4 partition is operator-authored scenarios; BF-L's is codebase-derived; the runner-API is uniform, but the *upstream* scenario provenance is per-candidate. Phase-5 Wave-5.3 candidate-specific ADRs (deferred to next run per [auto-005 Round 2](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md#decision-round-2)) will record those provenance variations.

## References

- [P-08 buildability sketch](../../architectures/v3/primitives/cluster-C3.md#p-08--scenario-storage-out-of-tree-holdout-partitioned), [P-09 absorbed sketch](../../architectures/v3/primitives/cluster-C3.md#p-09--held-out-scenario-runner)
- [Phase-4.2 overlap verdict on P-08 ↔ P-09 collapse](../../architectures/v3/primitives/overlap.md#p-08--p-09--held-out-runner--scenario-storage-collapse)
- [Substrate-requirements summaries citing P-08](../../architectures/v3/substrate-requirements/): [GF-S](../../architectures/v3/substrate-requirements/gf-s.md), [GF-M](../../architectures/v3/substrate-requirements/gf-m.md), [BF-L](../../architectures/v3/substrate-requirements/bf-l.md), [BF-M](../../architectures/v3/substrate-requirements/bf-m.md)
- [F28 holdout leakage failure mode](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — this ADR is the Wave-5.1a exemplar.
