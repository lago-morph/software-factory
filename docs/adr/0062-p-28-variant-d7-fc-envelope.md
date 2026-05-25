# ADR 0062: D7-U-1 P-28 variant — FC envelope schema

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3c2 subagent

## Context

[ADR 0029](0029-p-28-typed-object-store.md) records the **common P-28 framework** — content-addressed append-only typed-object store on libgit2 (`git_odb_write` + `refs/notes/<envelope-kind>`) with Postgres (`bytea` + `jsonb` + GIN) as the alternate path — shared across four contested envelope variants (U-A interval, U-B layer, U-C anchor, D7-U-1 FC). It explicitly defers per-variant envelope schemas to four Wave-5.3 ADRs (this ADR is the D7-U-1 FC one).

The [Phase-4.2 overlap analysis verdict on P-28](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) is verbatim: **"SAME primitive (P-28 typed-object store framework), DISTINCT envelopes. All four share the construction recipe (libgit2 `git_odb_write` + `refs/notes/<envelope-kind>`; Postgres `bytea`+`jsonb`+GIN alternate path; content-addressed append-only with typed envelope per [P-28 sketch](../../architectures/v3/primitives/P-28-typed-object-store.md)). The envelope schemas are non-overlapping but the underlying primitive (typed envelope + content-hash + append-only + Glean/Postgres-compatible storage) is identical."** The overlap.md table row for D7-U-1 specifies the envelope as `FC{id, artifact, artifact-kind, conjecture, opposing-side, refutation-attempt, verdict, ledger}` with typed-filter primary axis `artifact-kind × verdict.outcome`.

[D7-U-1's substrate-requirements summary § P-28 contract](../../architectures/v3/substrate-requirements/d7-u-1.md) names the same fields with their domains: `artifact-kind ∈ {spec, plan, code-change, eval, adr, skill, classifier-decision, scaffold-edit}`; `opposing-side.{kind, identity, independence-evidence}`; `refutation-attempt.{budget, method, inputs[]}`; `verdict.{outcome ∈ {survived, conditionally-survived-with-window, refuted}, counter-evidence[], survival-window}`; `ledger.{immutable-log-ref, trajectory-ref}`. The envelope is **commitment-indexed rather than artifact-indexed** — it describes a commitment *about* an artifact, not the artifact itself — and it is D7-U-1's load-bearing substrate handle: every compounding boundary is gated by a typed survived-FC per [d7-u-1.md § P-28](../../architectures/v3/substrate-requirements/d7-u-1.md).

The storage, content-hash, immutability, and JSON-Schema-at-`put`-time disciplines are inherited unchanged from [ADR 0029](0029-p-28-typed-object-store.md); this ADR specifies only the per-variant envelope.

## Decision

**Build D7-U-1's P-28 instantiation as a falsification-commitment envelope `FC{id, artifact, artifact-kind, conjecture, opposing-side, refutation-attempt, verdict, ledger}` registered against the [ADR 0029](0029-p-28-typed-object-store.md) substrate under the `refs/notes/falsification-commitment` namespace (libgit2 path) or `envelope_kind = 'falsification-commitment'` discriminator (Postgres path).**

Schema components:

1. **Identity and indirection.** `id` is the content-hash returned by the substrate `put`. `artifact` is a content-hash handle into the P-28 store (or into the codebase ODB for in-tree artifacts) — the envelope **points at** the artifact rather than wrapping it, which is what makes the FC store commitment-indexed. `artifact-kind` is a closed enum drawn from the D7-U-1 § P-28 domain above.

2. **Commitment body.** `conjecture` is the falsifiable claim the FC commits to; `opposing-side.{kind, identity, independence-evidence}` declares the model-family-different agent / deterministic checker / named human / population vote that will attempt refutation, with `independence-evidence` carrying the proof-of-independence used by [P-34 independence auditor](../../architectures/v3/primitives/P-34-independence-auditor.md). `refutation-attempt.{budget, method, inputs[]}` records the budgeted attempt configuration.

3. **Verdict and survival window.** `verdict.outcome ∈ {survived, conditionally-survived-with-window, refuted}` is the load-bearing field for the compounding gate ([ADR 0030 P-29 framework](0030-p-29-policy-mediator.md) D7-U-1 variant). `verdict.survival-window` carries the expiry timer consumed by the [P-30 survival-window registrar](../../architectures/v3/primitives/P-30-event-registrar.md). `verdict.counter-evidence[]` is an array of P-28 handles to refutation attempts.

4. **Ledger.** `ledger.{immutable-log-ref, trajectory-ref}` points back into the append-only log and the D-7 trajectory event-stream for the refutation attempt; FC-graph traversal walks ledger entries to verify upstream-FC survival before compounding.

5. **Typed-filter axis.** Per overlap.md row, the primary index axis is `artifact-kind × verdict.outcome`. Under the libgit2 path this is realised as `refs/notes/falsification-commitment/<artifact-kind>/<outcome>` sub-namespaces; under the Postgres path as a composite GIN index on `(envelope->>'artifact-kind', envelope->'verdict'->>'outcome')`. **FC ledger walks** — the operation [P-29 D7-U-1 compounding gate](../../architectures/v3/substrate-requirements/d7-u-1.md) performs to verify upstream-FC survival — are supported via Glean Angle queries over `data.fc_ledger` (libgit2 path Glean-indexed) or recursive CTE over the `jsonb` envelope (Postgres path), both inheriting the Glean/Postgres-compatible storage promise from ADR 0029.

6. **JSON-Schema registration.** A canonical `falsification-commitment.schema.json` is registered with the substrate per the ADR 0029 envelope-typing contract; `put` validates structure (rejecting unknown top-level fields) and the `verdict.outcome` enum closure. New `artifact-kind` values register via a `kind: methodology-delta` FC against the schema itself.

Per overlap.md, multiple envelope variants **can coexist** on one P-28 substrate via distinct `refs/notes/<envelope-kind>` namespaces; a deployment that runs D7-U-1 alongside (e.g.) U-A intervals uses both `refs/notes/falsification-commitment` and `refs/notes/escrow-interval` against the same substrate without cross-talk.

## Alternatives considered

**B. Interval-typed envelope (U-A's variant).** *Why rejected here:* U-A's `EscrowInterval{id, kind, pace-layer, priors, policies, classifier, artefacts}` is artifact-indexed and wraps the *handoff* between cycle nodes; the load-bearing axis is `kind × pace-layer × classifier.work-unit-class`. D7-U-1's load-bearing axis is **falsification commitment about an artifact** — `artifact-kind × verdict.outcome` — and the envelope must be commitment-indexed to support the compounding-gate ledger walk per [d7-u-1.md § P-28](../../architectures/v3/substrate-requirements/d7-u-1.md). Importing U-A's shape collapses the FC's `opposing-side` / `refutation-attempt` / `verdict` triad into U-A's `policies` slot-set and erases the commitment indirection that makes survived-FC enforcement work. Per [overlap.md](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants), interval-typed is U-A's distinct envelope; preserved as [ADR 0051](0051-p-28-variant-u-a-interval-envelope.md), rejected here.

**C. Anchor envelope (U-C's variant).** *Why rejected here:* U-C's `Anchor{kind, content, frozen-since, owning-mandate, mutation-protocol}` makes immutability-metadata first-class — anchors are frozen-by-default. D7-U-1's FCs are **verdict-mutable along a controlled lifecycle** (`FC-declared → opposing-side-running → verdict-rendered → survival-window-open → window-expired → re-falsification-required` per [P-30 D7-U-1 variant](../../architectures/v3/primitives/P-30-event-registrar.md)); the survival-window expiry cascade requires the registrar to wake dependent-FC graphs, which anchor's frozen-since semantics forbid. Adopting anchor shape would erase the timer-driven re-falsification trigger that is D7-U-1's structural replacement for voluntary review. Per overlap.md, anchor is U-C's distinct envelope; preserved as that variant's ADR, rejected here.

## Consequences

**Easier:** D7-U-1's load-bearing substrate handle lands on the [ADR 0029](0029-p-28-typed-object-store.md) framework with no substrate-construction re-litigation. FC-graph traversal is queryable along its natural axis (`artifact-kind × verdict.outcome`) via Glean Angle on the libgit2 path or composite GIN on the Postgres path. Coexistence with other envelope variants on the same substrate is preserved per overlap.md, enabling hybrid deployments that combine FC-gating with U-A intervals or U-C anchors.

**Harder:** The `verdict.outcome` enum closure must be enforced at `put`-time JSON-Schema validation — the compounding gate and survival-window registrar both treat this field as load-bearing. Schema-versioning must stay in lockstep with [ADR 0030 P-29 framework](0030-p-29-policy-mediator.md) (which consumes `verdict` and `ledger`) and the [P-30 D7-U-1 survival-window registrar](../../architectures/v3/primitives/P-30-event-registrar.md) (which consumes `verdict.survival-window`). FC-graph cost at high parallelism (D7-U-1 OQ-2 per [d7-u-1.md](../../architectures/v3/substrate-requirements/d7-u-1.md)) is corpus-unmeasured and carries to Phase-8 lean-eval.

## References

- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — parent common ADR (libgit2/Postgres construction, content-hash, append-only discipline, envelope-typing contract)
- [Phase-4.2 overlap.md P-28 verdict — four contested variants](../../architectures/v3/primitives/overlap.md#p-28-typed-object-store--four-contested-variants) — SAME-with-DISTINCT-envelopes verdict and the FC row this ADR instantiates
- [D7-U-1 substrate-requirements summary § P-28 contract](../../architectures/v3/substrate-requirements/d7-u-1.md) — FC envelope field domains, commitment-indexing rationale, and typed-filter axis
- [D7-U-1 candidate sketch — Falsification-Topology Factory](../../architectures/v3/bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) — `FalsificationCommitment` schema source; compounding-gate semantics
- [P-28 typed-object store buildability sketch](../../architectures/v3/primitives/P-28-typed-object-store.md) — substrate construction path; D7-U-1 FC envelope row
- [ADR 0051: U-A P-28 variant — interval-typed envelope schema](0051-p-28-variant-u-a-interval-envelope.md) — sibling variant ADR (interval-typed alternative rejected here)
- [ADR 0055: U-B P-28 variant — layer-typed envelope schema](0055-p-28-variant-u-b-layer-typed-envelope.md) — sibling variant ADR
