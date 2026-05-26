# ADR 0059: U-C P-28 variant — anchor envelope schema

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

[ADR 0029 (P-28 typed-object store substrate framework)](0029-p-28-typed-object-store.md) records the substrate decision (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>` namespaces, or Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only). Per the [Phase-4.2 overlap verdict on P-28's four contested variants](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants):

> **Verdict: SAME primitive (P-28 typed-object store framework), DISTINCT envelopes.** All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per [P-28 sketch](../../architectures/v3/primitives/P-28-typed-object-store.md)). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical.

ADR 0029 explicitly defers the four per-variant envelope schemas — U-A `EscrowInterval`, U-B `TypedObject<L>`, U-C `Anchor`, D7-U-1 `FalsificationCommitment` — to Wave 5.3 as four candidate-specific ADRs. This ADR records the U-C variant.

U-C is the [Anchor-Distance Factory](../../architectures/v3/tracks/unified-C.md) candidate: every work unit is parameterised by graph-distance to a load-bearing **immutable anchor**, with mandate parameterised by anchor `kind`. Per [U-C substrate-requirements §P-28](../../architectures/v3/substrate-requirements/u-c.md), U-C's contract on P-28 is **immutability-metadata-first** — frozen-since and mutation-protocol are first-class envelope fields, not policy attached out-of-band, and the typed filter is keyed on `kind × owning-mandate`.

## Decision

**Register the U-C envelope-kind `anchor` on the [ADR 0029](0029-p-28-typed-object-store.md) substrate with the following anchor schema and typed-filter axis.**

**Envelope shape** (per [overlap.md §1 P-28 table row 3](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants)):

```
Anchor{
  kind ∈ {intent-invariant, architecture-rule, standards-rule, live-test, runtime-trace},
  content,                  // immutable bytes
  frozen-since,             // timestamp, content-addressed
  owning-mandate ∈ {greenfield, brownfield, both},
  mutation-protocol         // reference to the rare-mutation policy
}
```

**Substrate binding.** Stored under `refs/notes/anchor` on the libgit2 path; on the Postgres path stored with `envelope_kind = 'anchor'`. The envelope-kind's canonical-serialisation function, JSON-Schema validator, and typed-filter axis are registered into P-28's envelope-registration contract per [ADR 0029 § Decision](0029-p-28-typed-object-store.md#decision).

**Typed-filter axis.** `kind × owning-mandate`, with immutability-metadata as a first-class projection (not a secondary index). On libgit2, sub-namespaces under `refs/notes/anchor/<kind>/<owning-mandate>/` carry the typed scan; on Postgres, a composite GIN index over `(envelope_kind, envelope->'kind', envelope->'owning-mandate')` plus a partial index on `envelope->'frozen-since'` carries the same axis. The [P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) reads the anchor set produced by this filter for `graph_distance` and `pace_layer_crossings` computation.

**Frozen-since is content-addressed immutable.** The `frozen-since` timestamp is part of the canonical-serialisation preimage that feeds the content-hash — flipping it produces a different content-hash, making "silent re-dating" structurally impossible. Once `put(anchor)` returns a hash, that hash *is* the freeze-event identity; later supersession appears as a new anchor envelope (different hash) with `mutation-protocol`-attested back-reference to the prior hash.

**Mutation-protocol encodes the rare-mutation pathway.** The `mutation-protocol` field is a reference (content-hash or named-policy identifier) to the policy governing legitimate change. Per [unified-C §1 primitive #1 and §4 anchor mutation queue](../../architectures/v3/tracks/unified-C.md), legitimate mutation is **always L4 with named-human approval** plus cooling-off windows; this ADR additionally requires **operator-acknowledged + cross-model-judge consensus** as the encoded pathway for the rare-mutation case (the cross-model-judge cohort routed via [P-14](../../architectures/v3/primitives/P-14-judge-router.md), with operator acknowledgement recorded as a typed P-05 event). The anchor mutation queue is a **typed-filter view** over the same substrate (`kind=anchor-edit` envelopes carrying `proposed-content` + `target-anchor-hash`), not a separate primitive — approval gates against the target anchor's `mutation-protocol` value.

## Alternatives considered

**A. Interval-typed (adopt U-A's `EscrowInterval` envelope).** *Why rejected:* the [overlap.md verdict](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is explicit that the four envelopes are non-overlapping. `EscrowInterval`'s typed-filter axis is `kind × pace-layer × classifier.work-unit-class` — it has no first-class slot for `frozen-since` or `mutation-protocol`. U-C's load-bearing claim is that immutability metadata is the primary axis the distance estimator and dispatcher read against; demoting frozen-since/mutation-protocol to free-form fields under an interval envelope would force the [P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) and the [P-19 distance-gated dispatcher](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) to reconstruct immutability state out-of-band — exactly the failure mode that motivated the anchor envelope.

**B. Layer-typed (adopt U-B's `TypedObject<L>` envelope, project anchors onto layers).** *Why rejected:* layer-typed semantics encode pace-layer cadence (change-rate per layer, parent/child graph walk for cross-layer drift). U-C's anchors are not stratified by pace layer — an `intent-invariant` and a `runtime-trace` are both anchors, distinguished by `kind` and `owning-mandate`, not by L0..L4 layer membership. Forcing anchors onto a layer enum would (i) make `kind × owning-mandate` typed filtering indirect (going through a layer index that doesn't carry the relevant axis), and (ii) lose first-class immutability metadata, which the [U-B variant ADR](0055-p-28-variant-u-b-layer-typed-envelope.md) does not carry. Pace-layer cadence is not U-C's organising principle; anchor-distance is.

## Consequences

**Easier:** [P-32 distance estimator](../../architectures/v3/primitives/P-32-distance-estimator.md) gets a directly-typed anchor-set query (`kind × owning-mandate` scan); the [P-19 distance-gated dispatcher](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) reads `mutation-protocol` straight off the target anchor at anchor-edit dispatch time without secondary lookup. Frozen-since being content-addressed means anchor-freeze auditing reduces to ODB walk — no separate provenance log to keep in sync.

**Harder:** Mutation-protocol policy DSL (Phase-5 ADR seed (iv) per [U-C §3](../../architectures/v3/substrate-requirements/u-c.md)) must specify how operator-acknowledged + cross-model-judge consensus is encoded, validated, and replayed — deferred to that downstream ADR. The content-hash-frozen `frozen-since` discipline means re-issuing an anchor for a clerical fix (typo in `content`) produces a new hash and therefore a new freeze event — by design, but it means low-stakes edits still route through the mutation-protocol pathway.

**Explicitly NOT promising:** the mutation-protocol policy DSL itself, the Goodhart-resistance closure on the `intent_field_touches` leg of P-32 (Phase-5 ADR seed (ii)), or co-deployment compatibility with other P-28 envelope variants — envelope-collision pressure-testing across `anchor`, `escrow-interval`, `typed-object-layer`, and `falsification-commitment` envelopes on one substrate is the Wave 5.3 cross-cutting concern per [ADR 0029](0029-p-28-typed-object-store.md#consequences).

## References

- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — parent ADR; substrate construction, envelope-registration contract, deferral of per-variant envelopes to Wave 5.3
- [Phase-4.2 overlap verdict on P-28 four-variant collapse](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) — SAME substrate, DISTINCT envelopes; source of the `Anchor` envelope row and the `kind × owning-mandate` typed-filter axis
- [U-C substrate-requirements §P-28](../../architectures/v3/substrate-requirements/u-c.md) — U-C's contract on the anchor store, immutability-metadata-first framing, anchor mutation queue as typed-filter view
- [Unified-C track §1 primitive #1 + §4 anchor mutation queue](../../architectures/v3/tracks/unified-C.md) — anchor-object canonical shape, cooling-off windows, named-human L4 mutation discipline
- [P-28 typed-object store buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) — construction path, per-variant envelope schemas, corpus citations
- [ADR 0055: U-B P-28 variant — layer-typed envelope schema](0055-p-28-variant-u-b-layer-typed-envelope.md) — sibling Wave 5.3 variant ADR; pattern exemplar for envelope-kind registration on the shared substrate
