# ADR 0040: GF-M P-20 reversibility primitive

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3a subagent (GF-M orphan ADR)

## Context

[GF-M](../../architectures/v3/tracks/greenfield-methodology-first.md) is the sole claimer of [P-20 reversibility primitive](../../architectures/v3/primitives/P-20-reversibility-primitive.md), making this a GF-M-specific orphan ADR rather than a cross-candidate framework decision. P-20 is *constitutive* of [GF-M's Regime A](../../architectures/v3/tracks/greenfield-methodology-first.md#11-regime-a--spec-discovery-the-malleable-phase) — the malleable-phase "promote or reverse" gate requires sub-millisecond commit-and-reverse on intent / scenario / artifact aggregates, without which the "commitments are reversible by design and cheap by substrate" claim collapses and the cycle becomes paralytic.

The [P-20 sketch](../../architectures/v3/primitives/P-20-reversibility-primitive.md) verdicts the primitive `designed-system`: event-sourcing is well-understood, but the integration with intent / scenario / slice artifacts (typed-event taxonomy + compensating-event projection semantics) is the load-bearing design content. The [GF-M substrate-requirements summary § P-20](../../architectures/v3/substrate-requirements/gf-m.md) defers the storage-substrate choice (EventStoreDB vs Postgres event_log vs an event-log on a content-addressed object store) to this Phase-5 ADR.

Failure modes the primitive is shaped against: **F9 (spec overfitting)**, **F41 (under-defined-intent debt)**, **F37 (silent contradictory-prompt collapse)**, and **F40 (last-mile drift)** — all surfaced in the [P-20 sketch corpus-why](../../architectures/v3/primitives/P-20-reversibility-primitive.md#corpus-why-citation).

## Decision

**Build P-20 as an event-sourced reversibility layer on top of the [ADR 0029 P-28 typed-object store substrate](0029-p-28-typed-object-store.md) (libgit2 `git_odb_write` + content-addressed envelopes), rather than as a free-standing event store.** Each mutation event (`IntentDrafted`, `IntentParaphraseEmitted`, `IntentPromoted`, `IntentReversed`, `ScenarioAuthored`, `ScenarioPromoted`, `ScenarioReversed`, `ProbeRealized`, `ProbeOutcomeRecorded`, `SlicePromoted`, `SliceRolledBack`) is a typed envelope-kind under P-28. The **commit operation** is `git_odb_write(canonical_serialise(event))` — the resulting content-hash is the event identity, append-only and immutable by the substrate's construction. The **reverse operation** is `git_odb_write` of a `*Reversed` envelope whose typed `reverses` field is the back-reference content-hash of the event being reversed. The original event stays in the DAG, immutable; reversal is purely additive.

Aggregate projection is a catch-up subscription over the `refs/notes/<event-kind>` indices defined by ADR 0029: a worker scans the stream for an aggregate-ID (e.g., `intent-<uuid>`, `scenario-<uuid>`, `slice-<uuid>`), folds events left-to-right, and drops any event whose hash appears in a subsequent `*Reversed.reverses` field. Optimistic concurrency on append rides on `git_odb_write`'s content-hash uniqueness; the per-aggregate stream order is materialised by a `prev_event_hash` field on each envelope (Merkle-chained), preserving the per-stream `expectedVersion` semantics the [P-20 sketch construction path](../../architectures/v3/primitives/P-20-reversibility-primitive.md#construction-path) requires without an external version counter.

Per-event persist cost is dominated by `git_odb_write` (sub-millisecond on local libgit2; ADR 0029's published latency envelope), satisfying the [P-20 sketch sub-ms target](../../architectures/v3/primitives/P-20-reversibility-primitive.md#cost--latency-analysis) and keeping reversal inside Regime A's inner loop.

## Alternatives considered

**B. Bidirectional mutable state with a rollback log.** Store the current projected aggregate as mutable state and log forward / backward operations to a side journal so reversal replays the inverse. *Why rejected:* fragility under partial failure. If the mutable update succeeds but the rollback-log append fails (or vice versa), the system is in a state that cannot be soundly reversed — the very property GF-M's Regime A demands. The event-sourced + content-addressed shape is sound by construction: every state transition is a single content-addressed append, and "reversal" is forward-only. Mutable state also violates the P-28 substrate's immutability invariant ([ADR 0029](0029-p-28-typed-object-store.md) explicitly forbids in-place mutation), so this alternative would require a parallel substrate just for P-20.

**C. SQL transactional rollback (Postgres `BEGIN` / `ROLLBACK`).** Treat each Regime-A cycle as a database transaction; "reverse" means `ROLLBACK` before commit. *Why rejected:* doesn't fit the content-addressed, append-only convention the rest of the substrate is built on (per [ADR 0029](0029-p-28-typed-object-store.md)). Transactional rollback also collapses to a single decision point — once committed, reversal requires a compensating transaction anyway, which is structurally the event-sourced approach plus an unnecessary transactional middle-layer. The [P-20 sketch's Postgres fallback](../../architectures/v3/primitives/P-20-reversibility-primitive.md#construction-path) is still event-sourced (an `event_log` table), not transactional rollback — confirming this alternative was already rejected upstream.

## Consequences

**Easier:** P-20 inherits ADR 0029's substrate (libgit2 + content-hash + immutability + `refs/notes/<envelope-kind>` typed indices) for free — no separate event-store cluster, no second persistence path to maintain, and the immutability-and-append-only invariants are enforced at the C-API level rather than by P-20-layer discipline. The reversibility primitive's storage-team ownership footprint is zero (it's an envelope-kind registration on P-28); only the typed-event taxonomy and projection-fold logic are owned by the GF-M methodology layer.

**Harder:** The Merkle-chained `prev_event_hash` projection logic is one layer above `git_odb_write` and must be authored as part of GF-M's substrate adapters; the projection worker is a separate process (catch-up subscription) the deployment owns. Compensating-event semantics for cross-aggregate causality (e.g., reversing an intent automatically reversing all scenarios that depend on it) is *not* part of this ADR — the [P-20 sketch RG flag](../../architectures/v3/primitives/P-20-reversibility-primitive.md#research-grade-uncertainty-flag) notes this escalates the projection to a graph-rewrite engine; that work is deferred to GF-M's Phase-6 architecture spec.

**Explicitly NOT promising:** the typed-event taxonomy in its final form. The 11 event-kinds enumerated in the [P-20 sketch contract restatement](../../architectures/v3/primitives/P-20-reversibility-primitive.md#contract-restatement) are the GF-M Regime-A working set; refinements (additional event kinds, field schema details) are Phase-6 architecture-spec work, not Phase-5 substrate.

## References

- [P-20 reversibility primitive buildability sketch](../../architectures/v3/primitives/P-20-reversibility-primitive.md) — construction path, cost/latency analysis, corpus-why citation, RG flag
- [GF-M substrate-requirements summary § P-20](../../architectures/v3/substrate-requirements/gf-m.md) — claimer record, contract, Phase-5 ADR seed
- [GF-M track § 1.1 Regime A and § 1.3 Reversibility primitive](../../architectures/v3/tracks/greenfield-methodology-first.md#11-regime-a--spec-discovery-the-malleable-phase) — methodology corpus-why for sub-ms reversal
- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — substrate this ADR builds on (libgit2 + content-addressed envelopes)
- [ADR 0015: P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — Wave 5.1a exemplar pattern
