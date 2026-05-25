# ADR 0051: U-A P-28 variant — interval-typed envelope schema

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c1 subagent

## Context

[ADR 0029](0029-p-28-typed-object-store.md) records the **common P-28 framework** — content-addressed append-only typed-object store on libgit2 (`git_odb_write` + `refs/notes/<envelope-kind>`) with Postgres (`bytea` + `jsonb` + GIN) as an alternate path — shared across four contested envelope variants (U-A interval, U-B layer, U-C anchor, D7-U-1 FC). It explicitly defers per-variant envelope schemas to four Wave-5.3 ADRs (this ADR is the U-A interval one).

The [Phase-4.2 overlap analysis verdict on P-28](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is verbatim: **"SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per [P-28 sketch](../../architectures/v3/primitives/P-28-typed-object-store.md)). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."** The overlap.md table row for U-A specifies the envelope as `EscrowInterval{id, kind, pace-layer, priors, policies, classifier, artefacts}` with typed-filter primary axis `kind × pace-layer × classifier.work-unit-class`.

[U-A's substrate-requirements summary §3 P-28 contract](../../architectures/v3/substrate-requirements/u-a.md) names the same fields with their domains: `kind ∈ {bootstrap, refactor, spec-author, review, merge, deploy, re-entry, archaeology, methodology-delta, …}`; `pace-layer ∈ {code, plans, specs, architecture, standards}`; `priors.{out-of-tree[], in-tree[]}`; `policies.{gate, log, sandbox, approval-gate, reflection-trigger, judge-diversity}`; `classifier.{work-unit-class, automation-eligibility}`; `artefacts.{inputs[], outputs[], trajectory}`. The envelope is U-A's load-bearing substrate handle — every cycle node is a durable `EscrowInterval` record per [unified-A §1](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch); D-7 trajectory capture is the inside-the-interval event stream the envelope wraps.

The storage, content-hash, immutability, and JSON-Schema-at-`put`-time disciplines are inherited unchanged from [ADR 0029](0029-p-28-typed-object-store.md); this ADR specifies only the per-variant envelope.

## Decision

**Build U-A's P-28 instantiation as an interval-typed envelope `EscrowInterval{id, kind, pace-layer, priors, policies, classifier, artefacts}` registered against the [ADR 0029](0029-p-28-typed-object-store.md) substrate under the `refs/notes/escrow-interval` namespace (libgit2 path) or `envelope_kind = 'escrow-interval'` discriminator (Postgres path).**

Schema components:

1. **Identity and typing.** `id` is the content-hash returned by the substrate `put`. `kind` is a closed-enum-with-extension-point per the U-A field domain above; new kinds register via a methodology-delta interval that itself carries `kind: methodology-delta`. `pace-layer` is a closed enum drawn from Brier's pace-layer model per [unified-A §1](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch).

2. **Priors and artefacts.** `priors.out-of-tree[]` and `priors.in-tree[]` are arrays of content-hashes pointing back into the P-28 store (or into the codebase ODB for in-tree priors). `artefacts.{inputs[], outputs[], trajectory}` similarly references P-28 handles; `trajectory` points at the D-7 event-stream segment for this interval.

3. **Policies and classifier.** `policies.{gate, log, sandbox, approval-gate, reflection-trigger, judge-diversity}` is the structured slot-set consumed by [ADR 0030 P-29 policy mediator](0030-p-29-policy-mediator.md) — closure conditions are evaluated against this block. `classifier.{work-unit-class, automation-eligibility}` is the structured output of [ADR 0028 P-19 classifier](0028-p-19-eligibility-regime-classifier.md), pinned at interval-open time.

4. **Typed-filter axis.** Per overlap.md row, the primary index axis is `kind × pace-layer × classifier.work-unit-class`. Under the libgit2 path this is realised as three `refs/notes/escrow-interval/<axis>/<value>` sub-namespaces; under the Postgres path as a composite GIN index on `(envelope->>'kind', envelope->>'pace-layer', envelope->'classifier'->>'work-unit-class')`.

5. **JSON-Schema registration.** A canonical `escrow-interval.schema.json` is registered with the substrate per the ADR 0029 envelope-typing contract; `put` validates structure and rejects unknown top-level fields (extension goes through the methodology-delta interval, not ad-hoc envelope mutation).

Per overlap.md, multiple envelope variants **can coexist** on one P-28 substrate via distinct `refs/notes/<envelope-kind>` namespaces; a deployment that runs U-A alongside (e.g.) U-C anchors uses both `refs/notes/escrow-interval` and `refs/notes/anchor` against the same substrate without cross-talk.

## Alternatives considered

**B. Layer-typed envelope (U-B's variant).** *Why rejected here:* U-B's `TypedObject<L>{layer ∈ {L0..L4}, change-rate, escrow-policy, invariants[], parent-layer-ref, child-layer-refs[]}` indexes on pace-layer-as-primary-key with parent/child traversal. U-A's load-bearing axis is the **interval-kind** (bootstrap, refactor, archaeology, re-entry, …) — the *what is happening at this handoff* — with pace-layer as a secondary tag. Importing U-B's shape collapses U-A's `kind` axis into a single layer label and forfeits the typed-node-graph framing that [unified-A §1](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch) makes load-bearing. Per [overlap.md](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants), layer-typed is U-B's distinct envelope; preserved as that variant's ADR, rejected here.

**C. Anchor envelope (U-C's variant).** *Why rejected here:* U-C's `Anchor{kind, content, frozen-since, owning-mandate, mutation-protocol}` makes immutability-metadata first-class — anchors are *frozen-by-default* with explicit mutation protocols. U-A's intervals are *durable but not frozen*; the substrate permits supersession-by-new-put (back-reference field), back-edges in the cycle graph, and revisable spec-author intervals per [unified-A §3 UC4 stance](../../architectures/v3/tracks/unified-A.md). Adopting anchor semantics would erase U-A's revisability and over-constrain bootstrap / methodology-delta intervals. Per overlap.md, anchor is U-C's distinct envelope; preserved as that variant's ADR, rejected here.

## Consequences

**Easier:** U-A's load-bearing substrate handle lands on the [ADR 0029](0029-p-28-typed-object-store.md) framework with no substrate-construction re-litigation. The interval graph is queryable along its natural axis (kind × pace-layer × work-unit-class); D-7 trajectory capture plugs into `artefacts.trajectory` as a P-28 handle, paid for at the framework price. Coexistence with other envelope variants on the same substrate is preserved per overlap.md.

**Harder:** The `kind` enum's extension discipline (methodology-delta intervals) must be enforced at `put`-time JSON-Schema validation, not after-the-fact. Interval-granularity ([unified-A §7 OQ 1](../../architectures/v3/tracks/unified-A.md#7-open-questions-surfaced-by-this-track)) determines envelope volume — DPU-1 cost concern carries to Phase 8 lean-eval per [u-a.md §2](../../architectures/v3/substrate-requirements/u-a.md). The `policies` and `classifier` sub-objects are now load-bearing for [ADR 0030](0030-p-29-policy-mediator.md) and [ADR 0028](0028-p-19-eligibility-regime-classifier.md) — schema-versioning across all three ADRs must stay in lockstep.

## References

- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — parent common ADR (libgit2/Postgres construction, content-hash, append-only discipline, envelope-typing contract)
- [Phase-4.2 overlap.md P-28 verdict — four contested variants](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) — SAME-with-DISTINCT-envelopes verdict and the interval row this ADR instantiates
- [U-A substrate-requirements summary §3 P-28 contract](../../architectures/v3/substrate-requirements/u-a.md) — interval envelope field domains and typed-filter axis
- [unified-A.md §1 architecture sketch](../../architectures/v3/tracks/unified-A.md#1-architecture-sketch) — `EscrowInterval` as the load-bearing typed-node-graph primitive; cycle as graph of interval nodes
- [P-28 typed-object store buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) — substrate construction path the envelope plugs into
- [ADR 0028: P-19 eligibility/regime classifier framework](0028-p-19-eligibility-regime-classifier.md) — consumes `classifier.{work-unit-class, automation-eligibility}` sub-object
- [ADR 0030: P-29 policy mediator framework](0030-p-29-policy-mediator.md) — consumes `policies` sub-object as closure conditions
