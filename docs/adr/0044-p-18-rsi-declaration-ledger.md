# ADR 0044: GF-C P-18 RSI Declaration Ledger

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3a subagent — GF-C orphan)

## Context

[GF-C — Greenfield, cold-start-first](../../architectures/v3/tracks/greenfield-cold-start-first.md) is the sole claimant of [P-18 — RSI-Declaration Ledger](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md) per [substrate-requirements §1](../../architectures/v3/substrate-requirements/gf-c.md#1-primitive-list-buildability-confirmed). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md) verdicts the primitive `designed-system`: the storage half is commodity, while the typed declaration schema, the immutable-append contract, and the deterministic board-report-derivation read query are the load-bearing design content.

P-18 records, day-0 and per-cycle, whether the factory satisfies Kahana's three-part RSI test ([durable self-modification + compounding capability + limited human gating](../../research/31-caremark-rsi-board-exposure.md)) and stores the evidence trail a Caremark-prong-1 board report would later need to demonstrate the three AILCCP controls (Human-Approval Gate / sandboxing / immutable logging) are *actually running* rather than *merely scaffolded*. Entry kinds: initial RSI declaration (operator-signed), per-cycle AILCCP-control attestations, Human-Approval-Gate exercise events, board-report renderings and acknowledgements, SB-53 reportability classifications, and declaration amendments (each a new append, never a rewrite).

The forcing failure mode is [F43 RSI Board-Visibility Gap](../../architectures/v3/failure-modes-v3.md) — structurally closed at day 0 only if per-cycle control attestation is a *required append*, not a retrospective reconstruction. Contributing closures: [F54 (goal subversion across cycles)](../../architectures/v3/failure-modes-v3.md) via durable declared-objective record, and [F55 (behavioural drift)](../../architectures/v3/failure-modes-v3.md) via human-grounded declaration the agent cannot rewrite. The append-only contract must live in the storage layer per F53 (voluntary-discipline fragility), not in the calling agent.

GF-C's substrate already mandates [P-28 typed-object store](../../architectures/v3/primitives/P-28-typed-object-store.md) for typed, content-addressed, append-only storage (per [ADR 0029](0029-p-28-typed-object-store.md)). P-17 ([Intent Crucible validator, ADR 0043](0043-p-17-intent-crucible-validator.md)) is the downstream consumer that must read declaration revision history to validate intent across cycles. P-18's day-0 instantiation predates P-17 substance use and must boot from the same substrate family without a second tamper-evident store.

## Decision

**Build P-18 as an envelope-typed view on the P-28 typed-object store substrate** ([ADR 0029](0029-p-28-typed-object-store.md)), introducing `EnvelopeKind=RSIDeclaration` whose canonical-serialisation, JSON-Schema, and typed-filter axes register against P-28's envelope contract. Every P-18 entry is a P-28 `put(typed_envelope) → content_hash` call; immutability and content-hash chaining are inherited from the substrate (libgit2 ODB or Postgres `bytea + jsonb` + immutability trigger). Supersession of a prior declaration is encoded as a new envelope with a `supersedes: <prior_content_hash>` back-reference field, matching P-28's no-in-place-mutation rule.

The `RSIDeclaration` envelope schema carries: `subkind ∈ {declaration, attestation, gate-exercise, report-emit, sb53-classification, amendment}`, `agent_id`, `cycle_id`, `declared_scope`, `evidence_pointer` (content-hash into P-28 itself for the underlying artifact), `judge_verdict` (where applicable), `operator_ack_state`, `prior_hash` (Merkle chain over the kind-filtered sequence), and an operator signature on `subkind=declaration` and `subkind=amendment` entries.

**Query API** (deterministic, no LLM in the path): `query_by_agent(agent_id, time_range, verdict_status?) → cursor` and `render_board_report(period) → ReportPayload`, both implemented as typed-filter scans over `refs/notes/RSIDeclaration` (libgit2 path) or `WHERE envelope_kind='RSIDeclaration' AND envelope->>'cycle_id' = ...` GIN-indexed lookups (Postgres path). Downstream: [P-17 intent validator](../../architectures/v3/primitives/P-17-intent-crucible-validator.md) consumes `query_by_agent` for cross-cycle reasoning over declared intent versus observed behaviour.

## Alternatives considered

**B. Standalone SQLite-WAL audit table with `BEFORE UPDATE`/`BEFORE DELETE` abort triggers** (the [P-18 sketch's named tool](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md#construction-path)). *Why rejected:* the sketch's recipe is sound in isolation, but GF-C's substrate already mandates P-28 for typed-object content-addressed storage. Standing up a second tamper-evident store duplicates content-addressing and append-only machinery the substrate-team would otherwise maintain twice, and a SQLite row is not content-addressed in the same shape as P-28 envelopes — so cross-references between RSI-declaration entries and other day-0 artifacts (P-11 bench manifests, P-17 intent blocks) would require a bespoke pointer convention rather than a uniform content-hash. The sketch's design content (typed schema, immutable-append contract, deterministic board-report query) transfers losslessly onto P-28 envelopes; the storage mechanics do not need to be re-litigated.

**C. Per-agent local append-only log** (one file or one repo per agent process). *Why rejected:* defeats the cross-cycle correlation P-17 needs. Caremark prong-1 board reporting is a *factory-level* statement about which controls were running across the population of agents in a reporting period; a per-agent log forces an offline correlation step that re-introduces F43 (board-visibility gap) at the aggregation boundary. A single typed substrate with `agent_id` as a typed-filter axis collapses the correlation into a query, not a batch job.

## Consequences

**Easier:** F43 mitigation becomes substrate-enforced (P-28's immutability trigger + content-hash chain), not P-18-bespoke. Board-report rendering is a deterministic typed-filter read query — no LLM in the path, no separate audit-trail synchronisation. P-17 cross-cycle reasoning reads the ledger through P-28's standard `query(typed_filter) → cursor` surface. Cross-references between declaration entries and other day-0 artifacts (P-11 bench, P-17 intent) use uniform content-hashes.

**Harder:** P-28 must be available at day 0 of GF-C's bootstrap, *before* P-17 substance use — a soft sequencing constraint already implied by GF-C's day-0 primitive list but worth naming. The `RSIDeclaration` envelope schema is now governed by P-28's envelope-registration discipline (canonical-serialisation function + JSON-Schema + typed-filter axes) rather than free-floating SQLite DDL; a Phase-6 architecture-spec task owns the registration.

**Explicitly NOT promising:** the day-0 *content* of the initial RSI declaration (which scope, which AILCCP-control attestations the factory commits to). That is methodology-layer per [GF-C §1.2](../../architectures/v3/tracks/greenfield-cold-start-first.md). The SB-53 classification rubric is also out of scope — P-18 stores the classification, it does not derive it.

## References

- [P-18 RSI-Declaration Ledger buildability sketch](../../architectures/v3/primitives/P-18-rsi-declaration-ledger.md) — typed-schema, immutable-append, board-report-derivation contract
- [GF-C substrate requirements §1 P-18 row](../../architectures/v3/substrate-requirements/gf-c.md#1-primitive-list-buildability-confirmed) — sole claimant, candidate-specific contract
- [ADR 0029: P-28 typed-object store substrate framework](0029-p-28-typed-object-store.md) — substrate this ADR builds on
- [ADR 0043: P-17 Intent Crucible validator](0043-p-17-intent-crucible-validator.md) — downstream consumer for cross-cycle reasoning
- [ADR 0015: P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — Wave 5.1a exemplar pattern for substrate-framework-on-substrate ADRs
- [research/31-caremark-rsi-board-exposure](../../research/31-caremark-rsi-board-exposure.md) — Kahana three-part RSI test, AILCCP controls
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.3a GF-C-orphan dispatch
