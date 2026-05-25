# Discipline: Holdout-partition

Builder agents cannot read the artifacts (scenarios, acceptance criteria, runtime telemetry, production traces) used to judge their output; the substrate enforces the partition, not the methodology. The discipline survives the D-2 brownfield challenge (scenarios may live in-tree) by re-anchoring the contract on *unseen-by-builder*, not *out-of-tree*. F28 (holdout leakage) is the failure mode; D-4 (brief §4.1) is the corpus default; the discipline is the operational form of D-4.

## Named-by

All 10 tracks. D-4 is `accepted` or `accepted-and-expanded` across the board.

- `GF-S` — *"Builder agents cannot read"* substrate-typed; S2 scenario storage enforces builder-blindness. [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S2 / §4 D-4.
- `BF-S` — *"Holdout discipline applies to telemetry-as-scenario (S-3 read partitioning), not just file-system scenario directories. Substrate enforcement is exactly the point."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §1.1 S-3 / §4 D-4.
- `BF-L` — in-model partition enforcement: the substrate marks subsets of the codebase-model as held-out; ingestion-aware judges enforce the partition. [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §1.
- `BF-M` — *"Stage 5 builder agent does not see stage 7 acceptance set; substrate enforces the air-gap. Brownfield re-defines the holdout per D-2 challenge but the discipline of *not letting builder see acceptance* is unchanged."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §4 D-4.
- `GF-C` — bench-construction agents and builder agents *never share context*; enforced at substrate, not methodology discipline (per F53). [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §4 D-4.
- `GF-M` — substrate-enforced read masking required for the sandboxed filesystem partition. [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.3.
- `U-A` — *"This architecture is uncompromising on this point: the substrate's policy mediator refuses to close a `kind: judge` interval if acceptance-criteria handles leaked into the upstream builder interval's inputs."* [unified-A.md](../tracks/unified-A.md) §4 D-4.
- `U-B` — substrate enforces per-layer; L3 plan-layer holdout from L4 builders is the primary instance. [unified-B.md](../tracks/unified-B.md) §4 D-4.
- `U-C` — distance-gated dispatcher is the substrate-enforced holdout boundary; near-anchor work has acceptance criteria withheld by the dispatcher itself. [unified-C.md](../tracks/unified-C.md) §4 D-4.
- `D7-U-1` — *"This architecture generalises D-4 to every artifact boundary."* The compounding gate is the substrate's universal holdout primitive. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §4 D-4.

## Corpus motivation

- **D-4** — brief §4.1.
- **F28** in [failure-modes-v3.md](../failure-modes-v3.md) §2 — holdout leakage, greenfield-critical.
- **Round-2 C13** — D-4 corpus origin.
- **CTR-B5 / CTR-G2** ([contradictions.md](../contradictions.md)) — the brownfield D-2 inversion that forces the *unseen* re-framing of holdout.
- **Report 01 §1** — StrongDM's "Tokens are the fuel" enumeration of incident replays / agentic simulation as in-runtime scenario-equivalents (the WEAK-3 sharpening).

## Open questions

- **Does D-2 challenge cascade to D-4?** BF-S §7 OQ-T5: if scenarios are inside the codebase and holdout is enforced by substrate read partitioning, substrate is now load-bearing for something Round-2 promoted as methodology discipline. May surface substrate-vs-methodology boundary issues at Phase 4.
- **How is "unseen subset" selected from a codebase-derived pool without leaking?** BF-M §7 #4: "Scenarios-from-codebase governance" — D-2 challenge inverts holdout-location but does not specify the selection protocol.
- **At population scale**, U-A §7 OQ-4: if many intervals share access to the same trajectory store or scenario library, F48 multi-agent collusion may re-emerge at substrate layer.

## Substrate-enforcement options

- `GF-S` `S2 scenario storage` — typed objects in substrate-managed store; builder agents cannot read.
- `BF-S` `S-3 runtime/telemetry ingestor` — substrate exposes telemetry queryable by tools but partitioned by role.
- `BF-L` `codebase model` with in-model partition fields — substrate marks held-out subsets.
- `BF-M` — sandbox + worktree isolation (F17) at stage 5.
- `U-A` `policy mediator` — refuses to close judge intervals on contamination.
- `U-C` `distance-gated dispatcher` — withholds acceptance from near-anchor work.
- `D7-U-1` `compounding gate` — generalises to all artifact boundaries.

Disciplines are distinct from these primitives by working-definition.
