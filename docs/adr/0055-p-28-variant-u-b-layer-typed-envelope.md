# ADR 0055: U-B P-28 variant — layer-typed envelope schema

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c1 subagent

## Context

[ADR 0029 (P-28 typed-object store substrate framework)](0029-p-28-typed-object-store.md) records the substrate decision (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>` namespaces, or Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only). Per the [Phase-4.2 overlap verdict on P-28's four contested variants](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants):

> **Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes.** All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per [P-28 sketch](../../architectures/v3/primitives/P-28-typed-object-store.md)). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical.

ADR 0029 explicitly defers the four per-variant envelope schemas — U-A `EscrowInterval`, U-B `TypedObject<L>`, U-C `Anchor`, D7-U-1 `FalsificationCommitment` — to Wave 5.3 as four candidate-specific ADRs. This ADR records the U-B variant.

U-B is the [Pace-Layered Escrow Factory](../../architectures/v3/tracks/unified-B.md) candidate: a 5-layer artifact stack (L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code) with bidirectional traversal. Per [U-B substrate-requirements §P-28](../../architectures/v3/substrate-requirements/u-b.md), U-B's contract on P-28 is layer-indexed (not interval-indexed like U-A, not anchor-immutability-indexed like U-C, not FC-commitment-indexed like D7-U-1). The `(parent-layer-ref → child-layer-refs)` traversal is the primary input axis for P-31 cross-layer drift detection.

## Decision

**Register the U-B envelope-kind `typed-object-layer` on the [ADR 0029](0029-p-28-typed-object-store.md) substrate with the following layer-typed schema and typed-filter axis.**

**Envelope shape** (per [overlap.md §1 P-28 table row 2](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants)):

```
TypedObject<L>{
  layer ∈ {L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code},
  change-rate,
  escrow-policy,
  invariants[],
  parent-layer-ref,
  child-layer-refs[]
}
```

**Substrate binding.** Stored under `refs/notes/typed-object-layer` on the libgit2 path; on the Postgres path stored with `envelope_kind = 'typed-object-layer'`. The envelope-kind's canonical-serialisation function, JSON-Schema validator, and typed-filter axis are registered into P-28's envelope-registration contract per [ADR 0029 § Decision](0029-p-28-typed-object-store.md#decision).

**Typed-filter axis.** `layer × (parent-layer-ref → child-layer-refs)` traversal. The `layer` field is the primary GIN index (libgit2: a sub-namespace per layer under `refs/notes/typed-object-layer/L{0..4}/`); the parent/child refs power graph-traversal queries used by [P-31 cross-layer drift detection](../../architectures/v3/primitives/P-31-cross-layer-drift-detector.md) (planned ADR 0054, which reads from this envelope shape).

**Layer-cross-reference discipline.** `parent-layer-ref` and `child-layer-refs[]` are stored as **content-hash pointers** (the put-result of the referenced envelope), not mutable handles. This preserves ADR 0029's append-only discipline across the layer graph: re-pointing a child at a new parent version is itself a new `put` carrying back-reference fields, never an in-place edit. Supersession of a `TypedObject<L>` instance follows the substrate's standard back-reference encoding.

**Per-layer semantics.** Each layer's `change-rate` (slow at L0, faster at L4) and `escrow-policy` are first-class envelope fields, not external metadata — preserving the pace-layer cadence that drives [P-29 per-layer transition gates](0030-p-29-policy-mediator.md) (the U-B variant's per-layer-boundary closure encoding consumes `escrow-policy` directly).

## Alternatives considered

**A. Use U-A's interval-typed `EscrowInterval` envelope and project pace-layers onto interval-kinds.** *Why rejected:* the [overlap.md verdict](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is explicit that the four envelopes are non-overlapping. `EscrowInterval`'s typed-filter axis is `kind × pace-layer × classifier.work-unit-class` — pace-layer appears as a *secondary* index over interval-kinds. U-B requires `layer` as the *primary* axis with parent/child graph traversal, which interval semantics neither expose nor optimize. Coercing U-B onto the interval envelope would lose the pace-layer cadence semantics (change-rate, per-layer escrow-policy) that drive P-29 transition gates and P-31 drift detection — the very differentiator that overlap.md flags as the basis for keeping U-B distinct.

**B. Flat typed-object envelope with `layer` as a free-form tag (no graph fields).** *Why rejected:* a flat envelope without `parent-layer-ref` / `child-layer-refs[]` cannot support the `(parent-layer-ref → child-layer-refs)` traversal that [P-31 cross-layer drift detection](../../architectures/v3/substrate-requirements/u-b.md) treats as its primary input axis. Stewart Brand pace-layer semantics also require explicit cross-layer linkage (change-rate at one layer constrains the next); a flat tag loses that. Reconstructing parent/child relationships at query time from a flat layer field would require a separate index structure outside the envelope — duplicating substrate machinery the typed envelope is designed to carry.

## Consequences

**Easier:** P-31 cross-layer drift detection (planned ADR 0054) gets a well-typed input shape — `layer`-keyed scans plus parent/child graph walk are direct queries against `refs/notes/typed-object-layer`. P-29's per-layer-boundary policy reads `escrow-policy` from the envelope without secondary lookup. Pace-layer cadence semantics are preserved in storage shape rather than reconstructed at the application layer.

**Harder:** Layer-count migration (OQ-PLEF-1 per [U-B §5](../../architectures/v3/substrate-requirements/u-b.md#5-open-carries)) requires an envelope-version field and a migration discipline — adding or removing a layer changes the `layer` enum's valid values, and historical envelopes must remain interpretable. Deferred to Phase-5 ADR seed (i). The content-hash-pointer discipline on cross-layer refs means a parent-layer update fans out re-points across all children — operationally heavy but the price of append-only correctness.

**Explicitly NOT promising:** layer-count stability, the P-31 invariant catalog (Wave 4.5 deliverable), or co-deployment compatibility with other P-28 envelope variants (a deployment hosting `typed-object-layer` alongside `escrow-interval` or `falsification-commitment` envelopes is permitted by the substrate but not validated here — envelope-collision pressure-testing is the Wave 5.3 cross-cutting concern per [ADR 0029](0029-p-28-typed-object-store.md#consequences)).

## References

- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — parent ADR; substrate construction, envelope-registration contract
- [Phase-4.2 overlap verdict on P-28 four-variant collapse](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) — SAME substrate, DISTINCT envelopes; source of the `TypedObject<L>` envelope row
- [U-B substrate-requirements §P-28](../../architectures/v3/substrate-requirements/u-b.md) — U-B's contract on the layer-typed store, typed-filter axis, and differentiator vs other P-28 variants
- [P-28 typed-object store buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) — construction path, per-variant envelope schemas, corpus citations
- [ADR 0030: P-29 policy mediator substrate](0030-p-29-policy-mediator.md) — consumer of the envelope's `escrow-policy` field at per-layer transition gates
- ADR 0054 (planned): P-31 cross-layer drift detector — reads from this envelope shape; `(parent-layer-ref → child-layer-refs)` traversal is its primary input axis
