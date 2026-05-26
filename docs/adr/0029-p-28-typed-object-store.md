# ADR 0029: P-28 typed-object store substrate framework

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1b parallel fanout)

## Context

Four candidates claim P-28 typed-object store as a load-bearing substrate primitive: [U-A typed-node-graph](../../architectures/v3/tracks/unified-A.md), [U-B layer-typed](../../architectures/v3/tracks/unified-B.md), [U-C anchor](../../architectures/v3/tracks/unified-C.md), and [D7-U-1 FC](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) verdicts the primitive `designed-system` — the storage half is commodity construction, while each variant's **typed envelope schema** is the load-bearing design content.

Per the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants): **"SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe ... The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."** This ADR records the **substrate framework only**; per-variant envelope schemas are deferred to Wave 5.3.

All four variants share a common API surface: `put(typed_envelope) → content_hash` (deterministic, idempotent), `get(content_hash) → typed_envelope` (immutable), and `query(typed_filter) → cursor` (typed-field-indexed scan over append-only log). Supersession is encoded as a new put carrying a back-reference field; no in-place mutation or deletion is permitted.

## Decision

**Build P-28 as a content-addressed append-only typed-object store on libgit2 (`git_odb_write` for blob storage under SHA-256 content addressing) with `refs/notes/<envelope-kind>` namespaces serving as typed-filter indices — one notes-ref per envelope-kind so multiple variants coexist on a single substrate without cross-talk. Postgres (`bytea` primary-key payload + `jsonb` envelope column + per-field GIN indexes on `(envelope_kind, envelope->'<typed_field>')` + immutability trigger) is the supported alternate path for deployments without a libgit2 dependency.** The envelope-typing contract is part of P-28's surface: each envelope-kind registers (a) a canonical-serialisation function whose output is the content-hash preimage, (b) a JSON-Schema (or CBOR-Schema) validating envelope structure at `put` time, and (c) the typed-filter axes that name the `refs/notes/<envelope-kind>` (or Postgres GIN) indices. Both paths satisfy Glean-compatible and Postgres-compatible storage requirements per overlap.md.

## Alternatives considered

**B. Postgres-only (drop libgit2 from substrate framework).** *Why rejected:* libgit2's object database is the most direct content-addressed append-only construction available — `git_odb_write` already enforces content-hash equality and immutability at the C-API level, and `refs/notes/<kind>` gives typed indexing without re-walking the ODB. Restricting the framework to Postgres would force Git-native deployments (the U-A and U-B tracks both assume codebase co-residency) to bolt a relational dependency onto a system that already ships a content-addressed store. Keeping both paths preserves deployment flexibility per the [P-28 sketch construction path](../../architectures/v3/primitives/P-28-typed-object-store.md#construction-path).

**C. IPFS / EventStoreDB / Pulumi blob+manifest.** *Why rejected:* the [P-28 sketch](../../architectures/v3/primitives/P-28-typed-object-store.md#construction-path) notes these are "equally viable" but adds operational surface (peer-to-peer infra, separate event-store cluster, or cloud-vendor coupling) without buying us anything the libgit2-or-Postgres pair doesn't already cover. Buildability bar is satisfied by two paths; adding more dilutes the substrate-team's ownership footprint.

**D. Per-variant separate substrates (four distinct stores).** *Why rejected:* the [Phase-4.2 overlap verdict](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) explicitly resolved SAME with DISTINCT envelopes — the underlying primitive is identical across all four variants. Four separate substrates would duplicate the content-addressing and append-only machinery without justification, and would foreclose the multi-variant-on-one-substrate deployment shape that overlap.md flags as viable.

## Consequences

**Easier:** All four candidates' substrate requirements are met by one framework; Wave 5.3's per-variant envelope ADRs become pure-schema work (no substrate-construction re-litigation). A single deployment can host multiple envelope variants on the same P-28 substrate via distinct `refs/notes/<envelope-kind>` namespaces (or distinct `envelope_kind` values in the Postgres path) — Phase-6 architecture specs determine whether variants co-deploy or fan out. Glean and Postgres-compatible storage are both first-class, matching overlap.md's framing.

**Harder:** Two implementation paths (libgit2 + Postgres) double substrate-team maintenance surface; the envelope-registration contract must stay in sync across both. JSON-Schema/CBOR-Schema validation discipline at `put` time is a per-envelope-kind ops requirement (resolved at Phase-6 architecture-spec time).

**Explicitly NOT promising:** per-variant envelope schemas. Per the [Phase-4.2 overlap verdict](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants), this ADR covers the substrate framework only. The four envelope schemas — U-A `EscrowInterval` (interval-typed), U-B `TypedObject<L>` (layer-typed), U-C `Anchor` (anchor with immutability metadata), D7-U-1 `FalsificationCommitment` (FC-typed) — are deferred to **Wave 5.3 as four candidate-specific ADRs** per the [auto-005 Round 2 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md). Envelope-collision pressure-testing (can multiple envelope variants coexist on one substrate without cross-talk?) is also a Wave 5.3 concern.

## References

- [P-28 typed-object store buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) — construction path (libgit2 / Postgres), per-variant envelope schemas, corpus-why citations
- [Phase-4.2 overlap verdict on P-28 four-variant collapse](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) — SAME primitive, DISTINCT envelopes
- [Substrate-requirements summaries citing P-28](../../architectures/v3/substrate-requirements/): [U-A](../../architectures/v3/substrate-requirements/u-a.md), [U-B](../../architectures/v3/substrate-requirements/u-b.md), [U-C](../../architectures/v3/substrate-requirements/u-c.md), [D7-U-1](../../architectures/v3/substrate-requirements/d7-u-1.md)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.1b parallel fanout brief; Wave 5.3 carries the per-variant envelope ADRs
- [ADR 0015: P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — Wave 5.1a exemplar pattern for substrate-framework ADRs
